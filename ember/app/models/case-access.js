import Model, { attr, belongsTo } from "@ember-data/model";

export default class CaseAccessModel extends Model {
  @attr caseId;
  @attr email;
  @belongsTo("identity", { inverse: null, async: false }) identity;

  get name() {
    return (
      this.identity.get("fullName") || this.email || this.identity.get("email")
    );
  }
}
