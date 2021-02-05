import graphqlHandler from "ember-caluma/mirage-graphql";

export default function () {
  this.namespace = "api/v1";

  this.get("/emails", (schema, request) => {
    const identityId = request.queryParams["filter[identity]"];
    return schema.emails.where({ identityId });
  });
  this.post("/emails");
  this.get("/emails/:id");
  this.patch("/emails/:id");
  this.delete("/emails/:id");

  this.get("/phone-numbers", (schema, request) => {
    const identityId = request.queryParams["filter[identity]"];
    return schema.phoneNumbers.where({ identityId });
  });
  this.post("/phone-numbers");
  this.get("/phone-numbers/:id");
  this.patch("/phone-numbers/:id");
  this.delete("/phone-numbers/:id");

  this.get("/identities", (schema, request) => {
    const isOrganisation = request.queryParams["filter[isOrganisation]"];
    return schema.memberships.where({ isOrganisation });
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
    const identityId = request.queryParams["filter[identity]"];
    return schema.memberships.where({ identityId });
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
