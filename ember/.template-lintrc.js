"use strict";

module.exports = {
  extends: "recommended",

  rules: {
    "no-bare-strings": true,
    "block-indentation": true,
    // disabled because of https://github.com/ember-template-lint/ember-template-lint/issues/2798
    "no-invalid-link-text": false,
  },
};
