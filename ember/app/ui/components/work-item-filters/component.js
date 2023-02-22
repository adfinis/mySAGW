import { trackedFunction } from "ember-resources/util/function";

import getTasksQuery from "mysagw/gql/queries/get-tasks.graphql";
import FiltersComponent from "mysagw/utils/filters-component";

export default class WorkItemFiltersComponent extends FiltersComponent {
  taskTypes = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: getTasksQuery,
        variables: {
          filter: [{ isArchived: false }],
          order: [{ attribute: "NAME" }],
        },
      },
      "allTasks.edges"
    );

    return response.map((edge) => ({
      value: edge.node.slug,
      label: edge.node.name,
    }));
  });
}
