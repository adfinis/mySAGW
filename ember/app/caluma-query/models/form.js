import FormModel from "@projectcaluma/ember-core/caluma-query/models/form";

export default class CustomFormModel extends FormModel {
  get isAdvisoryBoardForm() {
    return this.raw.meta?.advisoryBoardForm;
  }

  get isExpertAssociationForm() {
    return this.raw.meta?.expertAssociationForm;
  }

  static fragment = `{
    name
    slug
    description
    isArchived
    isPublished
    meta
  }`;
}
