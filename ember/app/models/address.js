import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class IdentityModel extends LocalizedModel {
  @belongsTo("identity") identity;
  @attr addressAddition;
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
}
