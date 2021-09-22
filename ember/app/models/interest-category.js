import { attr, hasMany } from "@ember-data/model";
import { localizedAttr, LocalizedModel } from "ember-localized-model";

export default class InterestCategoryModel extends LocalizedModel {
  @localizedAttr title;
  @attr description;
  @hasMany interests;
  @attr archived;
  @attr public;
}
