import Model, { attr, belongsTo } from "@ember-data/model";

export default class CaseModel extends Model {
  @attr caseId;
  @attr email;
  @belongsTo("identity") identity;
}
