(function _() {
  onload(() => {
    const lookupEl = $("#lookup");

    listen(
      lookup,
      "click",
      () => {
        const username = value("#username");

        if (username) {
          lookupEl.style = "display: none";
          $("#spinner").style = "display: inline;";
          window.location.search = `?username=${username}`;
        } else {
          alert("Missing username?");
        }
      },
      true
    );
  });
})();
