import { ap as s, _ as c, c as m } from "./index-Bs6A-haP.js";
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const g = Symbol("createValidator"), p = Symbol("getValidityAnchor"), h = Symbol("privateValidator"), a = Symbol("privateSyncValidity"), l = Symbol("privateCustomValidationMessage");
function v(n) {
  var i;
  class d extends n {
    constructor() {
      super(...arguments), this[i] = "";
    }
    get validity() {
      return this[a](), this[s].validity;
    }
    get validationMessage() {
      return this[a](), this[s].validationMessage;
    }
    get willValidate() {
      return this[a](), this[s].willValidate;
    }
    checkValidity() {
      return this[a](), this[s].checkValidity();
    }
    reportValidity() {
      return this[a](), this[s].reportValidity();
    }
    setCustomValidity(e) {
      this[l] = e, this[a]();
    }
    requestUpdate(e, r, o) {
      super.requestUpdate(e, r, o), this[a]();
    }
    firstUpdated(e) {
      super.firstUpdated(e), this[a]();
    }
    [(i = l, a)]() {
      this[h] || (this[h] = this[g]());
      const { validity: e, validationMessage: r } = this[h].getValidity(), o = !!this[l], V = this[l] || r;
      this[s].setValidity({ ...e, customError: o }, V, this[p]() ?? void 0);
    }
    [g]() {
      throw new Error("Implement [createValidator]");
    }
    [p]() {
      throw new Error("Implement [getValidityAnchor]");
    }
  }
  return d;
}
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const u = Symbol("getFormValue"), y = Symbol("getFormState");
function S(n) {
  class i extends n {
    get form() {
      return this[s].form;
    }
    get labels() {
      return this[s].labels;
    }
    // Use @property for the `name` and `disabled` properties to add them to the
    // `observedAttributes` array and trigger `attributeChangedCallback()`.
    //
    // We don't use Lit's default getter/setter (`noAccessor: true`) because
    // the attributes need to be updated synchronously to work with synchronous
    // form APIs, and Lit updates attributes async by default.
    get name() {
      return this.getAttribute("name") ?? "";
    }
    set name(t) {
      this.setAttribute("name", t);
    }
    get disabled() {
      return this.hasAttribute("disabled");
    }
    set disabled(t) {
      this.toggleAttribute("disabled", t);
    }
    attributeChangedCallback(t, e, r) {
      if (t === "name" || t === "disabled") {
        const o = t === "disabled" ? e !== null : e;
        this.requestUpdate(t, o);
        return;
      }
      super.attributeChangedCallback(t, e, r);
    }
    requestUpdate(t, e, r) {
      super.requestUpdate(t, e, r), this[s].setFormValue(this[u](), this[y]());
    }
    [u]() {
      throw new Error("Implement [getFormValue]");
    }
    [y]() {
      return this[u]();
    }
    formDisabledCallback(t) {
      this.disabled = t;
    }
  }
  return i.formAssociated = !0, c([
    m({ noAccessor: !0 })
  ], i.prototype, "name", null), c([
    m({ type: Boolean, noAccessor: !0 })
  ], i.prototype, "disabled", null), i;
}
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
class f {
  /**
   * Creates a new validator.
   *
   * @param getCurrentState A callback that returns the current state of
   *     constraint validation-related properties.
   */
  constructor(i) {
    this.getCurrentState = i, this.currentValidity = {
      validity: {},
      validationMessage: ""
    };
  }
  /**
   * Returns the current `ValidityStateFlags` and validation message for the
   * validator.
   *
   * If the constraint validation state has not changed, this will return a
   * cached result. This is important since `getValidity()` can be called
   * frequently in response to synchronous property changes.
   *
   * @return The current validity and validation message.
   */
  getValidity() {
    const i = this.getCurrentState();
    if (!(!this.prevState || !this.equals(this.prevState, i)))
      return this.currentValidity;
    const { validity: t, validationMessage: e } = this.computeValidity(i);
    return this.prevState = this.copy(i), this.currentValidity = {
      validationMessage: e,
      validity: {
        // Change any `ValidityState` instances into `ValidityStateFlags` since
        // `ValidityState` cannot be easily `{...spread}`.
        badInput: t.badInput,
        customError: t.customError,
        patternMismatch: t.patternMismatch,
        rangeOverflow: t.rangeOverflow,
        rangeUnderflow: t.rangeUnderflow,
        stepMismatch: t.stepMismatch,
        tooLong: t.tooLong,
        tooShort: t.tooShort,
        typeMismatch: t.typeMismatch,
        valueMissing: t.valueMissing
      }
    }, this.currentValidity;
  }
}
export {
  f as V,
  S as a,
  y as b,
  g as c,
  p as d,
  u as g,
  v as m
};
