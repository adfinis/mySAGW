import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  email: () => faker.internet.email(),
  description: () => faker.random.words(),
});
