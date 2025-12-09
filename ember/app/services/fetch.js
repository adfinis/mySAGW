import Service, { service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { handleUnauthorized } from "ember-simple-auth-oidc";
import fetch from "fetch";

const CONTENT_TYPE = "application/vnd.api+json";

const cleanObject = (obj) =>
  Object.fromEntries(
    // eslint-disable-next-line no-unused-vars
    Object.entries(obj).filter(([key, value]) => !isEmpty(value)),
  );

export default class FetchService extends Service {
  @service session;

  async fetch(resource, options = {}) {
    await this.session.refreshAuthentication.perform();

    options.headers = cleanObject({
      ...this.session.headers,
      accept: CONTENT_TYPE,
      "content-type": CONTENT_TYPE,
      ...(options.headers || {}),
    });

    const response = await fetch(resource, options);

    if (!response.ok) {
      if (response.status === 401) {
        return handleUnauthorized(this.session);
      }

      const contentType = response.headers.get("content-type");
      let body = "";

      if (/^application\/(vnd\.api+)?json$/.test(contentType)) {
        body = await response.json();
      } else if (contentType === "text/plain") {
        body = await response.text();
      }

      // throw an error containing a human readable message
      throw new Error(
        `Fetch request to URL ${response.url} returned ${response.status} ${response.statusText}:\n\n${body}`,
      );
    }

    return response;
  }
}
