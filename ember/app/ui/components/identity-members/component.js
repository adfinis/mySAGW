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

  @restartableTask
  *fetchMembers() {
    const membershipResponse = yield this.store.query(
      "membership",
      {
        filter: { organisation: this.args.identity.id },
        include: "role,identity",
        page: {
          number: this.pageNumber,
          size: this.pageSize,
        },
      },
      { adapterOptions: { customEndpoint: "org-memberships" } }
    );

    this.totalPages = membershipResponse.meta.pagination?.pages;

    membershipResponse.forEach((membership) => {
      const identity = membership.identity;
      const duplicateMembership = this.members.findBy(
        "identity.id",
        identity.get("id")
      );

      membership.roles = [
        {
          title: membership.role.get("title"),
          inactive: membership.isInactive,
        },
      ];
      if (duplicateMembership && membership.role.get("title")) {
        duplicateMembership.roles = [
          ...duplicateMembership.roles,
          ...membership.roles,
        ];
      }

      if (!duplicateMembership) {
        this.members.push(membership);
      }
    });

    return membershipResponse;
  }

  @action
  loadMoreMembers() {
    this.pageNumber += 1;
    this.fetchMembers.perform();
  }
}
