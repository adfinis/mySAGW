import graphqlHandler from "ember-caluma/mirage-graphql";
import parseFilters from "mysagw/mirage/helpers/parse-filters";

export default function () {
  this.passthrough("/auth");
  this.passthrough("https://mysagw.local/auth/**");

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

  this.get("/identities", (schema, request) => {
    const query = parseFilters(request, [
      { source: "isOrganisation", target: "isOrganisation" },
    ]);
    return schema.identities.where(query);
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

  // Use ember-caluma's Mirage routing for /graphql endpoint.
  // https://github.com/projectcaluma/ember-caluma/blob/master/tests/dummy/app/templates/docs/testing.md
  this.post("/graphql", graphqlHandler(this), 200);
}
