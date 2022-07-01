import { faker } from "@faker-js/faker";
import { Factory } from "ember-cli-mirage";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  email: () => faker.internet.email(),
  description: () => setAllLocales(faker.random.words()),
});
