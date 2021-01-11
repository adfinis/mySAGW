import Route from "@ember/routing/route";

export default class CasesRoute extends Route {
  model() {
    return [
      {
        id: 1,
        number: 2819,
        municipality: "Gemeinde Leuzigen",
        type: "Baugesuch",
      },
      {
        id: 2,
        number: 2839,
        municipality: "Gemeinde Münchenbuchsee",
        type: "Baugesuch",
      },
      {
        id: 3,
        number: 3892,
        municipality: "Gemeinde Köniz",
        type: "Vorabklärung",
      },
      { id: 4, number: 1893, municipality: "Gemeinde Belp", type: "Baugesuch" },
      {
        id: 5,
        number: 2832,
        municipality: "Gemeinde Schwarzenburg",
        type: "Vorabklärung",
      },
    ];
  }
}
