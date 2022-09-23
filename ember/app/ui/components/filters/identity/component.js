import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

export default class FiltersIdentityComponent extends Component {
  @service store;
  @service notification;

  get selectedIdentityOptions() {
    return this.selectedIdentities.value?.filter((i) =>
      this.args.selectedIdentities.includes(i.idpId)
    );
  }

  selectedIdentities = trackedFunction(this, async () => {
    if (!this.args.selectedIdentities.length) {
      return [];
    }

    try {
      await Promise.resolve();

      return (
        await this.store.query(
          "identity",
          {
            filter: { idpIds: this.args.selectedIdentities.join(",") },
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
}
