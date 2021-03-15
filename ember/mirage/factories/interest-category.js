import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  title: () => faker.random.word(),
  description: () => faker.random.words(),
  archived: () => faker.random.boolean(),

  afterCreate(category, server) {
    const children = Math.floor(Math.random() * 5 + 0.5);
    server.createList("interest", children, { category });
  },
});
