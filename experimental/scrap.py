# import requests
# model = 'facebook/bart-base'
# @routes.get("/")
# def _search():
#     x = requests.post(
#         f'https://api-inference.huggingface.co/models/{model}',
#         headers={
#             'Authorization': 'Bearer XXXX' # login to huggingface
#         },
#         json={
#             'inputs': 'trump',
#             'options': {
#                 'use_cache': True,
#                 'wait_for_model': False,
#             }
#         },
#     ).json()
#     return {'response': x}

# @functools.cache
# def _get_subtitles(video_id):
#     subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
#         video_id, languages=('en', ))
#     # fix durations
#     for i in range(len(subtitles) - 1):
#         subtitles[i]['duration'] = (subtitles[i + 1]['start'] -
#                                     subtitles[i]['start'])
#     return subtitles

# def _intersects(existing, new):
#     for start, end in existing:
#         if ((start <= new[0] <= end) or (start <= new[1] <= end)):
#             return True
#     return False

# def _process_results(results):
#     processed_results = []
#     intervals = {}
#     for result in results:
#         decoded_id = dict(k.split('=') for k in result.id.split('-'))
#         video_id = decoded_id.pop('video_id')
#         start_index = int(decoded_id.pop('subtitles_start_index'))
#         end_index = int(decoded_id.pop('subtitles_end_index'))
#         if _intersects(intervals.setdefault(video_id, []),
#                        (start_index, end_index)):
#             continue
#         intervals[video_id].append((start_index, end_index))
#         subtitles = _get_subtitles(video_id)
#         transcript = ' '.join(subtitles[i]['text']
#                               for i in range(start_index, end_index + 1))
#         processed_results.append({
#             'distance': result.distance,
#             'video_id': video_id,
#             'start': decoded_id.pop('start_sec'),
#             'end': decoded_id.pop('end_sec'),
#             'transcript': transcript
#         })
#     return processed_results

# encoding = podsearch.utils.encode([query]).squeeze().tolist()
# results = aiplatform.MatchingEngineIndexEndpoint(
#     index_endpoint_name='9035918498458501120',
#     project='podsearch-367715',
#     location='us-central1',
# ).match(
#     deployed_index_id=
#     'video_id_VeH7qKZr0WI_word_threshold_512_sentence_overlap_3',
#     queries=[encoding],
#     num_neighbors=16,
# )[0]
# results = _process_results(results)
# return {'query': query, 'search_results': results}

# import functools
# from google.cloud import aiplatform
# import os
# import youtube_transcript_api
