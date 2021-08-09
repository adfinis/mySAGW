"use strict";

const { name } = require("../package");

module.exports = function (environment) {
  const ENV = {
    environment,
    modulePrefix: name,
    podModulePrefix: `${name}/ui`,

    rootURL: "/",
    locationType: "auto",

    "ember-simple-auth-oidc": {
      clientId: "mysagw",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      endSessionEndpoint: "/logout",
      userinfoEndpoint: "/userinfo",
      afterLogoutUri: "/",
      host:
        process.env.OIDC_HOST ||
        "https://mysagw.local/auth/realms/mysagw/protocol/openid-connect",
    },
    "ember-validated-form": {
      theme: "uikit",
    },
    localizedModel: {
      allowAnyFallback: true,
      fallbacks: ["de", "en"],
    },
    apollo: {
      apiURL: "/graphql",
    },

    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false,
      },
    },

    APP: {
      // Here you can pass flags/options to your application document
      // when it is created
      navBarLogo: "/assets/logo-header.svg",
      navBarText: "mySAGW",

      caseStateIcons: {
        RUNNING: "clock",
        CANCELED: "ban",
        COMPLETED: "check",
      },

      casesTable: {
        defaultOrder: "CREATED_AT_DESC",
        orderOptions: [
          {
            value: "CREATED_AT_DESC",
            label: "documents.createdAt",
            direction: "documents.desc",
          },
          {
            value: "CREATED_AT_ASC",
            label: "documents.createdAt",
            direction: "documents.asc",
          },
          {
            value: "MODIFIED_AT_DESC",
            label: "documents.modifiedAt",
            direction: "documents.desc",
          },
          {
            value: "MODIFIED_AT_ASC",
            label: "documents.modifiedAt",
            direction: "documents.asc",
          },
        ],
      },

      dynamicTable: {
        classList: [], // class list for table element
        columns: [
          {
            classList: [], // class list for td element
            heading: {
              label: "documents.type",
              classList: [], // class list for th element
            },
            modelKey: "document.form.name",
            linkTo: "cases.detail.index",
          },
          {
            heading: { label: "documents.status" },
            modelKey: "status",
            type: "case-status",
          },
          {
            heading: { label: "documents.createdAt" },
            modelKey: "createdAt",
            type: "date",
          },
          {
            heading: { label: "documents.modifiedAt" },
            modelKey: "modifiedAt",
            type: "date",
          },
          {
            heading: { label: "documents.description" },
            modelKey: "document.form.description",
            truncate: true,
          },
        ],
      },

      caluma: {
        submitTaskSlug: "submit-document",
        reviseTaskSlug: "revise-docment",
        skippableTaskSlugs: [],
      },
    },
  };

  if (environment === "development") {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === "test") {
    // Testem prefers this...
    ENV.locationType = "none";

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = "#ember-testing";
    ENV.APP.autoboot = false;
  }

  if (environment === "production") {
    // here you can enable a production-specific feature
  }

  return ENV;
};
