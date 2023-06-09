import { module, test } from "qunit";

import { setupTest } from "mysagw/tests/helpers";

module("Unit | Service | case-data", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:case-data");
    assert.ok(service);
  });
});
