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
    moment: {
      includeLocales: ["de", "fr"],
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

      staffOrganisationName:
        "Schweizerische Akademie der Geistes- und Sozialwissenschaften (SAGW)",

      caseStateIcons: {
        submit: "clock",
        audit: "clock",
        revise: "clock",
        "submit-receipts": "clock",
        decision: "clock",
        completed: "check",
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

      caluma: {
        submitTaskSlug: "submit-document",
        reviseTaskSlug: "revise-document",
        completeTaskSlug: "complete-document",
        documentEditableTaskSlugs: [
          "submit-document",
          "revise-document",
          "additional-data-form",
        ],
        skippableTaskSlugs: [],
        redoableTaskSlugs: [
          "review-document",
          "circulation",
          "decision-and-credit",
          "define-amount",
        ],
        canRedoTaskSlug: [
          "circulation",
          "decision-and-credit",
          "additional-data",
          "complete-document",
        ],
        manuallyCompletableTasks: ["complete-document"],
        displayedAnswers: {
          // task slug
          "review-document": {
            // conditional answer
            "review-document-decision-reject":
              // displayed answers
              ["priorisierung-der-antrage-kommentar"],
            "review-document-decision-complete": [
              "priorisierung-der-antrage-kommentar",
            ],
            "review-document-decision-continue": [
              "priorisierung-der-antrage-kommentar",
            ],
            "review-document-decision-zurueckgezogen": [
              "priorisierung-der-antrage-kommentar",
            ],
          },
          "decision-and-credit": {
            "decision-and-credit-decision-additional-data": [
              "decision-and-credit-remark",
            ],
            "decision-and-credit-decision-complete": [
              "decision-and-credit-remark",
            ],
            "decision-and-credit-decision-close": [
              "decision-and-credit-remark",
            ],
            "decision-and-credit-decision-define-amount": [
              "decision-and-credit-remark",
            ],
            "decision-and-credit-decision-zurueckgezogen": [
              "decision-and-credit-remark",
            ],
          },
          "define-amount": {
            "define-amount-decision-continue": [
              "define-amount-amount-float",
              "define-amount-remark",
            ],
            "define-amount-decision-reject": ["define-amount-remark"],
            "define-amount-decision-zurueckgezogen": ["define-amount-remark"],
            "define-amount-decision-dismissed": ["define-amount-remark"],
          },
        },
        alwaysDisplayedAnswers: {
          "decision-and-credit": ["gesprochener-rahmenkredit"],
        },
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
