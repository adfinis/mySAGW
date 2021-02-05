import JSONAPIAdapter from "@ember-data/adapter/json-api";

export default class ApplicationAdapter extends JSONAPIAdapter {
  namespace = "api/v1";

  _appendInclude(url, adapterOptions) {
    if (adapterOptions?.include) {
      return `${url}?include=${adapterOptions.include}`;
    }
    return url;
  }

  urlForUpdateRecord(id, modelName, snapshot) {
    return this._appendInclude(
      super.urlForUpdateRecord(id, modelName, snapshot),
      snapshot.adapterOptions
    );
  }

  urlForCreateRecord(modelName, snapshot) {
    return this._appendInclude(
      super.urlForCreateRecord(modelName, snapshot),
      snapshot.adapterOptions
    );
  }
}
