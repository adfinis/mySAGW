export default function (server) {
  const form = server.create("form");
  server.create("question", {
    slug: "mitgliedinstitution",
    label: "mitgliedinstitution",
    formIds: [form.id],
    type: "MULTIPLE_CHOICE",
    hintText: null,
    options: [
      server.create("option", {
        slug: "institution-1",
        label: "Institution 1",
      }),
      server.create("option", {
        slug: "institution-2",
        label: "Institution 2",
      }),
    ],
  });
  server.create("question", {
    slug: "sektion",
    label: "sektion",
    formIds: [form.id],
    type: "MULTIPLE_CHOICE",
    hintText: null,
    options: [
      server.create("option", {
        slug: "sektion-1",
        label: "sektion 1",
      }),
      server.create("option", {
        slug: "sektion-2",
        label: "sektion 2",
      }),
    ],
  });
  server.create("question", {
    slug: "verteilplan-nr",
    label: "verteilplan-nr",
    formIds: [form.id],
    type: "MULTIPLE_CHOICE",
    hintText: null,
    options: [
      server.create("option", {
        slug: "verteilplan-nr-1",
        label: "verteilplan-nr 1",
      }),
      server.create("option", {
        slug: "verteilplan-nr-2",
        label: "verteilplan-nr 2",
      }),
    ],
  });
}
