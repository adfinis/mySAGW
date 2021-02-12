import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class InterestCategoryModel extends LocalizedModel {
  @localizedAttr title;
  @localizedAttr description;
  @hasMany interests;
  @attr archived;
}
