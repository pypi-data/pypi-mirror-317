import { V as c } from "./validator-C67eZdEZ.js";
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
class r extends c {
  computeValidity(e) {
    return this.checkboxControl || (this.checkboxControl = document.createElement("input"), this.checkboxControl.type = "checkbox"), this.checkboxControl.checked = e.checked, this.checkboxControl.required = e.required, {
      validity: this.checkboxControl.validity,
      validationMessage: this.checkboxControl.validationMessage
    };
  }
  equals(e, o) {
    return e.checked === o.checked && e.required === o.required;
  }
  copy({ checked: e, required: o }) {
    return { checked: e, required: o };
  }
}
export {
  r as C
};
