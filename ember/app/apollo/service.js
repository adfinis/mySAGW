import { inject as service } from "@ember/service";
import { setContext } from "apollo-link-context";
import ApolloService from "ember-apollo-client/services/apollo";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default ApolloService.extend(CalumaApolloServiceMixin, {
  session: service(),

  link(...args) {
    const httpLink = this._super(...args);

    const authMiddleware = setContext(async () => {
      const token = this.session.data.authenticated.access_token;
      return { headers: { authorization: `Bearer ${token}` } };
    });

    return authMiddleware.concat(httpLink);
  },
});
