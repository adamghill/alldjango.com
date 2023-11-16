/*
dork.js | https://github.com/adamghill
MIT
*/

function _get_el(el) {
  if (typeof el == "string") {
    el = $(el);
  }

  return el;
}

/**
 * Query for a particular element in a document. Classic.
 * @param {String} query - CSS-like query for an `Element`.
 * @returns The first `Element` found for the query.
 */
function $(query) {
  return document.querySelector(query);
}

/**
 * Adds an event listener to a particular `Element`.
 * @param {String|Element} el - `Element` to listen to.
 * @param {*} eventName - Event to listen to, e.g. "click", "mouseover", etc.
 * @param {*} fn - Function to run when a particular event is fired.
 */
function listen(el, eventName, fn, preventDefault) {
  el = _get_el(el);

  el.addEventListener(eventName, (event) => {
    if (preventDefault === true) {
      event.preventDefault();
    }

    return fn(event);
  });
}

/**
 * Runs a function after the DOM content has been loaded.
 * @param {Function} fn - The function to run after the DOM content has been loaded.
 */
function onload(fn) {
  listen(document, "DOMContentLoaded", fn);
}

/**
 * Get the value of an `Element`.
 * @param {String} query - The query for the `Element` to get the value for.
 */
function value(query) {
  return $(query).value;
}

/**
 * Get the value of an `Element`.
 * @param {String|Element} el - `Element` to get the value for.
 */
function value(el) {
  el = _get_el(el);

  return el.value;
}

/**
 * Hide an `Element`.
 * @param {String|Element} el - The `Element` to hide.
 */
function hide(el) {
  el = _get_el(el);

  if (el) {
    el.style = "display: none";
  }
}

/**
 * Show an `Element`.
 * @param {String|Element} el - The `Element` to show.
 */
function show(el) {
  el = _get_el(el);

  if (el) {
    el.style = "display: inline";
  }
}

/**
 * Writes to the console.
 * @param {String} s - The message to write to the console.
 */
function p(s) {
  console.log(s);
}
