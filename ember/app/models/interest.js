import { attr, belongsTo } from "@ember-data/model";
import { localizedAttr, LocalizedModel } from "ember-localized-model";

export default class InterestModel extends LocalizedModel {
  @localizedAttr title;
  @attr description;
  @attr archived;
  @belongsTo("interest-category", { inverse: "interests", async: true })
  category;
}
