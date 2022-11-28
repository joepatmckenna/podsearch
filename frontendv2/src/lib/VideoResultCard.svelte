<!-- <script>
  import ClipCarousel from './ClipCarousel.svelte';

  export let videoResult;
  export let isActive;

  $: [guestAndTitle, subtitle] = videoResult.title.split('|');
  $: [guest, title] = guestAndTitle.split(':');
</script>

<div
  class="card my-3"
  style={isActive
    ? 'box-shadow: 0px 0px 4px #fff;'
    : 'box-shadow: 0px 0px 4px black;'}
>
  <div class="container-fluid">
    <div class="row" on:mousedown={() => (isActive = !isActive)}>
      <div class="col-3 d-flex align-items-center justify-content-center">
        <img
          width="100%;"
          alt={videoResult.title}
          src={videoResult.thumbnails.default.url}
        />
      </div>
      <div class="col-9">
        <div class="card-body">
          <h1 class="card-title">{guest}</h1>
          <p class="card-subtitle">{title}</p>
          <p class="card-subtitle text-muted">{subtitle}</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card-footer" style={isActive ? '' : 'display:none'}>
        <ClipCarousel isVisible={isActive} {videoResult} />
      </div>
    </div>
  </div>
</div>

<style>
  .card {
    background: rgba(0, 0, 0, 0.3);
    border-width: 2px;
    border-color: #black;
  }

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
</style> -->
