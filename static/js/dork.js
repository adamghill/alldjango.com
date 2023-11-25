/*
dork.js | https://github.com/adamghill
The most important JavaScript framework ever created.
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
 * Query for all elements in a document.
 * @param {String} query - CSS-like query for `Element`s.
 * @returns All `Element`s found for the query.
 */
function $$(query) {
  return document.querySelectorAll(query);
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

    return fn(event, el);
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
 * Get the data value of an `Element`.
 * @param {String|Element} el - `Element` to get the value for.
 * @param {String} data - Attribute to get the data from.
 */
function data(el, data) {
  el = _get_el(el);

  p(el.dataset[data]);

  return el.data;
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
function print(s) {
  console.log(s);
}
