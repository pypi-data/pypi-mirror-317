import "./checkbox-Di7w86SP.js";
import "./pc-button-menu-BrK2NJOx.js";
import "./pc-select-Cl_dw0CS.js";
import "./filled-text-field-qW71ccQt.js";
import { a as b, x as c, ak as m, al as v, s as p, i as f, c as d, r as g, t as $ } from "./index-Bs6A-haP.js";
import { e as _ } from "./ensure-array-ILKxE5fq.js";
var y = Object.defineProperty, x = Object.getOwnPropertyDescriptor, n = (e, l, s, r) => {
  for (var i = r > 1 ? void 0 : r ? x(l, s) : l, t = e.length - 1, a; t >= 0; t--)
    (a = e[t]) && (i = (r ? a(l, s, i) : a(i)) || i);
  return r && i && y(l, s, i), i;
};
function C(e) {
  return e == null ? void 0 : e.label;
}
function u(e) {
  return !e || e === "" ? [] : _(e);
}
let o = class extends b {
  constructor() {
    super(...arguments), this.disabled = !1, this.required = !0, this._opened = !1;
  }
  render() {
    var s, r, i;
    const e = ((r = (s = this.selector.select) == null ? void 0 : s.options) == null ? void 0 : r.map(
      (t) => typeof t == "object" ? t : { value: t, label: t }
    )) || [], l = u(this.value);
    return (i = this.selector.select) != null && i.multiple ? c`
        <pc-button-menu
          .disabled=${this.disabled}
          fixed
          @opened=${this._handleOpen}
          @closed=${this._handleClose}
          multi
          activatable
        >
          <md-filled-text-field
            slot="trigger"
            .label=${this.label}
            .value=${l.map(
      (t) => C(e.find((a) => a.value === t)) || t
    ).join(", ")}
            .disabled=${this.disabled}
            tabindex="-1"
            .error=${!!this.errorMsg}
            .errorText=${this.errorMsg ?? ""}
          ></md-filled-text-field>
          <pc-svg-icon
            slot="trigger"
            .path=${this._opened ? m : v}
          ></pc-svg-icon>
          ${e.map((t) => {
      const a = t.value, h = l.includes(a);
      return c`<md-menu-item>
              <label @click=${this._preventClose}>
                <md-checkbox
                  touch-target="wrapper"
                  .checked=${h}
                  .disabled=${this.disabled}
                  .value=${a}
                  @change=${this._valueChanged}
                ></md-checkbox>
                ${t.label}</label
              >
            </md-menu-item>`;
    })}
        </pc-button-menu>
      ` : c`
      <pc-select
        label=${this.label}
        .required=${this.required}
        .disabled=${this.disabled}
      >
        ${e.length > 0 ? e.map(
      (t) => c`<md-select-option
                  .selected=${l.includes(t.value)}
                  value=${t.value}
                  @request-selection=${this._selectChanged}
                >
                  <div slot="headline">${t.label}</div>
                </md-select-option>`
    ) : ""}
      </pc-select>
    `;
  }
  _preventClose(e) {
    e.stopPropagation();
  }
  _selectChanged(e) {
    var s;
    let l = (s = e.target) == null ? void 0 : s.value;
    this.value !== l && (l === "" && (l = void 0), p(this, "value-changed", {
      value: l
    }));
  }
  _valueChanged(e) {
    const { value: l, checked: s } = e.target;
    this._handleValueChanged(l, s);
  }
  _handleValueChanged(e, l) {
    let s;
    const r = u(this.value);
    if (l) {
      if (r.includes(e)) return;
      s = [...r, e];
    } else {
      if (!r.includes(e))
        return;
      s = r.filter((i) => i !== e);
    }
    p(this, "value-changed", {
      value: s
    });
  }
  _handleOpen(e) {
    e.stopPropagation(), this._opened = !0;
  }
  _handleClose(e) {
    e.stopPropagation(), this._opened = !1;
  }
};
o.styles = f`
    md-menu-item {
      --md-menu-item-bottom-space: 4px;
    }
    md-checkbox {
      margin-top: 4px;
    }
    pc-button-menu {
      display: block;
      cursor: pointer;
    }
    md-filled-text-field {
      display: block;
      pointer-events: none;
    }
    pc-svg-icon {
      color: var(--input-dropdown-icon-color);
      position: absolute;
      right: 1em;
      top: 1em;
      cursor: pointer;
      inset-inline-end: 1em;
      inset-inline-start: initial;
      direction: var(--direction);
    }
    pc-select {
      display: block;
    }
  `;
n([
  d({ attribute: !1 })
], o.prototype, "selector", 2);
n([
  d()
], o.prototype, "value", 2);
n([
  d()
], o.prototype, "label", 2);
n([
  d({ attribute: !1 })
], o.prototype, "errorMsg", 2);
n([
  d({ type: Boolean })
], o.prototype, "disabled", 2);
n([
  d({ type: Boolean })
], o.prototype, "required", 2);
n([
  g()
], o.prototype, "_opened", 2);
o = n([
  $("pc-selector-select")
], o);
export {
  o as PcSelectSelector
};
