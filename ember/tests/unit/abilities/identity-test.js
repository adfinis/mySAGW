import { setupMirage } from "ember-cli-mirage/test-support";
import { setupTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Unit | Ability | identity", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.ability = this.owner.lookup("ability:identity");
  });

  test("staff can add", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });

    assert.ok(this.ability.canAdd);
  });

  test("normal can not add", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [] },
    });

    assert.notOk(this.ability.canAdd);
  });

  test("staff can edit", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });

    assert.ok(this.ability.canEdit);
  });

  test("own identity can edit", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [], sub: "own-id" },
    });

    this.ability.set(
      "model",
      this.server.create("identity", { idpId: "own-id", isOrganisation: false })
    );

    assert.ok(this.ability.canEdit);
  });

  // Mirage relationships are not working properly
  test.todo("organisation admin can edit", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [], sub: "own-id" },
    });

    const identity = this.server.create("identity", { idpId: "own-id" });
    const organisation = this.server.create("identity", {
      isOrganisation: true,
    });
    const membership = this.server.create("membership", {
      identity,
      organisation,
      authorized: true,
      isInactive: false,
    });
    organisation.members = [membership];

    this.ability.set("model", organisation);

    assert.ok(this.ability.canEdit);
  });

  test("other identity can not edit", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [], sub: "own-id" },
    });

    this.ability.set(
      "model",
      this.server.create("identity", {
        idpId: "other-id",
        isOrganisation: false,
      })
    );

    assert.notOk(this.ability.canEdit);
  });
});
