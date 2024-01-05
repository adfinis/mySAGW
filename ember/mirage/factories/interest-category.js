import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  title: () => faker.random.word(),
  description: () => faker.random.words(),
  archived: () => faker.datatype.boolean(),

  afterCreate(category, server) {
    server.createList("interest", 3, { category });
  },
});
