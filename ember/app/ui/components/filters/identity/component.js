import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

import { arrayFromString } from "mysagw/utils/query-params";

export default class FiltersIdentityComponent extends Component {
  @service store;
  @service notification;

  get selected() {
    const selected =
      typeof this.args.selected === "string"
        ? arrayFromString(this.args.selected ?? "")
        : this.args.selected;

    return this.identityOptions.value?.filter((option) =>
      selected.includes(option.idpId),
    );
  }

  identityOptions = trackedFunction(this, async () => {
    if (!this.args.selected.length) {
      return [];
    }

    let idpIds = this.args.selected;
    if (typeof this.args.selected !== "string") {
      idpIds = this.args.selected.join(",");
    }

    try {
      return (
        await this.store.query(
          "identity",
          {
            filter: {
              idpIds,
            },
          },
          { adapterOptions: { customEndpoint: "public-identities" } },
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
        { adapterOptions: { customEndpoint: "public-identities" } },
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
