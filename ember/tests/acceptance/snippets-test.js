import { visit, fillIn, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Acceptance | snippets", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    this.server.create("snippet");

    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });

    await visit("/snippets");
  });

  test("can list snippets", async function (assert) {
    assert.expect(1);

    assert.dom("[data-test-snippet-list] li").exists({ count: 1 });
  });

  test("can add an snippets", async function (assert) {
    assert.expect(2);

    assert.dom("[data-test-snippet-list] li").exists({ count: 1 });
    await click("[data-test-snippet-add]");

    await fillIn("input[name=title]", "Lorem ipsum");
    await click("button[type=submit]");

    assert.dom("[data-test-snippet-list] li").exists({ count: 2 });
  });

  test("can list snippets in sidebar", async function (assert) {
    assert.expect(1);

    await click("[data-test-snippet-sidebar-button]");
    assert.dom("[data-test-snippet-sidebar-list] li").exists({ count: 1 });
  });
});
