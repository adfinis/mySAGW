import JSONAPIAdapter from "@ember-data/adapter/json-api";

export default class EmeisStoreAdapter extends JSONAPIAdapter {
  // Configure this to your needs.
  namespace = "/emeis/api/v1";
}
