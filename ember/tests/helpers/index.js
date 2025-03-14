import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import {
  setupApplicationTest as upstreamSetupApplicationTest,
  setupRenderingTest as upstreamSetupRenderingTest,
  setupTest as upstreamSetupTest,
} from "ember-qunit";

// This file exists to provide wrappers around ember-qunit's / ember-mocha's
// test setup functions. This way, you can easily extend the setup that is
// needed per test type.

function setupApplicationTest(hooks, options) {
  upstreamSetupApplicationTest(hooks, options);

  // Additional setup for application tests can be done here.
  //
  // For example, if you need an authenticated session for each
  // application test, you could do:
  //
  // hooks.beforeEach(async function () {
  //   await authenticateSession(); // ember-simple-auth
  // });
  //
  // This is also a good place to call test setup functions coming
  // from other addons:
  //
  setupIntl(hooks, "de");
  setupMirage(hooks);
}

function setupRenderingTest(hooks, options) {
  upstreamSetupRenderingTest(hooks, options);
  setupIntl(hooks, "de");
}

function setupTest(hooks, options) {
  upstreamSetupTest(hooks, options);
  setupIntl(hooks, "de");
}

export { setupApplicationTest, setupRenderingTest, setupTest };
