import ApplicationAdapter from "./application";

export default class IdentityAdapter extends ApplicationAdapter {
  urlForFindRecord(id, modelName, snapshot) {
    if (snapshot.adapterOptions?.customEndpoint) {
      return `${this.buildURL()}/${
        snapshot.adapterOptions.customEndpoint
      }/${id}`;
    }

    return super.urlForFindRecord(id, modelName, snapshot);
  }

  urlForQueryRecord() {
    return `${this.buildURL()}/me`;
  }

  urlForUpdateRecord(id, modelName, snapshot) {
    if (snapshot.adapterOptions?.customEndpoint) {
      return `${this.buildURL()}/${snapshot.adapterOptions.customEndpoint}`;
    }

    return super.urlForUpdateRecord(id, modelName, snapshot);
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
