import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  authorized: () => faker.datatype.boolean(),
  nextElection: () => faker.date.future(),
  comment: () => faker.random.words(),
  inactive: () => faker.datatype.boolean(),
});
