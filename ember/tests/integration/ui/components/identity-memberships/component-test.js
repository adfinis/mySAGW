import { render, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { selectChoose } from "ember-power-select/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | identity-memberships", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });
  });

  // TODO ember-power-select does not work
  test.skip("it adds", async function (assert) {
    this.identity = this.server.create("identity");
    const organisation = this.server.create("identity", {
      isOrganisation: true,
    });
    this.server.create("membership-role", {
      title: {
        de: "Chef",
      },
    });

    await render(hbs`<IdentityMemberships @identity={{this.identity}} />`);

    assert.dom("[data-test-membership]").exists({ count: 0 });

    await click("[data-test-add]");
    await selectChoose(
      "[data-test-organisation-select]",
      organisation.organisationName,
    );
    await selectChoose("[data-test-role-select]", "Chef");

    await click("[data-test-membership-save]");

    assert.dom("[data-test-membership]").exists({ count: 1 });
  });

  test("it deletes", async function (assert) {
    this.identity = this.server.create("identity");
    const organisation = this.server.create("identity", {
      isOrganisation: true,
      organisationName: "SAGW",
    });
    this.server.create("membership", {
      identity: this.identity,
      organisation,
    });

    await render(hbs`<IdentityMemberships @identity={{this.identity}} />`);

    assert.dom("[data-test-membership]").exists({ count: 1 });

    await click("[data-test-membership-delete]");
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal button.uk-button-primary");

    assert.dom("[data-test-membership]").exists({ count: 0 });
  });
});
