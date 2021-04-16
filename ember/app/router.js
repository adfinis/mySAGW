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
  this.route("notfound", { path: "/*path" });

  this.route("protected", { path: "/" }, function () {
    // Index
    // Probably because of the namespace reset,
    // we need to manually specify the index route.
    this.route("index", { resetNamespace, path: "/" });

    // Engines
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

    // Caluma
    this.route("cases", { resetNamespace }, function () {
      this.route("detail", { path: "/:id" }, function () {
        this.route("edit");
      });
      this.route("new");
    });

    // API
    this.route("identities", { resetNamespace }, function () {
      this.route("add");
      this.route("edit", { path: "/edit/:identity" });
    });
    this.route("interests", { resetNamespace }, function () {
      this.route("add");
      this.route("edit", { path: "/edit/:category" });
    });
    this.route("membership-roles", { resetNamespace }, function () {
      this.route("add");
      this.route("edit", { path: "/edit/:role" });
    });
    this.route("profile", { resetNamespace });
  });
});
