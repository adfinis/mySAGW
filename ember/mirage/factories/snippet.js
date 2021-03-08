import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => setAllLocales(faker.random.word()),
  body: () => setAllLocales(faker.lorem.text()),
  archived: () => faker.random.boolean(),
});
