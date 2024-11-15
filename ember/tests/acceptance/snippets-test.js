import { visit, fillIn, click } from "@ember/test-helpers";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "mysagw/tests/helpers";

module("Acceptance | snippets", function (hooks) {
  setupApplicationTest(hooks);

  hooks.beforeEach(async function () {
    this.server.create("snippet", { body: { de: "Lorem ipsum" } });

    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });

    await visit("/snippets");
  });

  test("can list snippets", async function (assert) {
    assert.dom("[data-test-snippet-list] li").exists({ count: 1 });
  });

  test("can add an snippets", async function (assert) {
    assert.dom("[data-test-snippet-list] li").exists({ count: 1 });
    await click("[data-test-snippet-add]");

    await fillIn("input[name=title]", "Lorem ipsum");
    await click("button[type=submit]");

    assert.dom("[data-test-snippet-list] li").exists({ count: 2 });
  });

  test("can list snippets in sidebar", async function (assert) {
    await click("[data-test-snippet-sidebar-button]");

    assert.dom("[data-test-snippet-sidebar-list] li").exists({ count: 1 });

    await click("[data-test-snippet-sidebar-list] li:first-child a");

    assert
      .dom(".uk-accordion-content textarea:first-child")
      .hasValue("Lorem ipsum");
  });
});
