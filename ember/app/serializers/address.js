import ApplicationSerializer from "./application";

export default class AddressSerializer extends ApplicationSerializer {
  keyForAttribute(attr) {
    switch (attr) {
      case "addressAddition1":
        return "address-addition-1";
      case "addressAddition2":
        return "address-addition-2";
      case "addressAddition3":
        return "address-addition-3";
      default:
        return super.keyForAttribute(attr);
    }
  }
}
