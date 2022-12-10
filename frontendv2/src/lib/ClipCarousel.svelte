<script>
  import { zip, argmax } from '$lib/utils';

  export let clipResult;
  export let isExpanded;

  $: maxIndex = clipResult.scores.length - 1;
  $: activeIndex = argmax(clipResult.scores);
  let lastActiveIndex = activeIndex;

  const getCarouselItemClass = (index) => {
    let c = 'carousel-item video-container'; // text-center
    if (index === activeIndex) c += ' active';
    return c;
  };

  const getDotStyle = (index) => {
    let s = `left: ${100 * (clipResult.starts[index] / lengthSeconds)}%;`;
    if (index === activeIndex) {
      s +=
        'height: 20px; width: 20px; transform: translate(-10px, -8px); box-shadow: 0px 0px 8px #fff;';
    }
    return s;
  };

  $: lengthSeconds = clipResult.lengthSeconds;

  $: carouselItemClasses = clipResult.scores.map((_, index) =>
    getCarouselItemClass(index)
  );
  $: dotStyles = clipResult.scores.map((_, index) => getDotStyle(index));

  $: {
    for (let i of [lastActiveIndex, activeIndex]) {
      carouselItemClasses[i] = getCarouselItemClass(i);
      dotStyles[i] = getDotStyle(i);
    }
    lastActiveIndex = activeIndex;
  }

  const onKeyDown = (e) => {
    if (!(e.target.id === 'searchInput') && isExpanded) {
      if (e.keyCode === 37 && activeIndex > 0) {
        activeIndex -= 1;
      } else if (e.keyCode == 39 && activeIndex < maxIndex) {
        activeIndex += 1;
      }
    }
  };

  const iframeSrc = (videoId, start, end) => {
    return (
      `https://www.youtube.com/embed/${videoId}?` +
      [
        `start=${start}`,
        `end=${end}`,
        'enablejsapi=1',
        'autoplay=1',
        'cc_load_policy=0',
        'controls=0',
        'disablekb=1',
        'fs=1',
        'iv_load_policy=3',
        'loop=1',
        'modestbranding=1',
        'rel=0'
      ].join('&')
    );
  };
</script>

<svelte:window on:keydown={onKeyDown} />

<div class="carousel slide">
  <!-- <div class="container">
  <div class="row">

  <div class="col-2" style="background-color:pink;">
  <button
    class="carousel-control-prev"
    type="button"
    disabled={activeIndex === 0}
    on:click={() => {
      if (activeIndex > 0) activeIndex -= 1;
    }}
  >
    <span class="carousel-control-prev-icon" aria-hidden="true" />
  </button>
  </div> -->

  <!-- <div class="col-8" style="background-color:yellow;"> -->
  <div class="carousel-inner" style={isExpanded ? '' : 'display:none'}>
    <div class="spinner-border spinner-container" role="status" />
    {#each zip([clipResult.starts, clipResult.ends]) as [start, end], index}
      <div class={carouselItemClasses[index]}>
        {#if isExpanded && activeIndex === index}
          <iframe
            title={`${clipResult.videoId}-${start}-${end}`}
            src={iframeSrc(clipResult.videoId, start, end)}
          />
        {/if}
      </div>
    {/each}
  </div>
  <!-- </div> -->

  <!-- <div class="col-2" style="background-color:green;">
  <button
    class="carousel-control-next"
    type="button"
    disabled={activeIndex === maxIndex}
    on:click={() => {
      if (activeIndex < maxIndex) activeIndex += 1;
    }}
  >
    <span class="carousel-control-next-icon" aria-hidden="true" />
  </button>
  </div> -->

  <!-- </div> -->
  <!-- </div> -->
</div>

<div class="py-2 mt-2">
  <div class="track">
    {#each clipResult.starts as start, index}
      <div
        on:mousedown={() => (activeIndex = index)}
        class="button dot"
        style={dotStyles[index]}
      />
    {/each}
  </div>
</div>

<style>
  .spinner-container {
    margin: auto;
    width: 20px;
    height: 20px;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  }

  .video-container {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
  }

  .video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .track {
    position: relative;
    width: 100%;
    height: 4px;
    border-radius: 2px;
    background-color: #999;
  }

  .dot {
    position: absolute;
    height: 12px;
    width: 12px;
    border-radius: 50%;
    background-color: #ddd;
    transform: translate(-6px, -4px);
  }

  .button:hover {
    box-shadow: 0px 0px 8px #fff;
  }
</style>
