


# """
# pip install https://github.com/pietrodn/grpcio-mac-arm-build/releases/download/1.50.0/grpcio-1.50.0-cp310-cp310-macosx_11_0_arm64.whl --force-reinstall --no-cache-dir
# """
# from collections.abc import Iterator
# # from google.cloud import storage
# import json
# import os
# import sentence_transformers
# from typing import Optional, Union

# project = 'podsearch-367715'

# VIDEO_ID = 'VeH7qKZr0WI'  # Balaji
# # VIDEO_ID = 'DxREm3s1scA'  # Elon

# Embeddings = dict[str, list[float]]
# Example = dict[str, Union[int, str]]
# Subtitles = list[dict[str, Union[float, str]]]

# def _get_next_start_index(
#     subtitles: Subtitles,
#     index: int,
#     max_word_stride: int = 64,
# ) -> int:
#     num_words = 0
#     while index < len(subtitles) - 1:
#         n = len(subtitles[index]['text'].split())
#         if num_words + n > max_word_stride:
#             break
#         num_words += n
#         index += 1
#     return index

# def _generate_example(
#     subtitles: Subtitles,
#     start_index: int,
#     max_num_words: int = 1024,
#     min_num_words: int = 896,
# ) -> Optional[Example]:

#     words = []
#     end_index = start_index
#     while True:
#         subtitle = subtitles[end_index]
#         w = subtitle['text'].split()
#         if len(words) + len(w) > max_num_words:
#             break
#         words.extend(w)
#         if end_index == len(subtitles) - 1:
#             break
#         end_index += 1

#     num_words = len(words)
#     if num_words < min_num_words:
#         return

#     start_subtitle = subtitles[start_index]
#     end_subtitle = subtitles[end_index]
#     return {
#         'text': ' '.join(words),
#         'start_ms': int(1000 * start_subtitle['start']),
#         'end_ms': int(1000 * end_subtitle['start'] + end_subtitle['duration']),
#         'num_words': num_words,
#     }

# def _generate_batches(
#     video_id: str,
#     batch_size: int = 32,
# ) -> Iterator[list[Example]]:

#     subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
#         video_id, languages=('en', ))
#     # fix durations
#     for i, s in enumerate(subtitles[:-1]):
#         subtitles[i]['duration'] = subtitles[i + 1]['start'] - s['start']

#     subtitle_index = 0
#     batch = []
#     while True:
#         example = _generate_example(
#             subtitles,
#             subtitle_index,
#         )
#         is_last_example = example is None
#         if len(batch) == batch_size or is_last_example:
#             yield batch
#             batch = []
#         if is_last_example:
#             return
#         batch.append(example)
#         subtitle_index = _get_next_start_index(
#             subtitles,
#             subtitle_index,
#         )

# def get_embeddings(
#     video_id: str,
#     model_name: str = 'sentence-t5-base',
# ) -> Embeddings:

#     model = sentence_transformers.SentenceTransformer(
#         f'sentence-transformers/{model_name}')

#     embedding_id_template = '-'.join((
#         f'video_id={video_id}',
#         'start_ms={start_ms}',
#         'end_ms={end_ms}',
#         'num_words={num_words}',
#     ))

#     embeddings = {}
#     for batch in _generate_batches(video_id):
#         outputs = model.encode([example['text'] for example in batch])
#         for example, embedding in zip(batch, outputs):
#             embedding_id = embedding_id_template.format(**example)
#             embeddings[embedding_id] = embedding.tolist()

#     return embeddings

# # embeddings = get_embeddings(VIDEO_ID)

# model_name: str = 'sentence-t5-base'

# model = sentence_transformers.SentenceTransformer(
#     f'sentence-transformers/{model_name}')

# model = sentence_transformers.SentenceTransformer(
#     './data/models/sentence-t5-base')

# # bucket_name = f'{project}-matching_engine'
# # storage_client = storage.Client(project=project)
# # bucket = storage_client.bucket(bucket_name)
# # if not bucket.exists():
# #     bucket.create()
# # blob = bucket.blob(embeddings_path.name)
# # if not blob.exists():
# #     blob.upload_from_filename(embeddings_path)

# # # aiplatform.MatchingEngineIndex.create_tree_ah_index(
# # #     display_name=f'video-{VIDEO_ID}_window-{window}_stride-{stride}',
# # #     contents_delta_uri='gs://',
# # #     dimensions=embeddings.shape[1],
# # #     approximate_neighbors_count=256,
# # #     distance_measure_type='COSINE_DISTANCE',
# # #     location='us-central1',
# # #     sync=False)

# # from google.cloud import aiplatform
# # from google.cloud import storage
# # import json
# # import pathlib
# # import sentence_transformers
# # import youtube_transcript_api

# # SUBTITLES_LANGUAGE = "en"

# # subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
# #     VIDEO_ID, languages=(SUBTITLES_LANGUAGE, ))

# # # fix durations
# # for i, s in enumerate(subtitles[:-1]):
# #     subtitles[i]['duration'] = subtitles[i + 1]['start'] - s['start']

# # max_word_stride = 64

