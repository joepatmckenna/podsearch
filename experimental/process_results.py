from google.cloud import aiplatform
import functools
import json
import youtube_transcript_api

with open('results.json', 'rt') as fileobj:
    results = json.load(fileobj)


@functools.cache
def get_subtitles(video_id):
    subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
        video_id, languages=('en', ))
    # fix durations
    for i in range(len(subtitles) - 1):
        subtitles[i]['duration'] = (subtitles[i + 1]['start'] -
                                    subtitles[i]['start'])
    return subtitles


intervals = {}


def intersects(existing, new):
    for start, end in existing:
        if ((start <= new[0] <= end) or (start <= new[1] <= end)):
            return True
    return False


for result in results['results']:
    result = aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor(
        id=result['id'], distance=result['distance'])
    result = dict(k.split('=') for k in result.id.split('-'))
    video_id = result.pop('video_id')
    start_index = int(result.pop('subtitles_start_index'))
    end_index = int(result.pop('subtitles_end_index'))
    if intersects(intervals.setdefault(video_id, []),
                  (start_index, end_index)):
        continue
    intervals[video_id].append((start_index, end_index))
    subtitles = get_subtitles(video_id)
    text = ' '.join(subtitles[i]['text']
                    for i in range(start_index, end_index + 1))
    start = result.pop('start_sec')
    end = result.pop('end_sec')
    link = f'https://www.youtube.com/embed/{video_id}?start={start}&end={end}'
    print(link, ' '.join(text.split()[:16]))
