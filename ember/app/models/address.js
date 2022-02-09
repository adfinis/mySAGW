import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class IdentityModel extends LocalizedModel {
  @belongsTo("identity") identity;
  @attr addressAddition1;
  @attr addressAddition2;
  @attr addressAddition3;
  @attr streetAndNumber;
  @attr poBox;
  @attr postcode;
  @attr town;
  @attr country;
  @localizedAttr description;
  @attr default;

  get label() {
    return [this.streetAndNumber, this.town].join(", ");
  }

  get countryName() {
    const locale = window.localStorage.getItem("locale") ?? "en";
    const countries = new Intl.DisplayNames([locale], { type: "region" });
    return countries.of(this.country);
  }
}
