import FormModel from "@projectcaluma/ember-core/caluma-query/models/form";

export default class CustomFormModel extends FormModel {
  static fragment = `{
    name
    slug
    description
    isArchived
    isPublished
    meta
  }`;
}
