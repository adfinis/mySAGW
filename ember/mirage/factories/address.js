import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  streetAndNumber: () => "",
  description: () => setAllLocales(faker.word.words(5)),
  default: (index) => index === 0,
});
