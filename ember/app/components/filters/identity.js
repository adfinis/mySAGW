import { action } from "@ember/object";
import { service } from "@ember/service";
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
      selected.includes(option.id),
    );
  }

  identityOptions = trackedFunction(this, async () => {
    if (!this.args.selected.length) {
      return [];
    }

    let ids = this.args.selected;
    if (typeof this.args.selected !== "string") {
      ids = this.args.selected.join(",");
    }

    try {
      return Array.from(
        ...(await this.store.query(
          "identity",
          {
            filter: {
              ids,
            },
          },
          { adapterOptions: { customEndpoint: "public-identities" } },
        )),
      );
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

      return Array.from(
        yield this.store.query(
          "identity",
          {
            filter: {
              search,
              isOrganisation: false,
            },
          },
          { adapterOptions: { customEndpoint: "public-identities" } },
        ),
      );
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
