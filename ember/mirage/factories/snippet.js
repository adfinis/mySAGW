import { faker } from "@faker-js/faker";
import { Factory } from "ember-cli-mirage";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => faker.random.word(),
  body: () => setAllLocales(faker.lorem.text()),
  archived: false,
});
