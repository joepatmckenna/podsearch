import json
import logging
import time

import flask
import flask_cors
import numpy as np
import podsearch
import scann
import transformers

log = logging.getLogger(__name__)

search_fn = None


def load_search_fn():

    global search_fn
    if search_fn is not None:
        return
    load_search_fn_in_progress = True
    start = time.time()
    def _path(asset): return f'{podsearch.BASE_DIR}/../{asset}'
    tokenizer = transformers.AutoTokenizer.from_pretrained(_path('tokenizer'))
    model = transformers.AutoModel.from_pretrained(_path('model')).eval()
    searcher = scann.scann_ops_pybind.load_searcher(_path('searcher'))
    with open(_path('encodings_metadata.json'), 'rt') as fileobj:
        encodings_metadata = json.load(fileobj)

    def _search_fn(query):
        results = []
        query = podsearch.utils.preprocess(query)
        encoding = podsearch.utils.encode([query], tokenizer, model)
        encoding = encoding.squeeze().numpy()
        encoding /= np.linalg.norm(encoding)
        neighbors, scores = searcher.search(encoding)
        return dict(
            query=query,
            results=[encodings_metadata[i] for i in neighbors],
            scores=scores.tolist(),
        )
    search_fn = _search_fn
    log.info(f'finished loading search_fn in {time.time()-start} sec')


def create_server():
    server = flask.Flask(__name__)

    @server.get('/wakeup')
    def wakeup():
        global search_fn
        load_search_fn()
        return {'awake': search_fn is not None}

    @server.get('/awake')
    def awake():
        global search_fn
        return {'awake': search_fn is not None}

    @server.get('/search')
    def search():
        global search_fn
        query = flask.request.args.get('query', '')
        return search_fn(query)

    flask_cors.CORS(server)
    return server


if __name__ == '__main__':
    create_server().run(debug=True, host='0.0.0.0', port=8080)

#
