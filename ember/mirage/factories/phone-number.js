import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  phone: () => faker.phone.phoneNumber(),
  description: () => setAllLocales(faker.random.words()),
  default: () => faker.random.boolean(),
});
