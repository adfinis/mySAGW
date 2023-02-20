import { helper } from "@ember/component/helper";
import { DateTime } from "luxon";

export default helper(function formatDate(positional /*, named*/) {
  if (!positional[0]) {
    return "-";
  }

  let date;
  if (typeof positional[0] === "object") {
    date = DateTime.fromJSDate(positional[0]);
  } else {
    date = DateTime.fromISO(positional[0]);
  }

  return date.toFormat(positional[1]);
});
