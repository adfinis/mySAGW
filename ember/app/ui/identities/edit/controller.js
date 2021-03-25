import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

export default class IdentitiesEditController extends Controller {
  @tracked isOrganisation = false;

  @action onOrganisationUpdate(isOrganisation) {
    this.isOrganisation = isOrganisation;
  }
}
