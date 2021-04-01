import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

export default class IdentitiesEditController extends Controller {
  @tracked _isOrganistaion;
  get isOrganisation() {
    return this._isOrganistaion ?? this.model.isOrganisation;
  }
  set isOrganisation(value) {
    this._isOrganistaion = value;
  }

  @action onOrganisationUpdate(isOrganisation) {
    this.isOrganisation = isOrganisation;
  }
}
