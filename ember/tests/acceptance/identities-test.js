import { visit, click } from "@ember/test-helpers";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "mysagw/tests/helpers";

module("Acceptance | identities", function (hooks) {
  setupApplicationTest(hooks);

  hooks.beforeEach(async function () {
    this.identity = this.server.create("identity", { email: "test@test.com" });

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
});
