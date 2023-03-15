import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | identity-members", function (hooks) {
  setupRenderingTest(hooks);
  /*
   * There is a problem with ember-data/mirage resolving the membership role title
   * and returning undefined instead of the generated text.
   */
  test.skip("it renders", async function (assert) {
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
