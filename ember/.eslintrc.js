"use strict";

module.exports = {
  extends: ["@adfinis-sygroup/eslint-config/ember-app"],

  settings: { "import/internal-regex": "^mysagw/" },

  rules: {
    "ember/no-mixins": "warn",
  },
};
