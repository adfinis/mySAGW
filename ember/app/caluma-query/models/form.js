import FormModel from "ember-caluma/caluma-query/models/form";

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
