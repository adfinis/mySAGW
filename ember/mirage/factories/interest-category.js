import { Factory } from "ember-cli-mirage";
import faker from "faker";

import setAllLocales from "../helpers/set-all-locales";

export default Factory.extend({
  title: () => setAllLocales(faker.random.word()),
  description: () => setAllLocales(faker.random.words()),
  archived: () => faker.random.boolean(),

  afterCreate(category, server) {
    const children = Math.floor(Math.random() * 5 + 0.5);
    server.createList("interest", children, { category });
  },
});
