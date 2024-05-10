import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  title: () => faker.word.noun(),
  description: () => faker.word.words(),
  archived: () => faker.datatype.boolean(),
});
