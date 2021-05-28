import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => setAllLocales(faker.name.jobTitle()),
  description: () => setAllLocales(faker.random.words()),
  archived: () => faker.datatype.boolean(),
});
