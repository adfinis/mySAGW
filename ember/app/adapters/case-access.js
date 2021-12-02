import ApplicationAdapter from "./application";

export default class CaseAccessAdapter extends ApplicationAdapter {
  buildURL(...args) {
    const url = super.buildURL(...args);

    return url.replace("-", "/");
  }
}
