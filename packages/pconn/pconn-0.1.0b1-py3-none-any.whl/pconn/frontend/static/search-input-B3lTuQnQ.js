import "./filled-text-field-qW71ccQt.js";
import { i as d, c, a as h, x as p, af as f, o as u, s as v, t as b } from "./index-Bs6A-haP.js";
var g = Object.defineProperty, y = Object.getOwnPropertyDescriptor, r = (t, l, n, a) => {
  for (var e = a > 1 ? void 0 : a ? y(l, n) : l, s = t.length - 1, o; s >= 0; s--)
    (o = t[s]) && (e = (a ? o(l, n, e) : o(e)) || e);
  return a && e && g(l, n, e), e;
};
let i = class extends h {
  constructor() {
    super(...arguments), this.disabled = !1;
  }
  render() {
    return p`
      <md-filled-text-field
        .label=${this.label || "Search"}
        .value=${this.filter || ""}
        .disabled=${this.disabled}
        @input=${this._filterInputChanged}
      >
        <div slot="leading-icon">
          <pc-svg-icon .path=${f}></pc-svg-icon>
        </div>
        <div slot="trailing-icon">
          ${this.filter && p`
            <pc-icon-button
              @click=${this._clearSearch}
              label="Clear"
              .path=${u}
              class="clear-button"
            ></pc-icon-button>
          `}
        </div>
      </md-filled-text-field>
    `;
  }
  async _filterChanged(t) {
    v(this, "value-changed", { value: String(t) });
  }
  async _filterInputChanged(t) {
    this._filterChanged(t.target.value);
  }
  async _clearSearch() {
    this._filterChanged("");
  }
};
i.styles = d`
    :host {
      display: block;
    }
    pc-svg-icon,
    pc-icon-button {
      color: var(--primary-text-color);
    }
    pc-svg-icon {
      outline: none;
    }
    .clear-button {
      --md-icon-button-icon-size: 20px;
    }
    md-filled-text-field {
      display: inherit;
    }
  `;
r([
  c()
], i.prototype, "filter", 2);
r([
  c({ type: Boolean })
], i.prototype, "disabled", 2);
r([
  c({ type: String })
], i.prototype, "label", 2);
i = r([
  b("search-input")
], i);
