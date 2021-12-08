import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import moment from "moment";

export default class ApplicationRoute extends Route.extend(
  OIDCApplicationRouteMixin
) {
  @service intl;
  @service calumaOptions;

  beforeModel(...args) {
    super.beforeModel(...args);
    const locale = window.localStorage.getItem("locale") ?? "en";
    this.intl.setLocale([locale]);
    moment.locale(locale);

    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button",
      component: "submit-button",
      type: "StaticQuestion",
    });
  }
}
