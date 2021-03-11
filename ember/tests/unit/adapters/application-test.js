import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | application", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:application");
    assert.ok(adapter);

    const url = "http://example.com/api/v1/foo";
    assert.equal(
      adapter._appendInclude(url, { include: "bar" }),
      `${url}?include=bar`
    );
  });
});
