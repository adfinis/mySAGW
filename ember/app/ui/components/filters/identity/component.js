import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { restartableTask, lastValue, timeout } from "ember-concurrency";

export default class FiltersIdentityComponent extends Component {
  @service store;
  @service notification;

  constructor(...args) {
    super(...args);
    this.searchIdentities.perform("", true);
  }

  get selectedIdentityOptions() {
    return this.searchedIdentites?.filter((i) =>
      this.args.selectedIdentities.includes(i.idpId)
    );
  }

  @lastValue("searchIdentities") searchedIdentites;
  @restartableTask
  *searchIdentities(identitySearch, initial = false) {
    yield timeout(500);

    try {
      const filter = {
        search: identitySearch,
        isOrganisation: false,
        has_idp_id: true,
      };

      if (initial && this.args.selectedIdentities.length) {
        filter.idpIds = this.args.selectedIdentities.join(",");
      }

      const identities = yield this.store.query(
        "identity",
        {
          filter,
          page: {
            number: 1,
            size: 20,
          },
        },
        { adapterOptions: { customEndpoint: "public-identities" } }
      );

      const cachedIdentites = yield this.store
        .peekAll("identity")
        .filter((identity) =>
          this.args.selectedIdentities.includes(identity.idpId)
        );

      return [...cachedIdentites.toArray(), ...identities.toArray()].uniqBy(
        "idpId"
      );
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action
  updateIdentitySearch(value) {
    this.searchIdentities.perform(value);
  }

  @action
  onChange(identities) {
    this.args.onChange(identities);
  }
}
