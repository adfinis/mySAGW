import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { restartableTask, lastValue } from "ember-concurrency";

/**
 * @arg identity
 */
export default class IdentityMembersComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  @lastValue("fetchMembers") members;
  @restartableTask *fetchMembers() {
    const members = yield this.store.query("membership", {
      filter: { organisation: this.args.identity.id },
      include: "role",
    });

    const membersDeduped = [];

    members.forEach((member) => {
      const existingMember = membersDeduped.findBy(
        "identity.id",
        member.identity.get("id")
      );

      member.roles = [
        { title: member.role.get("title"), inactive: member.isInactive },
      ];
      if (existingMember && member.role.get("title")) {
        existingMember.roles = [...existingMember.roles, ...member.roles];
      }

      if (!existingMember) {
        membersDeduped.push(member);
      }
    });

    return membersDeduped;
  }
}
