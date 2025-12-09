import Component from "@glimmer/component";
import { action } from "@ember/object";

export default class CopyButtonComponent extends Component {
  @action async copy(){
    const content = document.querySelector(this.args.target)
    try{
      await navigator.clipboard.writeText(content.innerHTML)
      this.args.onSuccess?.()
    } catch(error){
      this.args.onError?.()

    }
  }
}
