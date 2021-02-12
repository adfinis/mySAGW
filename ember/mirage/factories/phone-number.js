import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  phone: () => faker.phone.phoneNumber(),
  description: () => faker.random.words(),
  default: (index) => index === 1,
});
