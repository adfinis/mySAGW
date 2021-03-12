import { validatePresence } from "ember-changeset-validations/validators";

export default {
  // As Google's libphonenumber is too big for most client-side applications
  // and the lightweight libphonenumber-js is still about 150kb we skip the
  // format validation in the frontend and concentrate on showing the backend
  // error correctly.
  phone: [validatePresence(true)],
};
