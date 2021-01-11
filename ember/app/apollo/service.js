import ApolloService from "ember-apollo-client/services/apollo";
//eslint-disable-next-line ember/no-mixins
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default ApolloService.extend(CalumaApolloServiceMixin, {});
