<script>
  import { argmax, zip } from "./utils";

  export let videoResult;

  let maxIndex = videoResult.scores.length - 1;
  let activeIndex = argmax(videoResult.scores);
  let lastActiveIndex = activeIndex;

  const getCarouselItemClass = (index) => {
    let c = "carousel-item text-center";
    if (index === activeIndex) c += " active";
    return c;
  };

  const getDotStyle = (index) => {
    let s = "";
    let left = 100 * (videoResult.starts[index] / videoResult.lengthSeconds);
    s += `left: ${left}%;`;
    if (index === activeIndex) {
      s += "height: 16px;";
      s += "width: 16px;";
      s += "transform: translate(-8px, -6px);";
    }
    return s;
  };

  let carouselItemClasses = videoResult.scores.map((_, index) =>
    getCarouselItemClass(index)
  );
  let dotStyles = videoResult.scores.map((_, index) => getDotStyle(index));

  $: {
    for (let i of [lastActiveIndex, activeIndex]) {
      carouselItemClasses[i] = getCarouselItemClass(i);
      dotStyles[i] = getDotStyle(i);
    }
    lastActiveIndex = activeIndex;
  }
</script>

<div class="carousel slide" style="background-color:black;">
  <div class="carousel-inner">
    {#each zip([videoResult.starts, videoResult.ends]) as [start, end], index}
      <div class={carouselItemClasses[index]}>
        <h1 style="color:white;">
          {start}-{end}
        </h1>
      </div>
    {/each}
  </div>

  <button
    class="carousel-control-prev"
    type="button"
    disabled={activeIndex === 0}
    on:click={() => {
      if (activeIndex > 0) activeIndex -= 1;
      console.log(activeIndex);
    }}
  >
    <span class="carousel-control-prev-icon" aria-hidden="true" />
  </button>

  <button
    class="carousel-control-next"
    type="button"
    disabled={activeIndex === maxIndex}
    on:click={() => {
      if (activeIndex < maxIndex) activeIndex += 1;
      console.log(activeIndex);
    }}
  >
    <span class="carousel-control-next-icon" aria-hidden="true" />
  </button>
</div>

<div class="py-3" style="background-color: #333; border-radius: 24px;">
  <div class="track">
    {#each videoResult.starts as start, index}
      <div
        on:mousedown={() => (activeIndex = index)}
        class="button dot"
        style={dotStyles[index]}
      />
    {/each}
  </div>
</div>

<!-- 
<iframe
title={videoResult.title}
src={`https://www.youtube.com/embed/${videoResult.videoId}?` +
  new URLSearchParams({
    start: videoResult.starts[0],
    end: videoResult.ends[0],
    controls: "0",
    autoplay: "1",
    cc_load_policy: "0",
    disablekb: "1",
    fs: "0",
    iv_load_policy: "3",
    rel: "0",
    modestbranding: "1",
    loop: "1",
  })}
/> -->
<style>
  .track {
    position: relative;
    width: 100%;
    height: 4px;
    border-radius: 2px;
    background-color: #999;
  }

  .dot {
    position: absolute;
    height: 8px;
    width: 8px;
    border-radius: 50%;
    background-color: #ddd;
    transform: translate(-4px, -2px);
  }
</style>
