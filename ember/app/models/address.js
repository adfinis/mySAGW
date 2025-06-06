import { inject as service } from "@ember/service";
import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class AddressModel extends LocalizedModel {
  @service intl;

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
    return [
      this.addressAddition1,
      this.addressAddition2,
      this.addressAddition3,
      this.streetAndNumber,
      this.poBox,
      `${this.postcode} ${this.town}`,
      this.country ? this.countryName : "",
    ]
      .filter(Boolean)
      .join("\n");
  }

  get countryName() {
    const countries = new Intl.DisplayNames(this.intl.primaryLocale, {
      type: "region",
    });
    return countries.of(this.country);
  }
}
