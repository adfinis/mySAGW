import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | identity-members", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    const identity = this.server.create("identity");
    const organisation = this.server.create("identity");
    const membership = this.server.create("membership");

    membership.identity = identity;
    membership.organisation = organisation;

    this.identity = organisation;

    await render(hbs`<IdentityMembers @identity={{this.identity}}/>`);

    assert.dom("li").exists({ count: 1 });
  });
});