# # max_num_words = 1024
# # min_num_words = max_num_words - 2 * max_word_stride

# # model_name = 'sentence-t5-base'

# # model = sentence_transformers.SentenceTransformer(
# #     f'sentence-transformers/{model_name}')

# # DATA_DIR = pathlib.Path.home() / 'WhatDidJoeSay/data'
# # embeddings_path = DATA_DIR / 'embeddings' / f'video_id={VIDEO_ID}-model={model_name}-max_num_words={max_num_words}-max_word_stride={max_word_stride}.json'

# # def generate_example(start_index):
# #     words = []
# #     end_index = start_index
# #     while True:
# #         subtitle = subtitles[end_index]
# #         w = subtitle['text'].split()
# #         if len(words) + len(w) > max_num_words:
# #             break
# #         words.extend(w)
# #         if end_index == len(subtitles) - 1:
# #             break
# #         end_index += 1
# #     num_words = len(words)
# #     if num_words < min_num_words:
# #         return
# #     start_subtitle = subtitles[start_index]
# #     end_subtitle = subtitles[end_index]
# #     return {
# #         'start_ms': int(1000 * start_subtitle['start']),
# #         'end_ms': int(1000 * end_subtitle['start'] + end_subtitle['duration']),
# #         'num_words': num_words,
# #         'text': ' '.join(words)
# #     }

# # def get_next_start_index(index):
# #     num_words = 0
# #     while index < len(subtitles):
# #         n = len(subtitles[index]['text'].split())
# #         if num_words + n > max_word_stride:
# #             break
# #         num_words += n
# #         index += 1
# #     return index

# # if embeddings_path.is_file():
# #     with embeddings_path.open('rt') as fileobj:
# #         embeddings = json.load(fileobj)
# # else:
# #     embeddings = {}
# #     embedding_id_template = f'video_id={VIDEO_ID}-start_ms={{start_ms}}-end_ms={{end_ms}}-num_words={{num_words}}'
# #     subtitle_index = 0
# #     batch_size = 32
# #     inputs = []
# #     while True:
# #         print(subtitle_index, len(subtitles), end='\r')
# #         example = generate_example(subtitle_index)
# #         is_last_example = example is None
# #         if len(inputs) == batch_size or is_last_example:
# #             outputs = model.encode([x['text'] for x in inputs])
# #             embeddings.update({
# #                 embedding_id_template.format(**i): o.tolist()
# #                 for i, o in zip(inputs, outputs)
# #             })
# #             inputs = []
# #         if is_last_example:
# #             break
# #         inputs.append(example)
# #         subtitle_index = get_next_start_index(subtitle_index)
# #     embeddings_path.parent.mkdir(parents=True, exist_ok=True)
# #     with embeddings_path.open('wt') as fileobj:
# #         json.dump(embeddings, fileobj)

# # # def retrieve(text, k=128):
# # #     text = text.lower().strip()
# # #     scores = embeddings.dot(model.encode([text]).T).squeeze()
# # #     indices = np.argpartition(-scores, kth=k)[:k]
# # #     return sorted(indices, key=scores.__getitem__, reverse=True)

# # # import os
# # # import youtube_dl
# # # import webvtt

# # # encoder = tensorflow_hub.KerasLayer(
# # #     "https://tfhub.dev/google/sentence-t5/st5-base/1")

# # # VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"

# # # SUBTITLES_FORMAT = "vtt"
# # # SUBTITLES_FILENAME = f'{VIDEO_ID}.{SUBTITLES_LANGUAGE}.{SUBTITLES_FORMAT}'

# # # class AutomaticSubtitles(dict):

# # #     def __init__(self, video_url):
# # #         ydl = youtube_dl.YoutubeDL({
# # #             'listsubtitles': True,
# # #             'skip_download': True
# # #         })
# # #         _to_screen = ydl.to_screen
# # #         try:
# # #             ydl.to_screen = self._handle_message
# # #             with ydl:
# # #                 ydl.download([video_url])
# # #         finally:
# # #             ydl.to_screen = _to_screen

# # #     def _handle_message(self, message, **kwargs):
# # #         if not message.startswith("Language formats"):
# # #             return
# # #         for line in message.splitlines()[1:]:
# # #             print(line)
# # #             language, formats = line.split(maxsplit=1)
# # #             formats = {f.strip() for f in formats.split(',')}
# # #             self.__setitem__(language, formats)

# # # if not os.path.exists(SUBTITLES_FILENAME):
# # #     automatic_subtitles = AutomaticSubtitles(VIDEO_URL)
# # #     if SUBTITLES_FORMAT in automatic_subtitles.get(SUBTITLES_LANGUAGE, set()):
# # #         with youtube_dl.YoutubeDL({
# # #                 'writeautomaticsub': True,
# # #                 'subtitleslangs': [SUBTITLES_LANGUAGE],
# # #                 'subtitlesformat': SUBTITLES_FORMAT,
# # #                 'skip_download': True,
# # #                 'outtmpl': '%(id)s.%(ext)s',
# # #         }) as ydl:
# # #             ydl.download([VIDEO_URL])

# # # # for caption in webvtt.read(subtitles_filename):
# # # #     pass
