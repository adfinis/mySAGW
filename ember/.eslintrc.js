"use strict";

module.exports = {
  extends: ["@adfinis-sygroup/eslint-config/ember-app"],

  settings: { "import/internal-regex": "^mysagw/" },

  plugins: ["ember"],
  env: {
    browser: true,
  },
  overrides: [
    // node files
    {
      files: [
        "./.eslintrc.js",
        "./.prettierrc.js",
        "./.template-lintrc.js",
        "./ember-cli-build.js",
        "./testem.js",
        "./blueprints/*/index.js",
        "./config/**/*.js",
        "./lib/*/index.js",
        "./server/**/*.js",
      ],
      parserOptions: {
        sourceType: "script",
      },
      env: {
        browser: false,
        node: true,
      },
      plugins: ["node"],
      extends: ["plugin:node/recommended"],
      rules: {
        // this can be removed once the following is fixed
        // https://github.com/mysticatea/eslint-plugin-node/issues/77
        "node/no-unpublished-require": "off",
      },
    },
    {
      // test files
      files: ["tests/**/*-test.{js,ts}"],
      extends: ["plugin:qunit/recommended"],
    },
  ],
};
