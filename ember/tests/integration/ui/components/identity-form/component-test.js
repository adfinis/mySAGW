import { render, fillIn, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Integration | Component | identity-form", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({ userinfo: { mysagw_groups: ["sagw"] } });
    this.model = this.server.create("identity");
  });

  test("it renders", async function (assert) {
    await render(hbs`<IdentityForm @identity={{this.model}}/>`);

    assert.dom("input[name=firstName]").hasValue(this.model.firstName);
  });

  test("it saves", async function (assert) {
    await render(hbs`<IdentityForm @identity={{this.model}}/>`);

    await fillIn("input[name=firstName]", "Lorem ipsum");
    await click("button[type=submit]");
    assert.dom("input[name=firstName]").hasValue("Lorem ipsum");
  });
});
