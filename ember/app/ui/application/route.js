import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ApplicationRoute extends Route {
  @service intl;
  @service calumaOptions;
  @service session;

  beforeModel(...args) {
    super.beforeModel(...args);

    this.session.setup();

    const locale = localStorage.getItem("locale") ?? "en";
    this.intl.setLocale([locale]);

    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button",
      component: "submit-button",
      type: "StaticQuestion",
    });
  }
}
