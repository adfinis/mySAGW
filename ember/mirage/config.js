import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";
import { discoverEmberDataModels } from "ember-cli-mirage";
import { createServer } from "miragejs";

import parseFilters from "mysagw/mirage/helpers/parse-filters";

export default function (config) {
  const finalConfig = {
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes,
  };

  return createServer(finalConfig);
}

function routes() {
  this.passthrough("/auth");
  this.passthrough("https://mysagw.local/auth/**");

  // Use ember-caluma's Mirage routing for /graphql endpoint.
  // https://github.com/projectcaluma/ember-caluma/blob/master/tests/dummy/app/templates/docs/testing.md
  this.post("/graphql", graphqlHandler(this), 200);

  this.namespace = "api/v1";

  this.get("/additional-emails", (schema, request) => {
    const query = parseFilters(request, [
      { source: "identity", target: "identityId" },
    ]);
    return schema.additionalEmails.where(query);
  });
  this.post("/additional-emails");
  this.get("/additional-emails/:id");
  this.patch("/additional-emails/:id");
  this.delete("/additional-emails/:id");

  this.get("/phone-numbers", (schema, request) => {
    const query = parseFilters(request, [
      { source: "identity", target: "identityId" },
    ]);
    return schema.phoneNumbers.where(query);
  });
  this.post("/phone-numbers");
  this.get("/phone-numbers/:id");
  this.patch("/phone-numbers/:id");
  this.delete("/phone-numbers/:id");

  this.get("/addresses", (schema, request) => {
    const query = parseFilters(request, [
      { source: "identity", target: "identityId" },
    ]);
    return schema.addresses.where(query);
  });
  this.post("/addresses");
  this.get("/addresses/:id");
  this.patch("/addresses/:id");
  this.delete("/addresses/:id");
  this.options("/addresses", () => {
    return {
      data: {
        actions: {
          POST: {
            country: {
              choices: [
                {
                  value: "CH",
                  display_name: "Schweiz",
                },
              ],
            },
          },
        },
      },
    };
  });

  this.get("/identities", (schema, request) => {
    const query = parseFilters(request, [
      { source: "isOrganisation", target: "isOrganisation" },
    ]);

    const pageSize = Number(request.queryParams["page[size]"]);
    const pageNumber = Number(request.queryParams["page[number]"] || 1);
    const search = request.queryParams.search?.toLowerCase();
    const keys = ["organisationName", "firstName", "lastName", "email"];

    const result = schema.identities.where(function (identity) {
      let result = !(search || Object.keys(query).length);

      if (search) {
        for (const key of keys) {
          if (identity[key]?.toLowerCase().includes(search)) {
            result = true;
            break;
          }
        }
      }

      if (Object.keys(query).length) {
        for (const key in query) {
          if (String(identity[key]) === query[key]) {
            result = true;
            break;
          }
        }
      }

      return result;
    });

    if (pageSize) {
      const start = (pageNumber - 1) * pageSize;
      const sliced = result.slice(start, start + pageSize);
      const json = this.serializerOrRegistry.serialize(sliced);
      json.meta = {
        pagination: {
          count: result.models.length,
          pages: Math.ceil(result.models.length / pageSize),
          page: pageNumber,
        },
      };
      return json;
    }

    return result;
  });
  this.post("/identities");
  this.get("/identities/:id");
  this.patch("/identities/:id");
  this.delete("/identities/:id");

  this.get("/interests");
  this.post("/interests");
  this.get("/interests/:id");
  this.patch("/interests/:id");
  this.delete("/interests/:id");

  this.get("/interest-categories");
  this.post("/interest-categories");
  this.get("/interest-categories/:id");
  this.patch("/interest-categories/:id");
  this.delete("/interest-categories/:id");

  this.get("/memberships", (schema, request) => {
    const query = parseFilters(request, [
      { source: "identity", target: "identityId" },
    ]);
    return schema.memberships.where(query);
  });
  this.post("/memberships");
  this.get("/memberships/:id");
  this.patch("/memberships/:id");
  this.delete("/memberships/:id");

  this.get("/membership-roles");
  this.post("/membership-roles");
  this.get("/membership-roles/:id");
  this.patch("/membership-roles/:id");
  this.delete("/membership-roles/:id");

  this.get("/snippets", (schema, request) => {
    const query = parseFilters(request, [
      { source: "archived", target: "archived" },
    ]);
    return schema.snippets.where(query);
  });
  this.post("/snippets");
  this.get("/snippets/:id");
  this.patch("/snippets/:id");

  this.get("/org-memberships", (schema, request) => {
    const query = parseFilters(request, [
      { source: "identity", target: "identityId" },
    ]);
    return schema.memberships.where(query);
  });

  this.get("/case/accesses", (schema, request) => {
    const query = parseFilters(request, [
      { source: "ipdIds", target: "idpId" },
    ]);
    return schema.memberships.where(query);
  });
  this.post("/case/accesses");

  this.get("/my-orgs", (schema, request) => {
    const query = parseFilters(request, [
      { source: "identity", target: "identityId" },
    ]);
    return schema.identities.where(query);
  });

  this.get("/my-memberships", (schema) => {
    return schema.memberships.all();
  });

  this.get("/me", (schema) => {
    return schema.identities.findOrCreateBy({ email: "test@test.com" });
  });
}
