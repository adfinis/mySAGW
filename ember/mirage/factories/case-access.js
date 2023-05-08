import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  caseId: () => faker.datatype.uuid(),

  afterCreate(caseAccess, server) {
    const identity = server.create("identity");
    caseAccess.identity = identity.idpId;
    caseAccess.email = identity.email;
  },
});
