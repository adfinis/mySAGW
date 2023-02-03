import { saveAs } from "file-saver";

export default async function downloadFile(promise, filenameOverride = null) {
  const response = await promise;

  if (!response.ok) {
    throw new Error(response.statusText || response.status);
  }

  const blob = await response.blob();

  // extract filename from content-disposition header e.g.
  // inline; filename*=utf-8''2022-0948%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf
  const filename =
    filenameOverride ??
    decodeURIComponent(
      response.headers
        .get("content-disposition")
        .match(/filename\*?=['"]?(?:UTF-\d['"]*)?([^;\r\n"']*)['"]?;?/i)[1]
    );

  saveAs(blob, filename);
}
