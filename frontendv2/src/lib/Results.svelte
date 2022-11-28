<script>
  export let form;
</script>

{#if form?.results}
  {#each form.results.slice(0, 4) as { video_id: videoId, score }}
    <p>{videoId}, {score}</p>
  {/each}
{/if}
