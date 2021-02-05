import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  idpId: () => faker.random.number(),
  organisationName: () => faker.company.companyName(),
  firstName: () => faker.name.firstName(),
  lastName: () => faker.name.lastName(),
  isOrganisation: () => faker.random.boolean(),

  afterCreate(identity, server) {
    server.createList("email", 3, { identity });
    server.createList("phone-number", 3, { identity });
  },
});
