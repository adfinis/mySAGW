import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | identity", function (hooks) {
  setupTest(hooks);

  test("urlForFindAll is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal(adapter.urlForFindAll("identity", {}), "/api/v1/identities");
    assert.equal(
      adapter.urlForFindAll("identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      }),
      "/api/v1/my-orgs"
    );
  });

  test("urlForFindRecord is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal(
      adapter.urlForFindRecord("1", "identity", {}),
      "/api/v1/identities/1"
    );
    assert.equal(
      adapter.urlForFindRecord("1", "identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      }),
      "/api/v1/my-orgs/1"
    );
  });

  test("urlForQueryRecord is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal(adapter.urlForQueryRecord(), "/api/v1/me");
  });

  test("urlForUpdateRecord is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal(
      adapter.urlForUpdateRecord("1", "identity", {}),
      "/api/v1/identities/1"
    );
    assert.equal(
      adapter.urlForUpdateRecord("1", "identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      }),
      "/api/v1/my-orgs"
    );
  });
});
