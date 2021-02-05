import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class InterestModel extends LocalizedModel {
  @localizedAttr title;
  @localizedAttr description;
  @belongsTo("interest-category", { inverse: null }) category;
  @attr archived;
}
