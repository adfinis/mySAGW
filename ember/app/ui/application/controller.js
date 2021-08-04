import Controller from "@ember/controller";

import ENV from "mysagw/config/environment";

export default class ApplicationController extends Controller {
  config = ENV.APP;
}
