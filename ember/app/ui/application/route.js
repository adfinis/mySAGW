import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";

export default class ApplicationRoute extends Route.extend(
  OIDCApplicationRouteMixin
) {
  @service intl;
  @service calumaOptions;

  beforeModel(...args) {
    super.beforeModel(...args);
    this.intl.setLocale(["en"]);

    this.calumaOptions.registerComponentOverride({
      label: "Circulation",
      component: "circulation",
      type: "CheckboxQuestion",
    });
  }
}
