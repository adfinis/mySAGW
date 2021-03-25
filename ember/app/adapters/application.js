import JSONAPIAdapter from "@ember-data/adapter/json-api";
import OIDCAdapterMixin from "ember-simple-auth-oidc/mixins/oidc-adapter-mixin";

export default class ApplicationAdapter extends JSONAPIAdapter.extend(
  OIDCAdapterMixin
) {
  namespace = "api/v1";

  /**
   * This adds the value of adapterOptions.include as a query parameter.
   * By including the relations the response provides the necessary data
   * for Ember Data to update the store correctly.
   */
  _appendInclude(url, adapterOptions) {
    if (adapterOptions?.include) {
      return `${url}?include=${adapterOptions.include}`;
    }
    return url;
  }

  urlForCreateRecord(modelName, snapshot) {
    return this._appendInclude(
      super.urlForCreateRecord(modelName, snapshot),
      snapshot.adapterOptions
    );
  }

  urlForUpdateRecord(id, modelName, snapshot) {
    return this._appendInclude(
      super.urlForUpdateRecord(id, modelName, snapshot),
      snapshot.adapterOptions
    );
  }

  urlForDeleteRecord(id, modelName, snapshot) {
    return this._appendInclude(
      super.urlForDeleteRecord(id, modelName, snapshot),
      snapshot.adapterOptions
    );
  }
}
