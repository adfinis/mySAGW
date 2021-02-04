import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  email: () => faker.internet.email(),
  description: () => setAllLocales(faker.random.words()),
  default: () => faker.random.boolean(),
});
