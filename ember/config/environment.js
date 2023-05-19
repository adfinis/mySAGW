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
      afterLogoutUri: "/login",
      host:
        process.env.OIDC_HOST ||
        "https://mysagw.local/auth/realms/mysagw/protocol/openid-connect",
      enablePkce: true,
    },
    localizedModel: {
      allowAnyFallback: true,
      fallbacks: ["de", "en"],
    },
    "changeset-validations": { rawOutput: true },
    apollo: {
      apiURL: "/graphql",
    },
    "ember-caluma": {
      FLATPICKR_DATE_FORMAT: {
        de: "d.m.Y",
        fr: "d.m.Y",
        en: "m/d/Y",
      },
      FLATPICKR_DATE_FORMAT_DEFAULT: "d.m.Y",
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

      nwpOrganisationName: "Kommission Nachwuchspreis (NWP)",

      caseStateIcons: {
        submit: "clock",
        audit: "clock",
        revise: "clock",
        "submit-receipts": "clock",
        decision: "clock",
        complete: "check",
      },

      caluma: {
        submitTaskSlug: "submit-document",
        reviseTaskSlug: "revise-document",
        decisionAndCredit: {
          task: "decision-and-credit",
          question: "decision-and-credit-decision",
          answers: ["additional-data"],
        },
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
          "complete-document",
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
        orderTypeKeys: {
          attribute: [
            "DOCUMENT__FORM__NAME",
            "CASE__DOCUMENT__FORM__NAME",
            "MODIFIED_AT",
            "CREATED_AT",
            "CLOSED_AT",
          ],
        },
        filterableQuestions: {
          expertAssociations: "mitgliedinstitution",
          sections: "sektion",
          distributionPlans: "verteilplan-nr",
        },
        formVisibilities: [
          "expertAssociationForm",
          "advisoryBoardForm",
          "hiddenForm",
        ],
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
