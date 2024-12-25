import { i as _, c as p, l as v, a as m, x as l, s as y, t as g, h as $, b as f, p as b, r as u } from "./index-Bs6A-haP.js";
import { m as C } from "./memoize-one.esm-DezIwejE.js";
import "./search-input-B3lTuQnQ.js";
import "./filled-text-field-qW71ccQt.js";
import "./pc-expansion-panel-COx4GI5O.js";
import { c as w } from "./styles-CmkOrDPY.js";
import "./pc-label-DgMf7W2p.js";
import "./pc-circular-progress-CXHtR8Ql.js";
const P = (e, t) => {
  const r = Object.keys(e), s = Object.keys(t);
  if (r.length !== s.length)
    return !1;
  for (const a of r)
    if (e[a] !== t[a])
      return !1;
  return !0;
};
var x = Object.defineProperty, O = Object.getOwnPropertyDescriptor, h = (e, t, r, s) => {
  for (var a = s > 1 ? void 0 : s ? O(t, r) : t, i = e.length - 1, d; i >= 0; i--)
    (d = e[i]) && (a = (s ? d(t, r, a) : d(a)) || a);
  return s && a && x(t, r, a), a;
};
let o = class extends m {
  constructor() {
    super(...arguments), this.loading = !1;
  }
  get cardholderPdfs() {
    return this._cardholderPdfs !== void 0 ? this._cardholderPdfs : (this._cardholderPdfs = this.cardholder.pdfs ? Object.fromEntries(
      this.cardholder.pdfs.filter((e) => !e.readOnly).map((e) => [e.name, e.value])
    ) : {}, this._cardholderPdfs);
  }
  render() {
    return l`
      <pc-expansion-panel>
        <div slot="header" class="header">
          <pc-label>
            ${this.cardholder.firstName + " " + this.cardholder.lastName}
            ${this.cardholder.photo ? l`<img
                  slot="icon"
                  src=${`data:image/jpeg;base64,${this.cardholder.photo}`}
                  alt="profile of cardholder"
                />` : l`<div slot="icon" class="initials">
                  ${`${this._computeInitials()}`}
                </div>`}
          </pc-label>
        </div>
        ${this.cardholder.pdfs && this.cardholder.pdfs.length > 0 ? l` <div class="root">
                ${this.cardholder.pdfs.map(
      (e) => l`
                    <md-filled-text-field
                      label=${e.name}
                      .value=${e.value}
                      @input=${this._valueChanged}
                      .configValue=${e.name}
                      .disabled=${e.readOnly || this.loading}
                    >
                    </md-filled-text-field>
                  `
    )}
              </div>
              <div class="buttons">
                ${this.error ? l`<pc-alert
                      alert-type="error"
                      .header=${this.error}
                      dismissable
                      @alert-dismissed-clicked=${this._dismissError}
                    ></pc-alert>` : ""}
                <md-text-button
                  disabled
                  id="save-btn"
                  @click=${this._handleSubmit}
                  >SAVE
                </md-text-button>
              </div>` : ""}
      </pc-expansion-panel>
    `;
  }
  _computeInitials() {
    let e = "";
    return this.cardholder.firstName && (e += this.cardholder.firstName[0]), this.cardholder.lastName && (e += this.cardholder.lastName[0]), e;
  }
  _dismissError() {
    this.error = void 0;
  }
  _valueChanged(e) {
    var s;
    e.stopPropagation();
    const t = e.target.configValue, r = ((s = e.detail) == null ? void 0 : s.value) || e.target.value;
    this.cardholderPdfs[t] !== r && (this.newValue || (this.newValue = {}), this.newValue[t] = r, this.saveBtn.disabled = P(this.newValue, this.cardholderPdfs));
  }
  _handleSubmit(e) {
    e.stopPropagation(), y(this, "value-changed", {
      value: {
        id: this.cardholder.id,
        pdfs: this.newValue
      }
    });
  }
};
o.styles = [
  w,
  _`
      .initials {
        display: inline-block;
        line-height: 48px;
        text-align: center;
        background-color: grey;
        text-decoration: none;
      }
      md-filled-text-field {
        display: block;
      }
      .root > *:first-child {
        margin-top: 16px;
      }
      .root > *:not([own-margin]):not(:last-child) {
        margin-bottom: 24px;
      }
    `
];
h([
  p({ attribute: !1 })
], o.prototype, "cardholder", 2);
h([
  p({ attribute: !1 })
], o.prototype, "error", 2);
h([
  p({ type: Boolean })
], o.prototype, "loading", 2);
h([
  v("#save-btn", !0)
], o.prototype, "saveBtn", 2);
o = h([
  g("cardholder-summary")
], o);
var N = Object.defineProperty, E = Object.getOwnPropertyDescriptor, c = (e, t, r, s) => {
  for (var a = s > 1 ? void 0 : s ? E(t, r) : t, i = e.length - 1, d; i >= 0; i--)
    (d = e[i]) && (a = (s ? d(t, r, a) : d(a)) || a);
  return s && a && N(t, r, a), a;
};
let n = class extends m {
  constructor() {
    super(...arguments), this._loading = !1, this._fetchData = new $(
      this,
      async () => {
        let e = 0;
        return await f.postRequest(`/plugins/${this.entry.entry_id}`, {
          action: "get_cardholders",
          user_input: { name: this._filter }
        }).then((t) => {
          this.allCardholders = t.data.result, e = this.allCardholders.length;
        }).catch((t) => {
          var r;
          if (((r = t.response) == null ? void 0 : r.status) === 400)
            throw new Error(t.response.data.detail);
        }), e;
      },
      () => []
    ), this._getFilteredCardholders = C(
      (e, t) => e.filter((r) => {
        var s, a;
        return t ? ((s = r.firstName) == null ? void 0 : s.toLowerCase().includes(t.toLocaleLowerCase())) || ((a = r.lastName) == null ? void 0 : a.toLocaleLowerCase().includes(t.toLocaleLowerCase())) || !1 : r;
      })
    );
  }
  _search(e) {
    e.key === "Enter" && this._filter && this._filter.length >= 3 && this._fetchData.run();
  }
  render() {
    var t;
    const e = this.allCardholders ? this._getFilteredCardholders(this.allCardholders, this._filter) : [];
    return l`
      <pc-card raised .header=${this.entry.title}>
        <div class="card-content">
          <search-input
            label="Search cardholders. Press Enter to fetch more."
            .filter=${this._filter}
            .disabled=${((t = this.allCardholders) == null ? void 0 : t.length) === 0}
            @value-changed=${this._filterChanged}
            @keyup=${this._search}
          ></search-input>
          ${l`${this._fetchData.render({
      pending: () => l`<p>
                <pc-circular-progress
                  indeterminate
                  size="small"
                ></pc-circular-progress>
                Loading Cardholders...
              </p>`,
      complete: (r) => l` ${r === 0 ? l`<p>No cardholders found</p>` : e.length === 0 ? l`<p>No cardholders found. Hit enter to search</p>` : l`<div class="root">
              <md-list>
                ${e.map(
        (s) => l`
                    <md-list-item>
                      <cardholder-summary
                        .cardholder=${s}
                        .loading=${this._loading}
                        @value-changed=${this._updateCardholder}
                      ></cardholder-summary>
                    </md-list-item>
                  `
      )}
              </md-list></div>
            </div>
          </pc-card>
        </div>
      `}`,
      error: (r) => l`<pc-alert
                alert-type="error"
                .header=${r}
              ></pc-alert>`
    })}`}
        </div></pc-card
      >
    `;
  }
  _filterChanged(e) {
    this._filter = e.detail.value;
  }
  async _updateCardholder(e) {
    const t = e.target, r = t.saveBtn;
    this._loading = !0, await f.postRequest(`/plugins/${this.entry.entry_id}`, {
      action: "update_cardholder",
      user_input: e.detail.value
    }).then((s) => {
      s.data.result && (r.disabled = !0);
    }).catch((s) => {
      var a;
      t.error = (a = s.response) == null ? void 0 : a.data.detail;
    }).finally(() => {
      this._loading = !1;
    });
  }
};
n.styles = b;
c([
  p({ attribute: !1 })
], n.prototype, "entry", 2);
c([
  u()
], n.prototype, "allCardholders", 2);
c([
  u()
], n.prototype, "_loading", 2);
c([
  u()
], n.prototype, "_filter", 2);
n = c([
  g("pc-plugin-gallagher_demo")
], n);
export {
  n as PcPluginGallagherDemo
};
