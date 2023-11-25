(function _() {
  onload(() => {
    const lookupEl = $("#lookup");

    listen(
      lookup,
      "click",
      () => {
        const usernameEl = $("#username");
        const username = value(usernameEl);

        if (username) {
          usernameEl.disabled = true;
          hide(lookupEl);
          hide("#user");
          hide("#repo");
          hide("#lookup");
          hide("#clear");
          hide("#intro");
          show("#loading");
          show("#spinner");

          window.location = `/gitego/user/${username}`;
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
        window.location = "/gitego/";
      },
      true
    );

    $$(".lookup").forEach((el) => {
      listen(
        el,
        "click",
        (event, el) => {
          const lookupUsername = data(el, "username");
          window.location = `/gitego/user/${lookupUsername}`;
        },
        true
      );
    });
  });
})();
