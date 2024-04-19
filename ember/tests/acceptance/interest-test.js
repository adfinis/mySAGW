import { visit, fillIn, click, waitFor, currentURL } from "@ember/test-helpers";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "mysagw/tests/helpers";

module("Acceptance | interest", function (hooks) {
  setupApplicationTest(hooks);

  hooks.beforeEach(async function () {
    this.category = this.server.create("interest-category");

    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });

    await visit("/interests");
  });

  test("can list", async function (assert) {
    assert.dom("[data-test-category]").exists({ count: 1 });
    assert.dom("[data-test-interest]").exists({ count: 3 });
  });

  test("can add new category", async function (assert) {
    await click("[data-test-category-add]");

    assert.strictEqual(currentURL(), "/interests/add");

    // create new category
    await fillIn("[data-test-input-title]", "Apple");
    await fillIn("[data-test-input-description]", "Pear");
    await click("[data-test-input-public]");

    await click("[data-test-save]");

    assert.ok(currentURL().includes("/edit/"));

    await click("[data-test-interest-add]");

    // create new interest
    await fillIn("[data-test-new-interest-title]", "Melon");
    await fillIn("[data-test-new-interest-description]", "Pumpkin");
    await click("[data-test-new-interest-save]");

    await click("[data-test-save-back]");

    assert.dom("[data-test-category]").exists({ count: 2 });

    assert
      .dom('[data-test-category="Apple"] [data-test-category-title]')
      .hasText("Apple");
    assert
      .dom('[data-test-category="Apple"] [data-test-category-description]')
      .hasText("Pear");
    assert
      .dom('[data-test-category="Apple"] [data-test-category-public]')
      .exists({ count: 1 });

    assert
      .dom('[data-test-category="Apple"] [data-test-interest]')
      .exists({ count: 1 });
    assert
      .dom('[data-test-category="Apple"] [data-test-interest-title]')
      .hasText("Melon");
    assert
      .dom('[data-test-category="Apple"] [data-test-interest-description]')
      .hasText("Pumpkin");
  });

  test("can delete category", async function (assert) {
    await click("[data-test-category-delete]");

    await waitFor(".uk-modal.uk-open");

    await click(".uk-modal button.uk-button-primary");

    assert.dom("[data-test-category]").doesNotExist();
  });

  test("interest is linked", async function (assert) {
    await click(`[data-test-interest]:first-child [data-test-interest-title]`);

    assert.ok(currentURL().includes("/identities?searchTerm=%22"));
  });
});
