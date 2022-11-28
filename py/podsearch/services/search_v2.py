import argparse
import functools
import json
import logging
import multiprocessing
import os
import scann
import socket
import socketserver
import sys
import threading
import time
from typing import Any, Optional, Union

import flask
import flask_cors
import gunicorn.app.base
import numpy as np
import podsearch
import transformers

# maximum length of search query in characters
MAX_QUERY_CHARS = 2048

Query = str
SearchResult = dict[str, Union[int, float, str]]
SearchResults = list[SearchResult]
SearchResponse = dict[str, Union[Query, SearchResults]]
"""
SearchResult: {
    'score': float,
    'video_id': str,
    'start_sec': int,
    'end_sec': int,
    'text': str,
    'start_captions_index': int,
    'end_captions_index': int
}

SearchResponse: {
    'query': str, (preprocessed version passed to tokenizer)
    'results': [SearchResult, SearchResult, ... ]
}
"""

log = logging.getLogger(__name__)


def log_latency(func):
    def timed_func(*args, **kwargs):
        start = time.time()
        retval = func(*args, **kwargs)
        log.info(
            f'{repr(func)}, '
            f'PID: {multiprocessing.current_process().pid}, '
            f'latency: {int(1000*(time.time() - start))} ms, '
        )
        return retval
    timed_func.__name__ = f'timed_{func.__name__}'
    return timed_func


class SearchServer(socketserver.TCPServer):
    '''Performs the nearest neigbor search.

    asset                      size
    --------------------------------
    tokenizer                  932K
    model                       87M
    encodings/searcher          66M
    encodings/metadata.json     24M
                               178M

    Maybe implement
    - verify_request(request, client_address)
    - handle_error()
    - handle_timeout()
    '''

    def __init__(self, asset_dir: str,  max_query_chars=MAX_QUERY_CHARS):
        super().__init__(('localhost', 0), SearchRequestHandler)
        self._asset_dir = asset_dir
        self.max_query_size = sys.getsizeof(max_query_chars * b'')

    @log_latency
    def search(self, query: str) -> SearchResponse:
        encoding: np.ndarray = self._encode_query(query)
        results: SearchResults = self._find_neighbors(encoding)
        return results

    @log_latency
    def _encode_query(self, query: str) -> np.ndarray:
        encoding = podsearch.utils.encode([query], self.tokenizer, self.model)
        encoding = encoding[0].numpy()
        return encoding / np.linalg.norm(encoding)

    @log_latency
    def _find_neighbors(self, encoding: np.ndarray) -> list[SearchResult]:
        results = list()
        neighbors, scores = self.searcher.search(encoding)
        for index, score in zip(neighbors, scores):
            result = self.encodings_metadata[index]
            result['score'] = float(score)
            results.append(result)
        return results

    @functools.cached_property
    def tokenizer(self) -> transformers.tokenization_utils_base.PreTrainedTokenizerBase:
        return transformers.AutoTokenizer.from_pretrained(f'{self._asset_dir}/tokenizer')

    @functools.cached_property
    def model(self) -> transformers.modeling_utils.PreTrainedModel:
        model = transformers.AutoModel.from_pretrained(
            f'{self._asset_dir}/model')
        model.eval()
        return model

    @functools.cached_property
    def encodings_metadata(self) -> list[SearchResult]:
        with open(f'{self._asset_dir}/encodings/metadata.json', 'rt') as fileobj:
            return json.load(fileobj)

    @functools.cached_property
    def searcher(self) -> 'scann.scann_ops_pybind.ScannSearcher':
        # try:
        return scann.scann_ops_pybind.load_searcher(
            f'{self._asset_dir}/encodings/searcher')
        # except:
        #     class Searcher:
        #         def __init__(self, n):
        #             self.n = n

        #         def search(self, _):
        #             neighbors = random.sample(list(range(self.n)), 512)
        #             scores = [random.random() for _ in neighbors]
        #             return neighbors, scores
        #     return Searcher(len(self.encodings_metadata))


class SearchRequestHandler(socketserver.BaseRequestHandler):
    @log_latency
    def handle(self):
        # recvall causes deadlocking here for reasons i don't understand
        query: bytes = self.request.recv(self.server.max_query_size)
        results = self.server.search(query.decode())
        response: bytes = json.dumps(results).encode()
        self.request.sendall(response)


class SearchApp(gunicorn.app.base.BaseApplication):
    def __init__(self, options: Optional[dict[str, Any]] = None):
        self._options = options or dict()
        super().__init__()

    def load_config(self):
        for key, value in self._options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)
        log.info(self.cfg)

    def load(self) -> flask.app.Flask:
        """Creates instance of web server gateway interface (WSGI) app."""
        app = flask.Flask(__name__)

        @app.get('/')
        def status() -> dict[str, str]:
            return {'status': 'ok'}

        @app.get('/search')
        @log_latency
        def search() -> SearchResponse:
            query: Query = podsearch.utils.preprocess(
                flask.request.args.get('query', ''))
            if not query:
                return {'query': '', 'results': []}
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(self._options['search_server_address'])
                sock.sendall(query.encode())
                response: bytes = podsearch.utils.recvall(sock)
            results = json.loads(response)
            return {'query': query, 'results': results}

        @app.get('/videos')
        @log_latency
        def get_videos_metadata():
            return flask.send_from_directory(self._options["asset_dir"], 'videos.json')

        # response too large
        # @ app.get('/captions')
        # @ log_latency
        # def get_captions():
        #     return flask.send_from_directory(self._options["asset_dir"], f'captions.json')

        # video_ids_with_captions = set(os.path.splitext(
        #     f)[0] for f in os.listdir(f'{self._options["asset_dir"]}/captions'))

        # @app.get('/captions/<video_id>')
        # @log_latency
        # def get_captions_for_video(video_id):
        #     if video_id in video_ids_with_captions:
        #         return flask.send_from_directory(
        #             f'{self._options["asset_dir"]}/captions', f'{video_id}.json')
        #     return {}

        # @app.get('/video/<video_id>')
        # @log_latency
        # def get_video(video_id):
        #     return flask.send_from_directory(
        #         f'{self._options["asset_dir"]}/videos', f'{video_id}.json')

        flask_cors.CORS(app)
        return app


def main(args):
    options = {
        'bind': f'{args.address}:{os.environ.get("PORT", args.port)}',
        'workers': args.workers or os.cpu_count(),
        'asset_dir': args.asset_dir,
    }

    # search server runs in a thread in the main process and handles
    # internal requests from gunicorn workers, it holds references to
    # the tokenizer, model, searcher, and encodings metadata
    SearchServer.request_queue_size = 128 * options['workers']
    server = SearchServer(args.asset_dir)

    with server:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        options.update({
            'search_server_address': server.server_address,
            'on_exit': lambda _: (server.shutdown() and thread.join())
        })

        # search app runs in the main process and passes external
        # requests to gunicorn workers running app
        # SearchApp(wsgi, options).run()
        SearchApp(options).run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', default='0.0.0.0')
    parser.add_argument('--port', default=8080)
    parser.add_argument('--asset-dir', default='/PodSearch')
    parser.add_argument('--workers', default=None)
    args = parser.parse_args()
    main(args)
