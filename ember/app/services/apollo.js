import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";
import { inject as service } from "@ember/service";
import CalumaApolloServiceMixin from "@projectcaluma/ember-core/mixins/caluma-apollo-service-mixin";
import ApolloService from "ember-apollo-client/services/apollo";
import { handleUnauthorized } from "ember-simple-auth-oidc";

export default class CustomApolloService extends ApolloService.extend(
  CalumaApolloServiceMixin
) {
  @service session;

  link(...args) {
    const httpLink = super.link(...args);

    const authMiddleware = setContext(async () => {
      const token = this.session.data.authenticated.access_token;
      return { headers: { authorization: `Bearer ${token}` } };
    });

    const afterware = onError((error) => {
      if (error.networkError && error.networkError.statusCode === 401) {
        handleUnauthorized();
      }
    });

    return authMiddleware.concat(afterware).concat(httpLink);
  }
}
