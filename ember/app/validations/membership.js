import { validatePresence } from "ember-changeset-validations/validators";
import { DateTime } from "luxon";

function validateTimeSlotLower() {
  return (key, newValue, oldValue, changes, content) => {
    if (
      newValue &&
      (changes?.timeSlot?.upper ?? content.get("timeSlot.upper"))
    ) {
      if (
        DateTime.fromISO(newValue) >
        DateTime.fromISO(
          changes?.timeSlot?.upper ?? content.get("timeSlot.upper")
        )
      ) {
        return "components.identity-memberships.timeSlotErrorLower";
      }
    }
    return true;
  };
}

function validateTimeSlotUpper() {
  return (key, newValue, oldValue, changes, content) => {
    if (
      newValue &&
      (changes?.timeSlot?.lower ?? content.get("timeSlot.lower"))
    ) {
      if (
        DateTime.fromISO(
          changes?.timeSlot?.lower ?? content.get("timeSlot.lower")
        ) > DateTime.fromISO(newValue)
      ) {
        return "components.identity-memberships.timeSlotError";
      }
    }
    return true;
  };
}

export default {
  organisation: [validatePresence(true)],
  timeSlot: {
    lower: [validateTimeSlotLower()],
    upper: [validateTimeSlotUpper()],
  },
};
