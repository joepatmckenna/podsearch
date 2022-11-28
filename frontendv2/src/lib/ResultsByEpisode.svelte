<script>
  // import VideoResultCard from '$lib/VideoResultCard.svelte';
  import ClipCarousel from './ClipCarousel.svelte';
  const resultsPerPage = 4;

  export let form;
  $: videoResults = form?.videoResults && form.videoResults;
  $: numPages = Math.floor((videoResults?.length || 0) / resultsPerPage);

  let pageIndex = 0;
  let activeCardIndex = null;

  const onKeyDown = (e) => {
    if (e.target.id === 'searchInput') return;
    if (activeCardIndex === null) {
      if (e.keyCode === 37 && pageIndex > 0) {
        pageIndex -= 1;
      } else if (e.keyCode == 39 && pageIndex < numPages - 1) {
        pageIndex += 1;
      }
    } else if (e.keyCode == 27) {
      activeCardIndex = null;
    }
  };
</script>

<svelte:window on:keydown={onKeyDown} />

{#if videoResults}
  {#if videoResults.length === 0}
    <div class="container-fluid py-2">
      <div class="mx-2">
        <p class="text-left" style="font-style:italic;">
          Didn't find any relevant results.
        </p>
      </div>
    </div>
  {:else if videoResults.length > 0}
    <div class="container-fluid py-2">
      <!-- <h1>Episodes</h1> -->
      {#each videoResults.slice(pageIndex * resultsPerPage, pageIndex * resultsPerPage + resultsPerPage) as videoResult, index}
        <!-- <VideoResultCard isActive={index == activeCardIndex} {videoResult}/> -->
        <div
          class="card my-3 p-2"
          style={activeCardIndex == index
            ? 'box-shadow: 0px 0px 6px #fff;'
            : 'box-shadow: 0px 0px 4px black;'}
        >
          <div class="container-fluid">
            <div
              class="row"
              on:mousedown={() => {
                if (activeCardIndex == index) {
                  activeCardIndex = null;
                } else {
                  activeCardIndex = index;
                }
              }}
            >
              <div
                class="col-3 p-0 d-flex align-items-center justify-content-center"
              >
                <img
                  style="border-radius:8px; width:100%;"
                  alt={videoResult.title}
                  src={videoResult.thumbnails.default.url}
                />
              </div>
              <div class="col-9">
                <div class="card-body">
                  <h1 class="card-title">
                    {videoResult.title.split('|')[0].split(':')[0]}
                  </h1>
                  <h2 class="card-subtitle my-1">
                    {videoResult.title.split('|')[0].split(':')[1] || ''}
                  </h2>
                  <h2 class="card-subtitle text-muted my-1">
                    {videoResult.title.split('|')[1]}
                  </h2>
                </div>
              </div>
            </div>
            <div class="row">
              <div
                class="card-footer"
                style={activeCardIndex === index ? '' : 'display:none'}
              >
                <ClipCarousel
                  isExpanded={activeCardIndex === index}
                  {videoResult}
                />
              </div>
            </div>
          </div>
        </div>
      {/each}
      <ins
        class="adsbygoogle"
        style="display:block"
        data-ad-format="fluid"
        data-ad-layout-key="-hs-l+4r-43-6d"
        data-ad-client="ca-pub-6007831715390930"
        data-ad-slot="3614473693"
      />
      <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
      </script>

      <div class="p-2 text-center page-nav">
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
    </div>
  {/if}
{/if}

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
