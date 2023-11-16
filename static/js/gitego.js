(function _() {
  onload(() => {
    const lookupEl = $("#lookup");

    listen(
      lookup,
      "click",
      () => {
        const username = value("#username");

        if (username) {
          hide(lookupEl);
          hide("#user");
          hide("#repo");
          hide("#intro");
          show("#spinner");
          show("#loading");

          window.location.search = `?username=${username}`;
        } else {
          alert("Missing username?");
        }
      },
      true
    );

    listen(
      "#clear",
      "click",
      () => {
        window.location.search = "";
      },
      true
    );
  });
})();
