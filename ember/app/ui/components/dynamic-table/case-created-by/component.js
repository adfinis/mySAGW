import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class CaseCreatedBy extends Component {
  @service store;

  get createdBy() {
    return this.store.peekAll("identity").findBy("idpId", this.args.value);
  }
}
