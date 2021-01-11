"use strict";

//eslint-disable-next-line node/no-missing-require, node/no-unpublished-require
const EmberApp = require("ember-cli/lib/broccoli/ember-app");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    sourcemaps: { enabled: true },
    "ember-cli-babel": {
      includePolyfill: true,
    },

    sassOptions: {
      includePaths: [
        // For some reason sass cant find these on its own :/
        "node_modules/ember-power-select/app/styles/",
        "node_modules/ember-basic-dropdown/app/styles/",
      ],
    },
    emberApolloClient: {
      keepGraphqlFileExtension: false,
    },
    "ember-fetch": {
      preferNative: true,
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
