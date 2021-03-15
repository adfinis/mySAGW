import Service from "ember-uikit/services/notification";
import formatError from "mysagw/utils/format-error";

export default class NotificationService extends Service {
  fromError(error) {
    this.danger(formatError(error));
  }
}
