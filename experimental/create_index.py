import json
from google.cloud import aiplatform
from google.cloud import storage
import podsearch.utils
import youtube_transcript_api

project = 'podsearch-367715'
location = 'us-central1'
video_id = 'VeH7qKZr0WI'  # Balaji

encoding_id_template = '-'.join((
    f'video_id={video_id}',
    'start_sec={start_sec}',
    'end_sec={end_sec}',
    'subtitles_start_index={subtitles_start_index}',
    'subtitles_end_index={subtitles_end_index}',
))

WORD_THRESHOLD = 512
SENTENCE_OVERLAP = 3

index_name = '-'.join((
    f'video_id={video_id}',
    f'word_threshold={WORD_THRESHOLD}',
    f'sentence_overlap={SENTENCE_OVERLAP}',
))

subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
    video_id, languages=('en', ))

# fix durations
for i in range(len(subtitles) - 1):
    subtitles[i]['duration'] = (subtitles[i + 1]['start'] -
                                subtitles[i]['start'])

encodings = []
subtitles_start_index, subtitles_end_index = 0, 0
while subtitles_end_index < len(subtitles) - 1:
    subtitles_end_index = subtitles_start_index = subtitles_start_index + (
        subtitles_end_index - subtitles_start_index) // SENTENCE_OVERLAP
    words = []
    while True:
        words.extend(subtitles[subtitles_end_index]['text'].split())
        if (len(words) > WORD_THRESHOLD
                or subtitles_end_index == len(subtitles) - 1):
            break
        subtitles_end_index += 1
    start_subtitle = subtitles[subtitles_start_index]
    end_subtitle = subtitles[subtitles_end_index]
    encoding_id = encoding_id_template.format(
        start_sec=int(start_subtitle['start']),
        end_sec=int(end_subtitle['start'] + end_subtitle['duration']),
        subtitles_start_index=subtitles_start_index,
        subtitles_end_index=subtitles_end_index,
    )
    sentence = ' '.join(words)
    encoding = podsearch.utils.encode(sentence).squeeze().tolist()
    encodings.append({'id': encoding_id, 'embedding': encoding})

    print(
        subtitles_start_index,
        len(subtitles),
        len(encodings),
        encoding_id,
        # sentence,
        end='\r')

# print('uploading to gcs')
# storage_client = storage.Client(project=project)
# bucket_name = f'{project}-matching_engine'
# bucket = storage_client.bucket(bucket_name)
# if not bucket.exists():
#     storage_client.create_bucket(bucket, project=project, location=location)
# blob = bucket.blob(f'{index_name}/encodings.json')
# blob.upload_from_string('\n'.join(map(json.dumps, encodings)))

# print('creating ann index')
# index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
#     display_name=index_name,
#     contents_delta_uri=f'gs://{bucket_name}/{index_name}',
#     dimensions=len(encodings[0]['embedding']),
#     approximate_neighbors_count=16,
#     distance_measure_type=(
#         aiplatform.matching_engine.matching_engine_index_config.
#         DistanceMeasureType.COSINE_DISTANCE.value),
#     project=project,
#     location=location,
# )

# print('creating endpoint')
# endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
#     display_name='podsearch_index_endpoint',
#     network='projects/945366276631/global/networks/default',
#     project=project,
#     location=location,
# )

# print('deploying index')
# deployed_index_id = index_name.replace('=', '_').replace('-', '_')
# endpoint.deploy_index(
#     index=index,
#     deployed_index_id=deployed_index_id,
# )

# # results = endpoint.match(
# #     deployed_index_id=index_name,
# #     queries=[[0.0 for _ in range(384)]],
# #     num_neighbors=1,
# # )

# # endpoint = aiplatform.MatchingEngineIndexEndpoint(
# #     index_endpoint_name='3599510798268891136',
# #     project=project,
# #     location=location,
# # )
# # index = aiplatform.MatchingEngineIndex(
# #     index_name='7718052657499209728',
# #     project=project,
# #     location=location,
# # )
# # endpoint.undeploy_index(deployed_index_id=deployed_index_id)
# # endpoint.undeploy_index(deployed_index_id='test_deployed_index')
# # index.delete()
# # endpoint.delete()

# endpoint = aiplatform.MatchingEngineIndexEndpoint(
#     index_endpoint_name='9035918498458501120')
# endpoint.undeploy_index(
#     deployed_index_id=
#     'video_id_VeH7qKZr0WI_word_threshold_512_sentence_overlap_3')
# endpoint.delete()
# index = aiplatform.MatchingEngineIndex(index_name='7059964161949696000')
# index.delete()

