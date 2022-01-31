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

  urlForFindAll(modelName, snapshot) {
    if (snapshot.adapterOptions?.customEndpoint) {
      return `${this.buildURL()}/${snapshot.adapterOptions.customEndpoint}`;
    }

    return super.urlForFindAll(modelName, snapshot);
  }

  // Overwrite and replicate the query function,
  // because ember doesnt pass adapterOptions to urlForQuery
  query(_, type, query, __, options) {
    let url = this.buildURL(type.modelName, null, null, "query", query);

    if (options?.adapterOptions?.customEndpoint) {
      url = `${this.buildURL()}/${options.adapterOptions.customEndpoint}`;
    }

    return this.ajax(url, "GET", { data: query });
  }
}
