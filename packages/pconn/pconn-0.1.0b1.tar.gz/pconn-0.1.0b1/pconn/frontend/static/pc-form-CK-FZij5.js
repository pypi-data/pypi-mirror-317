import { c as o, t as b, a as f, x as h, i as y, s as m } from "./index-Bs6A-haP.js";
import { d as v } from "./dynamic-element-directive-UOoPpDHn.js";
var $ = Object.defineProperty, g = Object.getOwnPropertyDescriptor, i = (r, e, s, a) => {
  for (var t = a > 1 ? void 0 : a ? g(e, s) : e, c = r.length - 1, n; c >= 0; c--)
    (n = r[c]) && (t = (a ? n(e, s, t) : n(t)) || t);
  return a && t && $(e, s, t), t;
};
const u = {
  boolean: () => import("./pc-selector-boolean-NiT7zzZj.js"),
  number: () => import("./pc-selector-number-z7wPw9bt.js"),
  select: () => import("./pc-selector-select-8qW38JmH.js"),
  text: () => import("./pc-selector-text-G95jpLoy.js"),
  file: () => import("./pc-selector-file-B7OhEu3u.js")
};
let l = class extends f {
  constructor() {
    super(...arguments), this.disabled = !1, this.required = !0;
  }
  async focus() {
    var r;
    await this.updateComplete, (r = this.renderRoot.querySelector("#selector")) == null || r.focus();
  }
  get _type() {
    return Object.keys(this.selector)[0];
  }
  willUpdate(r) {
    var e;
    r.has("selector") && this.selector && ((e = u[this._type]) == null || e.call(u));
  }
  render() {
    return h`
      ${v(`pc-selector-${this._type}`, {
      name: this.name,
      selector: this.selector,
      value: this.value,
      label: this.label,
      errorMsg: this.errorMsg,
      placeholder: this.placeholder,
      disabled: this.disabled,
      required: this.required
    })}
    `;
  }
};
i([
  o()
], l.prototype, "name", 2);
i([
  o({ attribute: !1 })
], l.prototype, "selector", 2);
i([
  o()
], l.prototype, "value", 2);
i([
  o()
], l.prototype, "label", 2);
i([
  o({ attribute: !1 })
], l.prototype, "errorMsg", 2);
i([
  o()
], l.prototype, "placeholder", 2);
i([
  o({ type: Boolean })
], l.prototype, "disabled", 2);
i([
  o({ type: Boolean })
], l.prototype, "required", 2);
l = i([
  b("pc-selector")
], l);
var _ = Object.defineProperty, P = Object.getOwnPropertyDescriptor, d = (r, e, s, a) => {
  for (var t = a > 1 ? void 0 : a ? P(e, s) : e, c = r.length - 1, n; c >= 0; c--)
    (n = r[c]) && (t = (a ? n(e, s, t) : n(t)) || t);
  return a && t && _(e, s, t), t;
};
const q = (r, e) => r ? e.name ? r[e.name] : r : null;
let p = class extends f {
  constructor() {
    super(...arguments), this.disabled = !1;
  }
  render() {
    var r;
    return h`
      <div class="root" part="root">
        ${this.error && this.error.base ? h` <pc-alert
              alert-type="error"
              .header=${(r = this.errorDescriptions) == null ? void 0 : r[this.error.base]}
            ></pc-alert>` : ""}
        ${this.schema.map(
      (e) => {
        var s;
        return h`<pc-selector
              .schema=${e}
              .name=${e.name}
              .selector=${e.selector}
              .value=${q(this.data, e)}
              .label=${this.labels[e.name] || e.name}
              .errorMsg=${(s = this.errorDescriptions) == null ? void 0 : s[e.name]}
              .disabled=${e.disabled || this.disabled || !1}
              .placeholder=${e.required ? "" : e.default}
              .required=${e.required || !1}
            ></pc-selector>`;
      }
    )}
      </div>
    `;
  }
  createRenderRoot() {
    const r = super.createRenderRoot();
    return r.addEventListener("value-changed", (e) => {
      e.stopPropagation();
      const s = e.target.schema, a = s.name ? { [s.name]: e.detail.value } : e.detail.value;
      m(this, "value-changed", {
        value: { ...this.data, ...a }
      });
    }), r;
  }
};
p.styles = y`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    .error {
      color: red; //enhance the look of the error
    }
  `;
d([
  o({ attribute: !1 })
], p.prototype, "data", 2);
d([
  o({ attribute: !1 })
], p.prototype, "schema", 2);
d([
  o({ attribute: !1 })
], p.prototype, "labels", 2);
d([
  o()
], p.prototype, "error", 2);
d([
  o({ attribute: !1 })
], p.prototype, "errorDescriptions", 2);
d([
  o({ type: Boolean })
], p.prototype, "disabled", 2);
p = d([
  b("pc-form")
], p);
