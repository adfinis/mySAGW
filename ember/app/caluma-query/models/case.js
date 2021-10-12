import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";

export default class CustomCaseModel extends CaseModel {
  static fragment = `{
    id
    createdAt
    modifiedAt
    createdByUser
    closedAt
    status
    meta
    workItems {
      edges {
        node {
          id
          status
          task {
            slug
          }
        }
      }
    }
    document {
      id
      createdAt
      modifiedAt
      form {
        slug
        name
        description
      }
      answers(filter: [{ questions: ["dossier-nr"] }]) {
        edges {
          node {
            id
            question {
              slug
            }
            ... on StringAnswer {
              StringAnswerValue: value
            }
          }
        }
      }
    }
  }`;
}
