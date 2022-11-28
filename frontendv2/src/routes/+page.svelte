<script>
  import SearchBar from '$lib/SearchBar.svelte';
  // import Results from '$lib/Results.svelte';
  import ResultsByEpisode from '$lib/ResultsByEpisode.svelte';

  export let form;
</script>

<svelte:head>
  <!-- Bootstrap -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.0/font/bootstrap-icons.css"
  />

  <!-- Google Analytics -->
  <script
    async
    src="https://www.googletagmanager.com/gtag/js?id=G-BL0GNYJNBY"
  ></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    gtag('js', new Date());
    gtag('config', 'G-BL0GNYJNBY');
  </script>

  <!-- Google AdSense -->
  <script
    async
    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6007831715390930"
    crossorigin="anonymous"
  ></script>
</svelte:head>

<div class="app-container container-sm">
  <SearchBar {form} />
  <!-- <Results {form} /> -->
  <ResultsByEpisode {form} />
</div>

<style>
  .app-container {
    max-width: 590px;
    min-height: 100vh;
  }
</style>
