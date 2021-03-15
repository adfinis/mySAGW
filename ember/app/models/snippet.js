import { attr } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class SnippetModel extends LocalizedModel {
  @attr title;
  @localizedAttr body;
  @attr archived;
}
