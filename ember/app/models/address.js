import { attr, belongsTo } from "@ember-data/model";
import { inject as service } from "@ember/service";
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
    return [this.streetAndNumber, this.town].join(", ");
  }

  get countryName() {
    const countries = new Intl.DisplayNames(this.intl.locale, {
      type: "region",
    });
    return countries.of(this.country);
  }
}
