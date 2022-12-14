<script>
  import {sum} from "$lib/utils.ts";
  import InfiniteScroll from "svelte-infinite-scroll";

  import { onMount } from 'svelte';

  let Carousel;
  onMount(async () => {
    const module = await import('svelte-carousel');
    Carousel = module.default;
  });

  import ClipCarousel from './ClipCarousel.svelte';
  const resultsPerPage = 4;

  let episodeResults;
  let clipResults;

  // .slice(pageIndex * resultsPerPage, pageIndex * resultsPerPage + resultsPerPage)

  export let form;

  $: episodeResults = form?.episodeResults && form.episodeResults;
  $: clipResults = form?.clipResults && form.clipResults.slice(0, pageIndex * resultsPerPage + resultsPerPage);

  // $: numPages = Math.floor((clipResults?.length || 0) / resultsPerPage);

  let pageIndex = 0;
  let activeCardIndex = null;

  // const onKeyDown = (e) => {
  //   if (e.target.id === 'searchInput') return;
  //   if (activeCardIndex === null) {
  //     if (e.keyCode === 37 && pageIndex > 0) {
  //       pageIndex -= 1;
  //     } else if (e.keyCode == 39 && pageIndex < numPages - 1) {
  //       pageIndex += 1;
  //     }
  //   } else if (e.keyCode == 27) {
  //     activeCardIndex = null;
  //   }
  // };
</script>

<!-- <svelte:window on:keydown={onKeyDown} /> -->

{#if episodeResults && clipResults}
{#if clipResults.length === 0 && episodeResults.length === 0}
  <div class="container-fluid py-2">
    <div class="mx-2">
      <p class="text-left" style="font-style:italic;">
        Didn't find any relevant results.
      </p>
    </div>
  </div>
{:else}
  <div class="container-fluid py-2" id="results-container">
    {#if episodeResults.length > 0}
      <h1>Episodes</h1>
      <div
        class="card my-3 p-2"
      >
        <div class="row">
          <svelte:component this={Carousel}
            particlesToShow={3}
            particlesToScroll={3}
            infinite={false}
          >
          {#each episodeResults as episodeResult, index}
          <div class="col-3 p-2">
            <a href={`https://www.youtube.com/watch?v=${episodeResult.videoId}`} target="_blank" rel="noreferrer"><img
              style="border-radius:8px;"
              alt={episodeResult.title}
              src={episodeResult.thumbnails.default.url}
            />
          </a>
          </div>
          {/each}
          </svelte:component>
      </div>
    </div>
      {/if}

      {#if clipResults.length > 0}
      <h1>Clips</h1>
      {#each clipResults as clipResult, index}
        <div
          class="card my-3 p-2"
          style={activeCardIndex == index
            ? 'box-shadow: 0px 0px 6px #fff;'
            : 'box-shadow: 0px 0px 4px #000;'}
        >
          <div class="container-fluid">
            <div class="row" on:mousedown={() => (activeCardIndex = activeCardIndex === index ? null : index)}>
              <div
                class="col-3 p-0 d-flex align-items-center justify-content-center"
              >
                <img
                  style="border-radius:8px; width:100%;"
                  alt={clipResult.title}
                  src={clipResult.thumbnails.default.url}
                />
                </div>
              <div class="col-9">
                <div class="card-body">
                  <h1 class="card-title">
                    {clipResult.title.split('|')[0].split(':')[0]}
                  </h1>
                  <h2 class="card-subtitle my-1">
                    {clipResult.title.split('|')[0].split(':')[1] || ''}
                  </h2>
                  <h2 class="card-subtitle text-muted my-1">
                    {clipResult.title.split('|')[1]}
                  </h2>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="card-footer" on:mousedown={() => (activeCardIndex = activeCardIndex = index)}>
                <ClipCarousel
                  isExpanded={activeCardIndex === index}
                  clipResult={clipResult}
                />
              </div>
            </div>
          </div>
        </div>
      {/each}
      {/if}

      <!-- <ins
        class="adsbygoogle"
        style="display:block"
        data-ad-format="fluid"
        data-ad-layout-key="-hs-l+4r-43-6d"
        data-ad-client="ca-pub-6007831715390930"
        data-ad-slot="3614473693"
      />
      <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
      </script> -->

      <!-- <div class="p-2 text-center page-nav">
        {#each [...Array(Math.min(8, numPages)).keys()] as i}
          <button
            type="button"
            class="btn btn-dark mx-1 mt-2 mb-5"
            style={i === pageIndex
              ? 'background-color: #ccc; color: black;'
              : ''}
            on:click={() => {
              pageIndex = i;
              activeCardIndex = null;
            }}
          >
            {i + 1}
          </button>
        {/each}
      </div>
     -->
  </div>

  {/if}
{/if}

<InfiniteScroll 
  window={true}
  on:loadMore={() => {
    console.log('load more');
    pageIndex++;
  }} 
/>

<style>
  h1 {
    font-size: 16px;
    font-weight: bold;
  }

  .card {
    background: rgba(0, 0, 0, 0.25);
    border-radius: 16px;
    border-width: 1px;
    border-color: rgba(0, 0, 0, 0.5);
  }

  .card-body h1,
  h2 {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .card-title {
    font-size: 16px;
  }

  .card-subtitle {
    font-size: 14px;
  }

  .page-nav {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .page-nav button {
    border-radius: 40%;
    background-color: rgba(0, 0, 0, 0.5);
  }
</style>
