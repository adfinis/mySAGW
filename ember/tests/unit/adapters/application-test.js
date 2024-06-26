import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | application", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:application");
    assert.ok(adapter);

    const url = "http://example.com/api/v1/foo";
    assert.strictEqual(
      adapter._appendInclude(url, { include: "bar" }),
      `${url}?include=bar`,
    );
  });

  test("urlForFindAll is correct", function (assert) {
    const adapter = this.owner.lookup("adapter:application");

    assert.strictEqual(
      adapter.urlForFindAll("identity", {}),
      "/api/v1/identities",
    );
    assert.strictEqual(
      adapter.urlForFindAll("identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      }),
      "/api/v1/my-orgs",
    );
  });
});
