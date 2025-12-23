import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";

/**
 * @arg identity
 */
export default class IdentityMembersComponent extends Component {
  @service store;
  @service intl;

  @tracked pageSize = 20;
  @tracked pageNumber = 1;
  @tracked totalPages = 1;
  @tracked members = [];

  get hasNextPage() {
    return this.pageNumber < this.totalPages;
  }

  get locale() {
    return this.intl.primaryLocale;
  }

  membersResource = trackedFunction(this, async () => {
    const membersResponse = await this.store.query(
      "identity",
      {
        filter: { organisation: this.args.identity.id },
        page: {
          number: this.pageNumber,
          size: this.pageSize,
        },
      },
      { adapterOptions: { customEndpoint: "org-memberships" } },
    );
    this.totalPages = membersResponse.meta.pagination?.pages;

    membersResponse.forEach((member) => {
      member.inactive = member.roles.every((role) => role.inactive);
      this.members.push(member);
    });
  });

  @action
  loadMoreMembers() {
    this.pageNumber += 1;
  }
}
