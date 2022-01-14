import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { restartableTask } from "ember-concurrency";

/**
 * @arg identity
 */
export default class IdentityMembersComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  @tracked pageSize = 10;
  @tracked pageNumber = 1;
  @tracked totalPages = 1;
  @tracked members = [];

  get hasNextPage() {
    return this.pageNumber < this.totalPages;
  }

  @restartableTask *fetchMembers() {
    const members = yield this.store.query("membership", {
      filter: { organisation: this.args.identity.id },
      include: "role",
      page: {
        number: this.pageNumber,
        size: this.pageSize,
      },
    });

    this.totalPages = members.meta.pagination?.pages;
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

    this.members = [...this.members, ...members.toArray()];

    return membersDeduped;
  }

  @action
  loadMoreMembers() {
    this.pageNumber += 1;
    this.fetchMembers.perform();
  }
}
