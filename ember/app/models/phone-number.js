import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class PhoneNumberModel extends LocalizedModel {
  @belongsTo("identity") identity;
  @attr phone;
  @localizedAttr description;
  @attr default;
}
