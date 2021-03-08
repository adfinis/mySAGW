import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  idpId: () => faker.random.arrayElement([null, faker.random.uuid()]),
  organisationName: () => faker.company.companyName(),
  firstName: () => faker.name.firstName(),
  lastName: () => faker.name.lastName(),
  isOrganisation: () => faker.random.boolean(),
  email: () => faker.internet.email(),

  afterCreate(identity, server) {
    if (!identity.isOrganisation) {
      identity.organisationName = null;
    }

    server.createList("additional-email", 3, { identity });
    server.createList("phone-number", 3, { identity });
  },
});
