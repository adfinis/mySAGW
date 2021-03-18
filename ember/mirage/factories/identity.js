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

    const interests = server.schema.interests.all();
    interests.models = faker.random.arrayElements(
      interests.models,
      faker.random.number({ min: 0, max: 5 })
    );
    identity.interests = interests;

    server.createList(
      "additional-email",
      faker.random.number({ min: 0, max: 3 }),
      { identity }
    );

    server.createList("phone-number", faker.random.number({ min: 0, max: 3 }), {
      identity,
    });
  },
});
