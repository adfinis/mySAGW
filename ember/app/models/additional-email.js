import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class AdditionalEmailModel extends LocalizedModel {
  @belongsTo("identity") identity;
  @attr email;
  @attr description;
}
