import ApplicationAdapter from "./application";

export default class IdentityAdapter extends ApplicationAdapter {
  urlForQueryRecord() {
    return `${this.buildURL()}/me`;
  }

  urlForFindAll() {
    return `${this.buildURL()}/my-orgs`;
  }

  urlForUpdateRecord(id, modelName, snapshot) {
    if (snapshot.adapterOptions.meEndpoint) {
      return `${this.buildURL()}/me`;
    }

    return super.urlForUpdateRecord(id, modelName, snapshot);
  }
}
