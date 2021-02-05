import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, skip } from "qunit";

module("Integration | Component | identity-interests", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  skip("it renders", async function (assert) {
    this.server.createList("interest-category", 3);

    this.identity = { id: "1" };

    await render(hbs`<IdentityInterests @identity={{this.identity}} />`);
    assert.ok(this.element);
  });
});
