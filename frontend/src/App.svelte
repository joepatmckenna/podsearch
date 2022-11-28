<script>
  import { onMount } from "svelte";

  import {
    Button,
    Container,
    Icon,
    Input,
    InputGroup,
    Spinner,
  } from "sveltestrap";

  import VideoResultCard from "./lib/VideoResultCard.svelte";

  const BACKEND_URL = "https://search-ouy3lqvqqq-uc.a.run.app";
  // const BACKEND_URL = "http://0.0.0.0:8080";

  import VIDEOS from "../../assets/frontend/videos.json";
  // import VIDEOS from "../videos.json";
  const RESULT_MARGIN_SECS = 300;

  let backendOk = false;

  let query = "";
  let results = [];
  let videoResults = [];

  $: {
    videoResults = aggregateResultsByVideo(results);
  }

  onMount(async () => {
    let response = await fetch(BACKEND_URL);
    let data = await response.json();
    backendOk = data.status === "ok";
  });

  const search = async () => {
    const res = await fetch(
      BACKEND_URL + "/search?" + new URLSearchParams({ query: query })
    );
    const response = await res.json();
    query = response.query;
    results = response.results;
  };

  export const aggregateResultsByVideo = (results) => {
    let _videoResults = Object.entries(
      // reformat videoId -> { (aggregated values) }
      results.reduce(
        (
          resultsByVideoId,
          { video_id: videoId, score, start, end, captions_start, captions_end }
        ) => {
          let videoResult = resultsByVideoId[videoId] || {
            score: 0.0,
            scores: [],
            starts: [],
            ends: [],
            captions_starts: [],
            captions_ends: [],
          };
          videoResult.score += score;
          videoResult.scores.push(score);
          videoResult.starts.push(start);
          videoResult.ends.push(end);
          videoResult.captions_starts.push(captions_start);
          videoResult.captions_ends.push(captions_end);
          resultsByVideoId[videoId] = videoResult;
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
      .sort(({ score: s1 }, { score: s2 }) => s2 - s1)
      // keep top videos
      .slice(0, 4)
      // sort timestamps and caption indices
      .map((videoResult) => {
        let order = argsort(videoResult.ends);
        for (let key of [
          "scores",
          "starts",
          "ends",
          "captions_starts",
          "captions_ends",
        ]) {
          videoResult[key] = order.map((i) => videoResult[key][i]);
        }
        return videoResult;
      })
      // remove intersecting intervals
      .map((videoResult) => {
        let keep = zip([videoResult.starts, videoResult.ends]).reduce(
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
        for (let key of [
          "scores",
          "starts",
          "ends",
          "captions_starts",
          "captions_ends",
        ]) {
          videoResult[key] = keep.indices.map((i) => videoResult[key][i]);
        }
        return videoResult;
      })
      // add in video metadata
      .map((videoResult) => {
        return { ...videoResult, ...VIDEOS[videoResult.videoId] };
      });
    // // add in captions
    // .map((videoResult) => {
    //   videoResult.captions = zip([
    //     videoResult.captions_starts,
    //     videoResult.captions_ends,
    //   ]).map(([captions_start, captions_end]) => {
    //     return (CAPTIONS[videoResult.videoId] || [])
    //       .slice(captions_start, captions_end + 1)
    //       .join(" ");
    //   });
    //   return videoResult;
    // });

    console.log(_videoResults);
    return _videoResults;
  };
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.0/font/bootstrap-icons.css"
  />
</svelte:head>

<main>
  <Container style="background-color:aquamarine; max-width:600px;">
    <Container fluid>
      <InputGroup>
        <Input
          type="search"
          name="search"
          id="exampleSearch"
          placeholder="Search Lex Fridman podcast episodes"
          bind:value={query}
        />
        <Button size="sm" on:click={search} disabled={!(backendOk && query)}>
          <Icon name="search" />
        </Button>
      </InputGroup>
    </Container>

    {#if backendOk}
      {#each videoResults as videoResult}
        <VideoResultCard {videoResult} />
      {/each}
    {:else}
      <Spinner color="dark" type="border" />
    {/if}
  </Container>
</main>

<style>
</style>
