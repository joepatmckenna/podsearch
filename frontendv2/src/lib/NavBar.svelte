<script>
    import logo from '$lib/assets/logo.png';
</script>
  
<nav class="navbar navbar-expand-sm">

  <div class="navbar-brand">
    <img class="logo mx-2" alt="Portrait of Lex" src={logo} />
  </div>

  <div 
    class="navbar-toggler" 
    data-toggle="collapse" 
    data-target="#navbarSupportedContent" 
    aria-controls="navbarSupportedContent" 
    aria-expanded="false" 
  />

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <span>Lex Fridman Podcast search engine</span>    
  </div>

  <div class="youtube-link mx-4">
    <a href="https://www.youtube.com/playlist?list=PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4" ><span class="bi-youtube" /></a>
  </div>

</nav>

<style>

  .navbar {
    background-color: rgb(0,0,0,0.25);
  }
  
  .logo {
    width: 32px;
    background-color: #aaa;
    border-radius: 50%;
  }
  .bi-youtube {
    color: red;
    font-size: 1.5em;
  }

</style>
