import EmberRouter from "@ember/routing/router";

import config from "./config/environment";

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

const resetNamespace = true;

//eslint-disable-next-line array-callback-return
Router.map(function () {
  this.route("login");

  this.route("protected", { path: "/" }, function () {
    this.mount("ember-emeis", {
      as: "emeis",
      path: "/emeis",
      resetNamespace,
    });
    this.mount("ember-alexandria", {
      as: "alexandria",
      path: "/alexandria",
      resetNamespace,
    });
    this.mount("ember-caluma", {
      as: "form-builder",
      path: "/form-builder",
      resetNamespace,
    });
  });
});
