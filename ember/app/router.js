import EmberRouter from "@ember/routing/router";

import config from "./config/environment";

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

//eslint-disable-next-line array-callback-return
Router.map(function () {
  this.mount("ember-emeis", { as: "emeis", path: "/emeis" });
  this.mount("ember-alexandria", { as: "alexandria", path: "/alexandria" });
  this.mount("ember-caluma", { as: "form-builder", path: "/form-builder" });
  this.route("cases", { path: "/" }, function () {
    this.route("detail", { path: "/:id" }, function () {
      this.route("edit");
    });
    this.route("new");
  });
});
