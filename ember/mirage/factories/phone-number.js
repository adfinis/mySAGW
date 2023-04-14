import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  phone: () => faker.phone.number(),
  description: () => setAllLocales(faker.random.words()),
  default: (index) => index === 0,
});
