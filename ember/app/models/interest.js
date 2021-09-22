import { attr, belongsTo } from "@ember-data/model";
import { localizedAttr, LocalizedModel } from "ember-localized-model";

export default class InterestModel extends LocalizedModel {
  @localizedAttr title;
  @attr description;
  @belongsTo("interest-category") category;
  @attr archived;
}
