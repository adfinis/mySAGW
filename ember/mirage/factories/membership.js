import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  authorized: () => faker.random.boolean(),
  nextElection: () => faker.date.future(),
  comment: () => faker.random.words(),
  inactive: () => faker.random.boolean(),
});
