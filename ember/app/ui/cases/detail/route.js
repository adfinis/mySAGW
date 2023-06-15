import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class CasesDetailRoute extends Route {
  @service store;
  @service caseData;

  async model({ case_id }) {
    const caseId = decodeId(case_id);

    await Promise.all([
      ...this.caseData.fetch(caseId),
      this.store.query("case-access", {
        filter: { caseIds: caseId },
        include: "identity",
      }),
    ]);

    return this.caseData.case;
  }
}
