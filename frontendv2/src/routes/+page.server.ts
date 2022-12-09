import type { Actions, RequestEvent } from '@sveltejs/kit';

import { zip, argsort, sum } from '$lib/utils';

const RESULT_MARGIN_SECS = 300;
const MAX_RESULTS_PER_VIDEO = 8;
const SCORE_THRESHOLD = 0.33;

interface SearchResult {
  video_id: string;
  score: number;
  start: number;
  end: number;
  captions_start: number;
  captions_end: number;
}

interface VideoSearchResult {
  scores: number[];
  starts: number[];
  ends: number[];
  captions_starts: number[];
  captions_ends: number[];
}

interface VideoMetadata {
  videoId: string;
}

let VIDEOS: VideoMetadata[];

const aggregateResultsByVideo = (results: SearchResult[]) => {
  const _videoResults: VideoSearchResult[] = Object.entries(
    // reformat videoId -> { (aggregated values) }
    results.reduce(
      (
        resultsByVideoId: { [videoId: string]: VideoSearchResult },
        { video_id: videoId, score, start, end, captions_start, captions_end }
      ) => {
        if (score > SCORE_THRESHOLD) {
          const videoResult: VideoSearchResult = resultsByVideoId[videoId] || {
            scores: [],
            starts: [],
            ends: [],
            captions_starts: [],
            captions_ends: []
          };
          videoResult.scores.push(score);
          videoResult.starts.push(start);
          videoResult.ends.push(end);
          videoResult.captions_starts.push(captions_start);
          videoResult.captions_ends.push(captions_end);
          resultsByVideoId[videoId] = videoResult;
        }
        return resultsByVideoId;
      },
      {}
    )
  )
    // move videoId keys into values, convert map to array
    .map(([videoId, videoResult]) => {
      videoResult.videoId = videoId;
      return videoResult;
    })
    // sort by agg (summed) score
    .sort(({ scores: s1 }, { scores: s2 }) => sum(s2) - sum(s1))
    // select top results per video
    .map((videoResult) => {
      const n = Math.min(MAX_RESULTS_PER_VIDEO, videoResult.scores.length);
      const order = argsort(videoResult.scores.map((s) => -s)).slice(0, n);
      for (const key of [
        'scores',
        'starts',
        'ends',
        'captions_starts',
        'captions_ends'
      ]) {
        videoResult[key] = order.map((i) => videoResult[key][i]);
      }
      return videoResult;
    })
    // sort timestamps and caption indices
    .map((videoResult) => {
      const order = argsort(videoResult.ends);
      for (const key of [
        'scores',
        'starts',
        'ends',
        'captions_starts',
        'captions_ends'
      ]) {
        videoResult[key] = order.map((i) => videoResult[key][i]);
      }
      return videoResult;
    })
    // remove intersecting intervals
    .map((videoResult) => {
      const keep = zip([videoResult.starts, videoResult.ends]).reduce(
        ({ indices, ends }, [start, end], index) => {
          if (
            indices.length == 0 ||
            start > ends[ends.length - 1] + RESULT_MARGIN_SECS
          ) {
            indices.push(index);
            ends.push(end);
          }
          return { indices: indices, ends: ends };
        },
        { indices: [], ends: [] }
      );
      for (const key of [
        'scores',
        'starts',
        'ends',
        'captions_starts',
        'captions_ends'
      ]) {
        videoResult[key] = keep.indices.map((i) => videoResult[key][i]);
      }
      return videoResult;
    })
    // only keep videos with >1 result
    .filter((videoResult) => videoResult.scores.length > 1)
    // keep top videos
    .slice(0, 32)
    // add in video metadata
    .map((videoResult) => {
      return { ...videoResult, ...VIDEOS[videoResult.videoId] };
    });
    // .filter((videoResult) => videoResult.playableInEmbed);
  // // add in captions
  // .map((videoResult) => {
  //   videoResult.captions = zip([
  //     videoResult.captions_starts,
  //     videoResult.captions_ends
  //   ]).map(([captions_start, captions_end]) => {
  //     return (CAPTIONS[videoResult.videoId] || [])
  //       .slice(captions_start, captions_end + 1)
  //       .join(' ');
  //   });
  //   return videoResult;
  // });

  return _videoResults;
};

export const actions: Actions = {
  default: async (event: RequestEvent) => {
    const url = event.url.href;
    const formData = await event.request.formData();
    const searchResponse = await fetch(`${url}api/search`, {
      method: 'POST',
      body: JSON.stringify({ query: formData.get('query') })
    });
    const data = await searchResponse.json();
    const results: SearchResult[] = data.results;
    if (!VIDEOS) VIDEOS = await (await fetch(`${url}api/videos`)).json();
    data.videoResults = aggregateResultsByVideo(results);
    return data;
  }
};
