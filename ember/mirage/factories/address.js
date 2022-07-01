import { faker } from "@faker-js/faker";
import { Factory } from "ember-cli-mirage";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  streetAndNumber: () => "",
  description: () => setAllLocales(faker.random.words()),
  default: (index) => index === 0,
});
