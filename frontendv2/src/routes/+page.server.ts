import type { Actions, RequestEvent } from '@sveltejs/kit';

import { argsort, mean, sum, zip } from '$lib/utils';

const RESULT_MARGIN_SECS = 120;
const MAX_RESULTS_PER_VIDEO = 8;
const SCORE_THRESHOLD = 0.5;

interface SearchResult {
  video_id: string;
  score: number;
  start: number;
  end: number;
  // captions_start: number;
  // captions_end: number;
}

interface VideoSearchResult {
  scores: number[];
  starts: number[];
  ends: number[];
  // captions_starts: number[];
  // captions_ends: number[];
}

interface VideoMetadata {
  videoId: string;
}

let VIDEOS: VideoMetadata[];

const aggregateResults = (results: SearchResult[]) => {
  let episodeResults = [];
  let clipResults = [];

  for (let result of results) {
    if (result.start === -1) {
      episodeResults.push(result);
    } else {
      clipResults.push(result);
    }
  }

  // episodes

  let episodeResultsByVideoId: { [videoId: string]: { scores: number[] } } = {};

  for (let { video_id: videoId, score } of episodeResults) {
    if (!episodeResultsByVideoId[videoId]) {
      episodeResultsByVideoId[videoId] = { scores: [score] };
    } else {
      episodeResultsByVideoId[videoId].scores.push(score);
    }
  }

  episodeResults = Object.entries(episodeResultsByVideoId).map(
    ([videoId, result]) => ({ ...result, ...{ videoId: videoId } })
  );

  // average scores
  episodeResults = episodeResults.map((result) => ({
    ...result,
    score: mean(result.scores)
  }));

  // filter episodes
  episodeResults = episodeResults.filter(
    ({ score, scores }) => score > 0.5 || scores.length > 3
  );

  // sort by avg score
  episodeResults = episodeResults.sort(
    ({ score: s1 }, { score: s2 }) => s2 - s1
  );

  // add in the video metadata
  episodeResults = episodeResults.map((result) => ({
    ...result,
    ...VIDEOS[result.videoId]
  }));

  // clips

  let clipResultsByVideoId: { [videoId: string]: VideoSearchResult } = {};
  for (let { video_id: videoId, score, start, end } of clipResults) {
    if (score > SCORE_THRESHOLD) {
      if (!clipResultsByVideoId[videoId]) {
        clipResultsByVideoId[videoId] = {
          scores: [score],
          starts: [start],
          ends: [end]
        };
      } else {
        clipResultsByVideoId[videoId].scores.push(score);
        clipResultsByVideoId[videoId].starts.push(start);
        clipResultsByVideoId[videoId].ends.push(end);
      }
    }
  }

  clipResults = Object.entries(clipResultsByVideoId).map(
    ([videoId, result]) => ({ ...result, ...{ videoId: videoId } })
  );

  clipResults = clipResults.map((result) => ({
    ...result,
    score:
      0.333 * sum(result.scores) +
      0.333 * mean(result.scores) +
      0.333 * result.scores.length
  }));

  // sort by video score
  clipResults = clipResults.sort(({ score: s1 }, { score: s2 }) => s2 - s1);

  // order clips by score
  clipResults = clipResults.map((result) => {
    const order = argsort(result.scores.map((s) => -s));
    for (const key of ['scores', 'starts', 'ends']) {
      result[key] = order.map((i) => result[key][i]);
    }
    return result;
  });

  // remove overlapping results
  clipResults = clipResults.map((result) => {
    const keep = zip([result.starts, result.ends]).reduce(
      ({ indices, ends }, [start, end], index) => {
        if (
          indices.length === 0 ||
          start > ends[ends.length - 1] + RESULT_MARGIN_SECS
        ) {
          indices.push(index);
          ends.push(end);
        }
        return { indices: indices, ends: ends };
      },
      { indices: [], ends: [] }
    );
    for (const key of ['scores', 'starts', 'ends']) {
      result[key] = keep.indices.map((i) => result[key][i]);
    }
    return result;
  });

  // add in video metadata
  clipResults = clipResults.map((result) => {
    return { ...result, ...VIDEOS[result.videoId] };
  });

  // keep top videos
  clipResults = clipResults.slice(0, 16);

  return [episodeResults, clipResults];

  // // only keep videos with >1 result
  // .filter((videoResult) => videoResult.scores.length > 1)
  // // keep top videos
  // .slice(0, 32)
  // const n = Math.min(MAX_RESULTS_PER_VIDEO, result.scores.length);
  // .slice(0, n);

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
    let [episodeResults, clipResults] = aggregateResults(results);
    data.episodeResults = episodeResults;
    data.clipResults = clipResults;
    return data;
  }
};
