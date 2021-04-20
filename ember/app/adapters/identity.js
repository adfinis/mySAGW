import ApplicationAdapter from "./application";

export default class IdentityAdapter extends ApplicationAdapter {
  urlForFindAll(modelName, snapshot) {
    if (snapshot.adapterOptions?.customEndpoint) {
      return `${this.buildURL()}/${snapshot.adapterOptions.customEndpoint}`;
    }

    return super.urlForFindAll(modelName, snapshot);
  }

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
}
