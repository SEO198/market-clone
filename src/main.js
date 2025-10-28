import { mount } from "svelte";
import App from "./App.svelte";
import "../firebase-config.js";

mount(App, {
  target: document.getElementById("app"),
});
