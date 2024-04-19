import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  title: () => faker.word.sample(),
  description: () => faker.word.words(5),
  archived: () => faker.datatype.boolean(),
});
