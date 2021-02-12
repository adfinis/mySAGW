import JSONAPIAdapter from "@ember-data/adapter/json-api";

export default class EmeisStoreAdapter extends JSONAPIAdapter {
  namespace = "/emeis/api/v1";
}
