<script>
  export let form;
  let query = form?.query || '';
</script>

<div class="container-fluid p-3">
  <!-- <label for="searchInput" class="form-label"
    >Search the Lex Fridman podcast:</label
  > -->

  <form method="POST">
    <div class="input-group">
      <input
        type="search"
        id="searchInput"
        class="search-input form-control width100"
        name="query"
        bind:value={query}
      />
      <button class="search-button btn border" disabled={!query}>
        <span class="bi-search" />
      </button>
    </div>
  </form>
</div>

<style>
  /* .form-label {
    font-weight: bold;
  } */

  input:focus {
    outline: none;
    outline-width: 0;
  }

  .search-input {
    background-color: rgba(0, 0, 0, 0);
    caret-color: white;
    color: white;
    border-radius: 32px;
    border-color: white;
    border-width: 1px;
  }

  [type='search']::-webkit-search-cancel-button {
    -webkit-filter: brightness(0) invert(1);
    filter: brightness(0) invert(1);
  }

  .search-button {
    border-radius: 32px;
    color: white;
    background-color: rgba(0, 0, 0, 0);
    border-color: white;
    border-width: 1px;
  }
</style>
