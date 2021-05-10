import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | identity", function (hooks) {
  setupTest(hooks);

  test("urlForFindAll is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal("/api/v1/identities", adapter.urlForFindAll("identity", {}));
    assert.equal(
      "/api/v1/my-orgs",
      adapter.urlForFindAll("identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      })
    );
  });

  test("urlForFindRecord is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal(
      "/api/v1/identities/1",
      adapter.urlForFindRecord("1", "identity", {})
    );
    assert.equal(
      "/api/v1/my-orgs/1",
      adapter.urlForFindRecord("1", "identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      })
    );
  });

  test("urlForQueryRecord is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal("/api/v1/me", adapter.urlForQueryRecord());
  });

  test("urlForUpdateRecord is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");

    assert.equal(
      "/api/v1/identities/1",
      adapter.urlForUpdateRecord("1", "identity", {})
    );
    assert.equal(
      "/api/v1/my-orgs",
      adapter.urlForUpdateRecord("1", "identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      })
    );
  });
});
