import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { DateTime } from "luxon";

export default class CfFieldInputDateComponent extends Component {
  @service intl;

  @tracked flatpickrRef = null;

  get locale() {
    return this.intl.primaryLocale.split("-")[0];
  }

  @action
  onReady(_selectedDates, _dateStr, flatpickrRef) {
    this.flatpickrRef = flatpickrRef;
  }

  @action
  clearCalendar(e) {
    e.stopPropagation();
    e.preventDefault();
    this.flatpickrRef.clear();
  }

  @action
  onChange([date]) {
    // Change Javascript date to ISO string if not null.
    this.args.onChange(date ? DateTime.fromJSDate(date).toISODate() : null);
  }

  // flatpickr doesnt call onChange after manual input and clicking outside.
  @action
  onClose(dates) {
    this.onChange(dates);
  }
}
