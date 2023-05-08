import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => faker.random.word(),
  body: () => setAllLocales(faker.lorem.text()),
  archived: false,
});
