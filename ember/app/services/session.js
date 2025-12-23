import { service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import Session from "ember-simple-auth-oidc/services/session";
import { task as trackedTask } from "reactiveweb/ember-concurrency";

import ENV from "mysagw/config/environment";

export default class CustomSession extends Session {
  @service store;
  @service router;

  currentIdentity = trackedTask(this, this.fetchCurrentIdentity, () => [
    this.isAuthenticated,
  ]);

  @dropTask
  *fetchCurrentIdentity() {
    yield Promise.resolve();

    if (!this.isAuthenticated) return null;

    try {
      const data = yield Promise.all([
        this.store.query(
          "membership",
          {
            include: "organisation",
          },
          { adapterOptions: { customEndpoint: "my-memberships" } },
        ),
        this.store.queryRecord("identity", {}),
      ]);

      return {
        memberships: data[0],
        identity: data[1],
      };
    } catch (error) {
      this.invalidate();

      if (
        error.errors[0].detail ===
        "Can't create Identity, because there is already an organisation with this email address."
      ) {
        return this.router.transitionTo("support");
      }

      return this.router.transitionTo("login");
    }
  }

  get identity() {
    return this.currentIdentity.value?.identity;
  }

  get memberships() {
    return this.currentIdentity.value?.memberships;
  }

  get isNwp() {
    return Boolean(
      this.identity?.memberships.find(
        (membership) =>
          ENV.APP.circulationOrganisations.includes(
            membership.organisation.get("organisationName"),
          ) && !membership.isInactive,
      ),
    );
  }
}
