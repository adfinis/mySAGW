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
    this.route("form", { resetNamespace }, function () {
      this.route("configuration");

      this.mount("@projectcaluma/ember-form-builder", {
        as: "form-builder",
        path: "/builder",
        resetNamespace,
      });
    });
    /* 
    this.mount("@projectcaluma/ember-analytics", {
      as: "analytics",
      path: "/analytics",
      resetNamespace,
    });
    */

    // Caluma
    this.route("cases", { resetNamespace }, function () {
      this.route("detail", { path: "/:case_id" }, function () {
        this.route("edit");
        this.route("work-items", function () {
          this.route("edit", { path: "/:work_item_id" }, function () {
            this.route("form");
          });
        });
        this.route("circulation");
      });
      this.route("new");
    });
    this.route("work-items", { resetNamespace });
    this.route("form-configuration", { resetNamespace });

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
    this.route("profile", { resetNamespace }, function () {
      this.route("edit", { path: "/edit/:identity" });
    });
    this.route("snippets", { resetNamespace }, function () {
      this.route("add");
      this.route("edit", { path: "/edit/:snippet" });
    });
  });
});
