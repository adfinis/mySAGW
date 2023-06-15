import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Acceptance | identities", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

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

    assert.dom(".uk-modal-body").includesText("applications");

    await click(".uk-modal-footer .uk-button-primary");

    assert.dom("[data-test-identities-list] li").exists({ count: 1 });
  });
});
