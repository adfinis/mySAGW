import { faker } from "@faker-js/faker";
import { Factory } from "ember-cli-mirage";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => setAllLocales(faker.name.jobTitle()),
  description: () => setAllLocales(faker.random.words()),
  archived: () => faker.datatype.boolean(),
});
