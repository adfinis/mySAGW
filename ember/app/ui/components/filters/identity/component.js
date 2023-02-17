import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import {
  arrayFromString,
} from "mysagw/utils/query-params";
import { action } from "@ember/object";

export default class FiltersIdentityComponent extends Component {
  @service store;
  @service notification;

  @tracked selection = this.selectedIdentityOptions;

  get selectedIdentities() {
    return arrayFromString(this.args.selectedIdentities ?? "");
  }

  get selectedIdentityOptions() {
    return this.identityOptions.value?.filter((i) =>
      this.selectedIdentities.includes(i.idpId)
    );
  }

  identityOptions = trackedFunction(this, async () => {
    if (!this.selectedIdentities.length) {
      return [];
    }

    try {
      await Promise.resolve();

      return (
        await this.store.query(
          "identity",
          {
            filter: { idpIds: this.selectedIdentities.join(",") },
          },
          { adapterOptions: { customEndpoint: "public-identities" } }
        )
      ).toArray();
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  });

  @restartableTask
  *search(search) {
    yield timeout(500);

    if (!search) {
      return [];
    }

    try {
      yield Promise.resolve();

      return (yield this.store.query(
        "identity",
        {
          filter: {
            search,
            isOrganisation: false,
            has_idp_id: true,
          },
        },
        { adapterOptions: { customEndpoint: "public-identities" } }
      )).toArray();
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action
  setSelection(value) {
    this.selection = value;
    this.args.onChange(value);
  }
}
