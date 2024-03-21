import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  idpId: () => faker.string.uuid(),
  organisationName: () => faker.company.name(),
  firstName: () => faker.person.firstName(),
  lastName: () => faker.person.lastName(),
  isOrganisation: false,
  email: () => faker.internet.email(),

  afterCreate(identity, server) {
    if (!identity.isOrganisation) {
      identity.organisationName = null;
    }

    const interests = server.createList(
      "interest",
      faker.number.int({ min: 0, max: 3 }),
    );
    identity.interests = interests;

    server.createList(
      "additional-email",
      faker.number.int({ min: 0, max: 3 }),
      { identity },
    );

    server.createList("phone-number", faker.number.int({ min: 0, max: 3 }), {
      identity,
    });

    server.createList("address", faker.number.int({ min: 0, max: 3 }), {
      identity,
    });
  },
});
