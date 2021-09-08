import CaseModel from "ember-caluma/caluma-query/models/case";

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
      answers(filter: [{ questions: ["dossier-nr", "section"] }]) {
        edges {
          node {
            id
            question {
              slug
            }
            ... on StringAnswer {
              StringAnswerValue: value
            }
            ... on IntegerAnswer {
              IntegerAnswerValue: value
            }
          }
        }
      }
    }
  }`;
}
