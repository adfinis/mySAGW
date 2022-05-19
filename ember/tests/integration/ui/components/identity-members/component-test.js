import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, skip } from "qunit";

module("Integration | Component | identity-members", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  /*
   * There is a problem with ember-data/mirage resolving the membership role title
   * and returning undefined instead of the generated text.
   */
  skip("it renders", async function (assert) {
    const identity = this.server.create("identity");
    const organisation = this.server.create("identity");
    const membership = this.server.create("membership");
    const role = this.server.create("membership-role");

    membership.identity = identity;
    membership.organisation = organisation;
    membership.role = role;

    this.identity = organisation;

    await render(hbs`<IdentityMembers @identity={{this.identity}}/>`);

    assert.dom("li").exists({ count: 1 });
  });
});
