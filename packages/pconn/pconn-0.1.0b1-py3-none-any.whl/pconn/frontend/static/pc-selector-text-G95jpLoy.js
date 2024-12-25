import "./filled-text-field-qW71ccQt.js";
import { i as u, c as o, r as c, l as h, a as f, x as d, an as x, ao as m, s as y, t as b } from "./index-Bs6A-haP.js";
var v = Object.defineProperty, _ = Object.getOwnPropertyDescriptor, s = (r, t, l, i) => {
  for (var a = i > 1 ? void 0 : i ? _(t, l) : t, n = r.length - 1, p; n >= 0; n--)
    (p = r[n]) && (a = (i ? p(t, l, a) : p(a)) || a);
  return i && a && v(t, l, a), a;
};
let e = class extends f {
  constructor() {
    super(...arguments), this.disabled = !1, this.required = !0, this._unmaskedPassword = !1;
  }
  focus() {
    this._input && this._input.focus();
  }
  render() {
    var r, t, l, i;
    return d`
      <md-filled-text-field
        .type=${this._unmaskedPassword ? "text" : ((r = this.selector.text) == null ? void 0 : r.type) ?? "text"}
        label=${this.label || ""}
        value=${this.value || ""}
        .prefixText=${((t = this.selector.text) == null ? void 0 : t.prefix) || ""}
        .suffixText=${((l = this.selector.text) == null ? void 0 : l.suffix) || ""}
        .disabled=${this.disabled}
        .required=${this.required}
        .name=${this.name || ""}
        .placeholder=${this.placeholder || ""}
        .autocomplete=${((i = this.selector.text) == null ? void 0 : i.autocomplete) || ""}
        .error=${!!this.errorMsg}
        .errorText=${this.errorMsg || ""}
        @input=${this._valueChanged}
      >
        ${this.renderIcon()}
      </md-filled-text-field>
    `;
  }
  renderIcon() {
    var r;
    return d` ${((r = this.selector.text) == null ? void 0 : r.type) === "password" ? d`
          <pc-icon-button
            toggles
            slot="trailing-icon"
            .label=${`${this._unmaskedPassword ? "Hide" : "Show"} password`}
            @click=${this._toggleUnmaskedPassword}
            .path=${this._unmaskedPassword ? x : m}
          ></pc-icon-button>
        ` : ""}`;
  }
  _toggleUnmaskedPassword() {
    this._unmaskedPassword = !this._unmaskedPassword;
  }
  _valueChanged(r) {
    let t = r.target.value;
    this.value !== t && (t === "" && !this.required && (t = void 0), y(this, "value-changed", {
      value: t
    }));
  }
};
e.styles = u`
    :host {
      display: block;
      position: relative;
    }
    :host([own-margin]) {
      margin-bottom: 5px;
    }
    md-filled-text-field {
      display: block;
    }
    pc-icon-button {
      position: absolute;
      top: 8px;
      right: 8px;
      inset-inline-start: initial;
      inset-inline-end: 8px;
      --md-icon-button-icon-size: 20px;
      color: var(--secondary-text-color);
      direction: var(--direction);
    }
  `;
s([
  o({ attribute: !1 })
], e.prototype, "selector", 2);
s([
  o()
], e.prototype, "value", 2);
s([
  o()
], e.prototype, "name", 2);
s([
  o()
], e.prototype, "label", 2);
s([
  o()
], e.prototype, "placeholder", 2);
s([
  o({ attribute: !1 })
], e.prototype, "errorMsg", 2);
s([
  o({ type: Boolean })
], e.prototype, "disabled", 2);
s([
  o({ type: Boolean })
], e.prototype, "required", 2);
s([
  c()
], e.prototype, "_unmaskedPassword", 2);
s([
  h("pc-textfield")
], e.prototype, "_input", 2);
e = s([
  b("pc-selector-text")
], e);
export {
  e as PcTextSelector
};
