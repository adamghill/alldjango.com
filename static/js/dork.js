/*
dork.js | https://github.com/adamghill
MIT
*/

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
 * @param {Element} el - `Element` to listen to.
 * @param {*} eventName - Event to listen to, e.g. "click", "mouseover", etc.
 * @param {*} fn - Function to run when a particular event is fired.
 */
function listen(el, eventName, fn, preventDefault) {
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
 * Writes to the console.
 * @param {String} s - The message to write to the console.
 */
function p(s) {
  console.log(s);
}
