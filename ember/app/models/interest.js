import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class InterestModel extends LocalizedModel {
  @attr title;
  @attr description;
  @belongsTo("interest-category") category;
  @attr archived;
}
