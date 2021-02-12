import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class PhoneNumberModel extends LocalizedModel {
  @belongsTo("identity") identity;
  @attr phone;
  @attr description;
  @attr default;
}
