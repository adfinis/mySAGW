"use strict";

module.exports = {
  extends: ["@adfinis/eslint-config/ember-app"],

  settings: { "import/internal-regex": "^mysagw/" },

  rules: {
    "ember/no-runloop": "warn",
  },
};
