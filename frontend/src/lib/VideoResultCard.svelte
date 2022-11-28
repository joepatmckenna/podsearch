<script>
  import { Card, CardTitle } from "sveltestrap";

  import { zip } from "./utils";
  import ClipCarousel from "./ClipCarousel.svelte";

  export let videoResult;

  let guest, title, subtitle;

  $: {
    let [guestAndTitle, _subtitle] = videoResult.title.split("|");
    let [_guest, _title] = guestAndTitle.split(":");
    guest = _guest;
    title = _title;
    subtitle = _subtitle;
  }
</script>

<div class="card m-2">
  <div class="row">
    <div
      class="col-3 d-flex align-items-center justify-content-center"
      style="background-color:lightblue;"
    >
      <a href={`https://www.youtube.com/watch?v=${videoResult.videoId}`}>
        <img
          width="100%;"
          alt={videoResult.title}
          src={videoResult.thumbnails.default.url}
        /></a
      >
    </div>
    <div class="col-9" style="background-color:beige;">
      <div class="card-body">
        <h1 class="card-title" style="background-color:yellow;">{guest}</h1>
        <p class="card-subtitle">{title}</p>
        <p class="card-subtitle text-muted">{subtitle}</p>
      </div>
    </div>
  </div>

  <div class="row">
    <ClipCarousel {videoResult} />
  </div>
</div>

<style>
  .card-body p {
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
</style>
