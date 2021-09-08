import CustomCaseModel from "mysagw/caluma-query/models/case";
import CustomFormModel from "mysagw/caluma-query/models/form";
import CustomWorkItemModel from "mysagw/caluma-query/models/work-item";

export function initialize(application) {
  application.register("caluma-query-model:case", CustomCaseModel);
  application.register("caluma-query-model:form", CustomFormModel);
  application.register("caluma-query-model:work-item", CustomWorkItemModel);
}

export default {
  initialize,
};
