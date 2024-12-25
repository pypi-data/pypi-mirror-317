import { k as p, i as g, r as d, l as h, a as u, h as m, b as v, x as r, o as f, m as _, t as $ } from "./index-Bs6A-haP.js";
import "./pc-form-CK-FZij5.js";
import "./search-input-B3lTuQnQ.js";
import "./dialog-data-entry-flow-BnPHFKR5.js";
var w = Object.defineProperty, y = Object.getOwnPropertyDescriptor, a = (t, e, i, l) => {
  for (var s = l > 1 ? void 0 : l ? y(e, i) : e, o = t.length - 1, c; o >= 0; o--)
    (c = t[o]) && (s = (l ? c(e, i, s) : c(s)) || s);
  return l && s && w(e, i, s), s;
};
let n = class extends u {
  constructor() {
    super(...arguments), this.plugins = {}, this.searchInput = "", this._filter = "", this._fetchData = new m(
      this,
      async () => {
        let t = [];
        return await v.getRequest("/config/plugins").then((e) => {
          this.plugins = e.data.result.plugins, t = e.data.result.licensedPlugins;
        }), t;
      },
      () => []
    );
  }
  async _closeDialog() {
    var t;
    await ((t = this.dialog) == null ? void 0 : t.close("close"));
  }
  _preventClose(t) {
    t.target.returnValue !== "close" && t.preventDefault();
  }
  render() {
    const t = Object.keys(this.plugins).filter(
      (e) => e.toLowerCase().includes(this._filter.toLowerCase())
    ).reduce(
      (e, i) => (e[i] = this.plugins[i], e),
      {}
    );
    return r`<pc-dialog open @close=${this._preventClose}
      >${this._fetchData.render({
      complete: (e) => r`
          <div slot="headline">
            <div>Select Plugin</div>
            <pc-icon-button
              label="Close"
              .path=${f}
              @click=${this._closeDialog}
            ></pc-icon-button>
          </div>
          <div slot="content">
            <search-input
              .filter=${this._filter}
              @value-changed=${this._filterChanged}
            ></search-input>
            <div>
              <md-list role="menu">
                ${Object.entries(t).map(
        ([i, l]) => r`
                    <md-list-item
                      type="button"
                      class="plugin_domain"
                      .domain=${i}
                      @click=${this._handleSelection}
                      .disabled=${!e.includes(i)}
                    >
                      <div slot="start">
                        <pc-svg-icon
                          .path=${l.iconPath}
                        ></pc-svg-icon>
                      </div>
                      <div slot="headline">${l.name}</div>
                      <div slot="supporting-text">
                        ${l.description}
                      </div>
                      <pc-svg-icon
                        slot="end"
                        .path=${_}
                      ></pc-svg-icon>
                    </md-list-item>
                  `
      )}
              </md-list>
            </div>
          </div>
        </pc-dialog>`
    })}</pc-dialog
    >`;
  }
  _filterChanged(t) {
    this._filter = t.detail.value;
  }
  async _handleSelection(t) {
    var l;
    if (t.target.disabled) return;
    const e = t.target.closest(".plugin_domain").domain;
    await this._closeDialog();
    const i = document.createElement("dialog-data-entry-flow");
    i.domain = e, i.handler = e, i.flowType = "config", (l = this.shadowRoot) == null || l.appendChild(i);
  }
};
n.styles = [
  p,
  g`
      @media all and (min-width: 550px) {
        pc-dialog {
          --md-dialog-min-width: 500px;
        }
      }
      search-input {
        margin: 16px 16px 0px;
      }

      md-list-item:not([disabled]):hover {
        cursor: pointer;
      }
    `
];
a([
  d()
], n.prototype, "plugins", 2);
a([
  d()
], n.prototype, "searchInput", 2);
a([
  h("pc-dialog")
], n.prototype, "dialog", 2);
a([
  d()
], n.prototype, "_filter", 2);
n = a([
  $("pc-add-plugin")
], n);
