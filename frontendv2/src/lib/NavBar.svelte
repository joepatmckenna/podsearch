<script>
    import logo from '$lib/assets/logo.png';
</script>

<!-- navbar-expand-sm -->
<nav class="navbar">

  <!-- <div 
    class="navbar-toggler" 
    data-toggle="collapse" 
    data-target="#navbarSupportedContent" 
    aria-controls="navbarSupportedContent" 
    aria-expanded="false" 
  >
    <img class="logo mx-2" alt="Portrait of Lex" src={logo} />
  </div>  -->

  <!-- collapse navbar-collapse -->
  <div class="mx-4" id="navbarSupportedContent">
    <span><a href="https://lexfridman.com/podcast/">Lex Fridman Podcast</a> search engine</span>    
  </div>

  <div class="youtube-link mx-4">
    <a href="https://www.youtube.com/playlist?list=PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4" ><span class="bi-youtube" /></a>
  </div>

</nav>

<style>

  .navbar {
    background-color: rgb(0,0,0,0.25);
  }
  a {
    color: #fff;
    text-decoration: none;
  }

  a:hover {
    color: #aaa;
  }

  /* .logo {
    width: 32px;
    background-color: #aaa;
    border-radius: 50%;
  } */
  
  .bi-youtube {
    color: red;
    font-size: 1.5em;
  }

</style>
