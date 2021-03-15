import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  title: () => faker.random.word(),
  description: () => faker.random.words(),
  archived: () => faker.random.boolean(),
});
