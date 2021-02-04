export default function () {
  this.namespace = "api/v1";

  this.get("/emails");
  this.post("/emails");
  this.get("/emails/:id");
  this.patch("/emails/:id");
  this.delete("/emails/:id");

  this.get("/phone-numbers");
  this.post("/phone-numbers");
  this.get("/phone-numbers/:id");
  this.patch("/phone-numbers/:id");
  this.delete("/phone-numbers/:id");

  this.get("/identities");
  this.post("/identities");
  this.get("/identities/:id");
  this.patch("/identities/:id");
  this.delete("/identities/:id");

  this.get("/interest-categories");
  this.get("/interests");
  this.get("/membership-roles");
  this.get("/memberships");
}
