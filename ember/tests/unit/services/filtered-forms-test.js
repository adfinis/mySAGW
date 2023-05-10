import { setupMirage } from "ember-cli-mirage/test-support";
import { setupTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Unit | Service | filtered-forms", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    /*
     * A total of 8 forms
     * 1 public
     * 4 internal
     * 5 expertAssociation
     * 6 advisoryBoard
     */
    this.server.create("form");
    this.server.createList("form", 1, { meta: { internalForm: true } });
    this.server.createList("form", 2, { meta: { advisoryBoardForm: true } });
    this.server.createList("form", 3, {
      meta: { expertAssociationForm: true },
    });
    this.server.create("form", {
      meta: {
        expertAssociationForm: true,
        internalForm: true,
      },
    });
    this.server.create("form", {
      meta: {
        advisoryBoardForm: true,
        internalForm: true,
      },
    });
    this.server.create("form", {
      meta: {
        advisoryBoardForm: true,
        expertAssociationForm: true,
      },
    });
    this.server.create("form", {
      meta: {
        advisoryBoardForm: true,
        expertAssociationForm: true,
        internalForm: true,
      },
    });
  });

  test("it filters expert association forms", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [] },
    });

    const service = this.owner.lookup("service:filtered-forms");
    const identity = this.server.create("identity", {
      isAuthorized: false,
      isOrganisation: false,
    });
    const organisation = this.server.create("identity", {
      isAuthorized: true,
      isOrganisation: true,
      isExpertAssociation: true,
    });
    this.server.create("membership", {
      identity,
      organisation,
      authorized: true,
    });

    const forms = await service.fetch();

    assert.strictEqual(forms.length, 7);
  });

  test("it filters advisory board forms", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [] },
    });

    const service = this.owner.lookup("service:filtered-forms");
    const identity = this.server.create("identity", {
      isAuthorized: false,
      isOrganisation: false,
    });
    const organisation = this.server.create("identity", {
      isAuthorized: true,
      isOrganisation: true,
      isAdvisoryBoard: true,
    });
    this.server.create("membership", {
      identity,
      organisation,
      authorized: true,
    });

    const forms = await service.fetch();

    assert.strictEqual(forms.length, 6);
  });

  test("it filters internal forms", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: ["sagw"] },
    });
    const service = this.owner.lookup("service:filtered-forms");

    const forms = await service.fetch();

    assert.strictEqual(forms.length, 5);
  });

  test("it filters public forms", async function (assert) {
    await authenticateSession({
      access_token: "123qweasdyxc",
      userinfo: { mysagw_groups: [] },
    });
    const service = this.owner.lookup("service:filtered-forms");

    const forms = await service.fetch();

    assert.strictEqual(forms.length, 1);
  });
});
