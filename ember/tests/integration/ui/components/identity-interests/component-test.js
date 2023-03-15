import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | identity-interests", function (hooks) {
  setupRenderingTest(hooks);

  // Mirage does not work with relationships
  test.skip("it renders", async function (assert) {
    this.identity = this.server.create("identity", {
      interests: this.server.createList("interest", 3),
    });

    await render(hbs`<IdentityInterests @identity={{this.identity}} />`);

    assert.ok(this.element);
  });
});
