import { visit, click, currentURL } from "@ember/test-helpers";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "mysagw/tests/helpers";

module("Acceptance | identities", function (hooks) {
  setupApplicationTest(hooks);

  hooks.beforeEach(async function () {
    this.identity = this.server.create("identity", {
      email: "test@test.com",
      isOrganisation: false,
    });

    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });
  });

  test("can list identities", async function (assert) {
    await visit("/identities");

    assert.dom("[data-test-identities-list] li").exists({ count: 1 });
  });

  test("can delete identity", async function (assert) {
    this.server.create("identity");

    await visit("/identities");

    assert.dom("[data-test-identities-list] li").exists({ count: 2 });

    await click("[data-test-identities-list] li a");

    assert.dom("input[name=firstName]").hasValue(this.identity.firstName);

    await click(".uk-button-danger");

    assert.dom(".uk-modal-body").includesText("0 Gesuche");

    await click(".uk-modal-footer .uk-button-primary");

    assert.dom("[data-test-identities-list] li").exists({ count: 1 });
  });

  test("can navigate through membership", async function (assert) {
    const organisation = this.server.create("identity", {
      isOrganisation: true,
    });
    const identity = this.server.create("identity", { isOrganisation: false });
    this.server.create("membership", { identity, organisation });

    await visit(`/identities/edit/${identity.id}`);

    await click("[data-test-membership] a");

    assert.strictEqual(currentURL(), `/identities/edit/${organisation.id}`);
    assert.dom("input[type=checkbox]").isChecked();
  });
});
