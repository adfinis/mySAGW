import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  authorized: () => faker.random.boolean(),
  // timeSlot: () => {},
  nextElection: () => faker.date.future(),
  comment: () => setAllLocales(faker.random.words()),
  inactive: () => faker.random.boolean(),
});
