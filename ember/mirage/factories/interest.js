import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => setAllLocales(faker.random.word()),
  description: () => setAllLocales(faker.random.words()),
  archived: () => faker.random.boolean(),
});
