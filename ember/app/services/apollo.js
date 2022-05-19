import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";
import { inject as service } from "@ember/service";
import CalumaApolloService from "@projectcaluma/ember-core/services/apollo";
import { handleUnauthorized } from "ember-simple-auth-oidc";

export default class CustomApolloService extends CalumaApolloService {
  @service session;

  link(...args) {
    const httpLink = super.link(...args);

    const authMiddleware = setContext(async () => {
      const token = this.session.data.authenticated.access_token;
      return { headers: { authorization: `Bearer ${token}` } };
    });

    const afterware = onError((error) => {
      if (error.networkError && error.networkError.statusCode === 401) {
        handleUnauthorized(this.session);
      }
    });

    return authMiddleware.concat(afterware).concat(httpLink);
  }
}
