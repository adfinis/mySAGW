import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import { arrayFromString } from "mysagw/utils/query-params";

export default class FiltersIdentityComponent extends Component {
  @service store;
  @service notification;

  get selected() {
    const selected = arrayFromString(this.args.selected ?? "");

    return this.identityOptions.value?.filter((option) =>
      selected.includes(option.idpId)
    );
  }

  identityOptions = trackedFunction(this, async () => {
    if (!this.args.selected) {
      return [];
    }

    try {
      await Promise.resolve();

      return (
        await this.store.query(
          "identity",
          {
            filter: {
              idpIds: this.args.selected,
            },
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
    this.args.onChange(value);
  }
}
