"use strict";

const EmberApp = require("ember-cli/lib/broccoli/ember-app");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    sourcemaps: { enabled: true },
    "ember-cli-babel": {
      includePolyfill: true,
    },
    "ember-validated-form": {
      theme: "uikit",
      defaults: {
        "types/date": "mysagw/ui/components/date-picker",
      },
    },
    "ember-fetch": {
      preferNative: true,
    },
    "ember-simple-auth": {
      useSessionSetupMethod: true,
    },
    flatpickr: {
      locales: ["fr", "de"],
    },
    "@embroider/macros": {
      setConfig: {
        "@ember-data/store": {
          polyfillUUID: true,
        },
      },
    },
    babel: {
      plugins: [
        require.resolve("ember-concurrency/async-arrow-task-transform"),
      ],
    },
  });

  // Use `app.import` to add additional libraries to the generated
  // output files.
  //
  // If you need to use different assets in different
  // environments, specify an object as the first parameter. That
  // object's keys should be the environment name and the values
  // should be the asset to use in that environment.
  //
  // If the library that you are including contains AMD or ES6
  // modules that you would like to import into your application
  // please specify an object with the list of modules as keys
  // along with the exports of each module as its value.

  return app.toTree();
};
