import { setContext } from "@apollo/client/link/context";
import { inject as service } from "@ember/service";
import CalumaApolloServiceMixin from "@projectcaluma/ember-core/mixins/caluma-apollo-service-mixin";
import ApolloService from "ember-apollo-client/services/apollo";

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
