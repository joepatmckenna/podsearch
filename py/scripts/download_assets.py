import argparse
import json
import os

import transformers
from google.cloud import storage

project = 'podsearch-367715'
storage_client = storage.Client(project=project)

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def main(service):

    assets_dir = f'{THIS_DIR}/../../assets/{service}'

    print(f'downloading assets for service {service} to {assets_dir}')

    PLAYLIST_ID = 'PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4'
    MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

    encoding_type = f'{MODEL_NAME}/word_threshold=128-stride_overlap=2'
    bucket = storage_client.bucket(f'{project}-youtube')

    if service == 'search':
        # encodings/searcher
        os.makedirs(f'{assets_dir}/encodings/searcher', exist_ok=True)
        # prefix = f'{PLAYLIST_ID}/encodings/{MODEL_NAME}/word_threshold={WORD_THRESHOLD}-stride_overlap={STRIDE_OVERLAP}/searcher'
        for blob in bucket.list_blobs(prefix=f'{PLAYLIST_ID}/encodings/{encoding_type}/searcher'):
            filename = f'{assets_dir}/encodings/searcher/{os.path.basename(blob.name)}'
            blob.download_to_filename(filename)

        # tokenizer
        tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_NAME)
        tokenizer.save_pretrained(f'{assets_dir}/tokenizer')

        # model
        model = transformers.AutoModel.from_pretrained(MODEL_NAME)
        model.save_pretrained(f'{assets_dir}/model')

        # encodings/metadata.json
        os.makedirs(f'{assets_dir}/encodings', exist_ok=True)
        # f'{PLAYLIST_ID}/encodings/{MODEL_NAME}/word_threshold={WORD_THRESHOLD}-stride_overlap={STRIDE_OVERLAP}/metadata.json'
        blob = bucket.blob(
            f'{PLAYLIST_ID}/encodings/{encoding_type}/metadata.json')
        blob.download_to_filename(f'{assets_dir}/encodings/metadata.json')

        # videos.json
        # f'{PLAYLIST_ID}/videos.json'
        blob = bucket.blob(f'{PLAYLIST_ID}/videos.json')
        blob.download_to_filename(f'{assets_dir}/videos.json')

        # # videos/{video_id}.json
        # os.makedirs(f'{assets_dir}/videos/', exist_ok=True)

    elif service == 'frontend':

        # videos.json
        blob = bucket.blob(f'{PLAYLIST_ID}/videos.json')
        blob.download_to_filename(f'{assets_dir}/videos.json')

        # captions.json
        blob = bucket.blob(f'{PLAYLIST_ID}/captions.json')
        blob.download_to_filename(f'{assets_dir}/captions.json')

        # # captions/{video_id}.json
        # os.makedirs(f'{assets_dir}/captions/', exist_ok=True)
        # playlist = json.loads(bucket.blob(
        #     f'{PLAYLIST_ID}/metadata.json').download_as_string())
        # for playlist_item in playlist:
        #     video_id = playlist_item['snippet']['resourceId']['videoId']
        #     # # video
        #     # blob = bucket.blob(f'{PLAYLIST_ID}/{video_id}/metadata.json')
        #     # filename = f'{assets_dir}/videos/{video_id}.json'
        #     # if not os.path.exists(filename):
        #     #     blob.download_to_filename(filename)
        #     # caption
        #     blob = bucket.blob(f'{PLAYLIST_ID}/{video_id}/captions.json')
        #     if not blob.exists():
        #         continue
        #     filename = f'{assets_dir}/captions/{video_id}.json'
        #     # blob.download_to_filename(filename)
        #     captions = json.loads(blob.download_as_string())
        #     captions = [caption['text'] for caption in captions]
        #     with open(filename, 'wt') as fileobj:
        #         json.dump(captions, fileobj)

    else:
        raise ValueError(f'service {service} not recognized.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', help='cloud run service', required=True)
    args = parser.parse_args()
    main(args.service)
