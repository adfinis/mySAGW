import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  authorized: () => faker.datatype.boolean(),
  nextElection: () => faker.date.future(),
  comment: () => faker.random.words(),
  inactive: () => faker.datatype.boolean(),
});
