import "./filled-text-field-qW71ccQt.js";
import { a as h, x as d, s as v, i as m, c as a, t as b } from "./index-Bs6A-haP.js";
var c = Object.defineProperty, f = Object.getOwnPropertyDescriptor, s = (l, e, o, i) => {
  for (var t = i > 1 ? void 0 : i ? f(e, o) : e, u = l.length - 1, p; u >= 0; u--)
    (p = l[u]) && (t = (i ? p(e, o, t) : p(t)) || t);
  return i && t && c(e, o, t), t;
};
let r = class extends h {
  constructor() {
    super(...arguments), this.required = !0, this.disabled = !1, this._valueStr = "";
  }
  willUpdate(l) {
    l.has("value") && (this._valueStr === "" || this.value !== Number(this._valueStr)) && (this._valueStr = this.value == null || isNaN(this.value) ? "" : this.value.toString());
  }
  render() {
    var l, e, o, i, t, u, p, n;
    return d`
      <md-filled-text-field
        .inputMode=${((l = this.selector.number) == null ? void 0 : l.step) === "any" || (((e = this.selector.number) == null ? void 0 : e.step) ?? 1) % 1 !== 0 ? "decimal" : "numeric"}
        .label=${this.label}
        .error=${!!this.errorMsg}
        .errorText=${this.errorMsg || ""}
        .placeholder=${((o = this.placeholder) == null ? void 0 : o.toString()) ?? ""}
        .min=${((t = (i = this.selector.number) == null ? void 0 : i.min) == null ? void 0 : t.toString()) ?? ""}
        .max=${((p = (u = this.selector.number) == null ? void 0 : u.max) == null ? void 0 : p.toString()) ?? ""}
        .value=${this._valueStr ?? ""}
        .step=${(((n = this.selector.number) == null ? void 0 : n.step) ?? 1).toString()}
        .disabled=${this.disabled}
        .required=${this.required}
        type="number"
        @input=${this._handleInputChange}
      >
      </md-filled-text-field>
    `;
  }
  _handleInputChange(l) {
    this._valueStr = l.target.value;
    const e = Number(this._valueStr) || void 0;
    this.value !== e && v(this, "value-changed", { value: e });
  }
};
r.styles = m`
    md-filled-text-field {
      display: block;
    }
  `;
s([
  a({ attribute: !1 })
], r.prototype, "selector", 2);
s([
  a({ type: Number })
], r.prototype, "value", 2);
s([
  a({ type: Number })
], r.prototype, "placeholder", 2);
s([
  a()
], r.prototype, "label", 2);
s([
  a({ attribute: !1 })
], r.prototype, "errorMsg", 2);
s([
  a({ type: Boolean })
], r.prototype, "required", 2);
s([
  a({ type: Boolean })
], r.prototype, "disabled", 2);
r = s([
  b("pc-selector-number")
], r);
export {
  r as PcNumberSelector
};
