import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  streetAndNumber: () => "",
  description: () => setAllLocales(faker.random.words()),
  default: (index) => index === 0,
});
