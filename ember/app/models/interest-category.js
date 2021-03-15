import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class InterestCategoryModel extends LocalizedModel {
  @attr title;
  @attr description;
  @hasMany interests;
  @attr archived;
}
