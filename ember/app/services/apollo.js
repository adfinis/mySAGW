import { service } from "@ember/service";
import CalumaApolloService from "@projectcaluma/ember-core/services/apollo";
import { apolloMiddleware } from "ember-simple-auth-oidc";

export default class CustomApolloService extends CalumaApolloService {
  @service session;

  link() {
    const httpLink = super.link();

    return apolloMiddleware(httpLink, this.session);
  }
}
