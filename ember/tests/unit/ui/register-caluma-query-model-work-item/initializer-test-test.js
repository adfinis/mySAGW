import Application from "@ember/application";
import { run } from "@ember/runloop";
import Resolver from "ember-resolver";
import { initialize } from "mysagw/initializers/register-caluma-query-model-work-item";
import { module, test } from "qunit";

module(
  "Unit | Initializer | register-caluma-query-model-work-item",
  function (hooks) {
    hooks.beforeEach(function () {
      this.TestApplication = class TestApplication extends Application {};
      this.TestApplication.initializer({
        name: "initializer under test",
        initialize,
      });

      this.application = this.TestApplication.create({
        autoboot: false,
        Resolver,
      });
    });

    hooks.afterEach(function () {
      run(this.application, "destroy");
    });

    // TODO: Replace this with your real tests.
    test("it works", async function (assert) {
      await this.application.boot();

      assert.ok(true);
    });
  }
);
