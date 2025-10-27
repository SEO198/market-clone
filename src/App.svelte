<script>
  import Router from "svelte-spa-router";
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import "./css/style.css";

  const routes = {
    "/": Main,
    "/Login": Login,
    "/Signup": Signup,
    "/Write": Write,
    "*": NotFound,
  };
</script>

<Router {routes}></Router>
<main></main>

<style>
</style>
