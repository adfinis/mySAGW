import { faker } from "@faker-js/faker";
import { Factory } from "ember-cli-mirage";

export default Factory.extend({
  idpId: () => faker.datatype.uuid(),
  organisationName: () => faker.company.name(),
  firstName: () => faker.name.firstName(),
  lastName: () => faker.name.lastName(),
  isOrganisation: () => faker.datatype.boolean(),
  email: () => faker.internet.email(),

  afterCreate(identity, server) {
    if (!identity.isOrganisation) {
      identity.organisationName = null;
    }

    const interests = server.schema.interests.all();
    interests.models = faker.helpers.arrayElements(
      interests.models,
      faker.datatype.number({ min: 0, max: 5 })
    );
    identity.interests = interests;

    server.createList(
      "additional-email",
      faker.datatype.number({ min: 0, max: 3 }),
      { identity }
    );

    server.createList(
      "phone-number",
      faker.datatype.number({ min: 0, max: 3 }),
      {
        identity,
      }
    );

    server.createList("address", faker.datatype.number({ min: 0, max: 3 }), {
      identity,
    });
  },
});
