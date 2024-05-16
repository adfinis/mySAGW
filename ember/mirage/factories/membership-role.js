import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => setAllLocales(faker.person.jobTitle()),
  description: () => setAllLocales(faker.word.words()),
  archived: () => faker.datatype.boolean(),
});
