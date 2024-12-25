import { k as b, i as _, c as m, r as p, l as v, a as g, x as o, o as k, b as h, s as f, t as w, p as $, h as D, P as y, E as C, Q as S, F as O, R as x, n as P } from "./index-Bs6A-haP.js";
import "./filled-button-DK7nEDMp.js";
import "./pc-button-menu-BrK2NJOx.js";
import { m as I } from "./memoize-one.esm-DezIwejE.js";
import "./pc-circular-progress-CXHtR8Ql.js";
import "./search-input-B3lTuQnQ.js";
import "./checkbox-Di7w86SP.js";
import "./outlined-text-field-BKI7dxSQ.js";
import "./pc-form-CK-FZij5.js";
import { c as W } from "./styles-CmkOrDPY.js";
import { s as E } from "./styles-BLMRQn28.js";
var R = Object.defineProperty, q = Object.getOwnPropertyDescriptor, d = (t, e, s, a) => {
  for (var i = a > 1 ? void 0 : a ? q(e, s) : e, n = t.length - 1, l; n >= 0; n--)
    (l = t[n]) && (i = (a ? l(e, s, i) : l(i)) || i);
  return a && i && R(e, s, i), i;
};
const N = (t) => [
  {
    name: "name",
    required: !0,
    selector: {
      text: {
        type: "text",
        autocomplete: "on"
      }
    }
  },
  {
    name: "ip_address",
    required: !0,
    disabled: t,
    selector: {
      text: {
        type: "text",
        autocomplete: "on"
      }
    }
  },
  {
    name: "dashboard_only",
    required: !1,
    selector: {
      boolean: {}
    }
  }
], T = {
  name: "Name",
  ip_address: "IP Address",
  dashboard_only: "Dashboard only"
};
let r = class extends g {
  constructor() {
    super(...arguments), this.isCurrentWS = !1, this._loading = !1;
  }
  _preventClose(t) {
    t.target.returnValue !== "close" && t.preventDefault();
  }
  async _closeDialog() {
    var t;
    await ((t = this.dialog) == null ? void 0 : t.close("close"));
  }
  render() {
    const t = this._stepDataProcessed;
    return o`
      <pc-dialog open @close=${this._preventClose}>
        <div slot="headline">
          Configure Workstation
          <pc-icon-button
            label="Close"
            .path=${k}
            @click=${this._closeDialog}
          ></pc-icon-button>
        </div>
        <div slot="content" class="content">
          ${this._errorMsg ? o`<div class="error">
                <pc-alert
                  alert-type="error"
                  .header=${this._errorMsg}
                ></pc-alert>
              </div>` : ""}
          <pc-form
            .data=${t}
            @value-changed=${this._stepDataChanged}
            .schema=${N(this.isCurrentWS)}
            .labels=${T}
            .disabled=${this._loading}
          >
          </pc-form>
        </div>
        <div slot="actions" class="buttons">
          ${this._loading ? o`<pc-circular-progress indeterminate></pc-circular-progress>` : o` <md-filled-button @click=${this._handleSubmit}
                >Submit
              </md-filled-button>`}
        </div>
      </pc-dialog>
    `;
  }
  _stepDataChanged(t) {
    this._stepData = t.detail.value;
  }
  get _stepDataProcessed() {
    return this._stepData !== void 0 ? this._stepData : (this._stepData = {
      name: this.workstation.name,
      ip_address: this.workstation.ip,
      dashboard_only: this.workstation.dashboard_only ?? !1
    }, this._stepData);
  }
  async _handleSubmit(t) {
    t.stopPropagation(), this._loading = !0, await h.postRequest("/config/workstations", {
      action: "update",
      data: { id: this.workstation.id, ...this._stepData }
    }).then(() => {
      var e;
      (e = this.dialog) == null || e.close("close"), f(this, "data-updated", {
        data: this._stepData
      });
    }).catch((e) => {
      var s;
      this._errorMsg = (s = e.response) == null ? void 0 : s.data.detail;
    }).finally(() => {
      this._loading = !1;
    });
  }
};
r.styles = [
  b,
  W,
  _`
      .init-spinner {
        padding: 50px 100px;
        text-align: center;
      }
      pc-circular-progress {
        margin-top: 16px;
      }
      md-outlined-text-field {
        display: block;
      }
    `
];
d([
  m({ attribute: !1 })
], r.prototype, "workstation", 2);
d([
  m({ attribute: !1 })
], r.prototype, "isCurrentWS", 2);
d([
  p()
], r.prototype, "_errorMsg", 2);
d([
  p()
], r.prototype, "_stepData", 2);
d([
  p()
], r.prototype, "_loading", 2);
d([
  v("pc-dialog")
], r.prototype, "dialog", 2);
r = d([
  w("step-workstation-update")
], r);
var F = Object.defineProperty, L = Object.getOwnPropertyDescriptor, u = (t, e, s, a) => {
  for (var i = a > 1 ? void 0 : a ? L(e, s) : e, n = t.length - 1, l; n >= 0; n--)
    (l = t[n]) && (i = (a ? l(e, s, i) : l(i)) || i);
  return a && i && F(e, s, i), i;
};
let c = class extends g {
  constructor() {
    super(...arguments), this._filter = "", this._loading = !1, this._fetchData = new D(
      this,
      async () => {
        var e;
        const t = await h.getRequest(
          "/config/workstations/registered"
        );
        return this._workstationInfo = t.data.result, (e = this._workstationInfo) == null ? void 0 : e.workstations;
      },
      () => []
    ), this._getFilteredItems = I(
      (t, e) => t.filter((s) => e ? s.name.toLowerCase().includes(e) : s)
    );
  }
  render() {
    var e;
    const t = this._workstationInfo ? this._getFilteredItems(
      this._workstationInfo.workstations,
      this._filter.toLowerCase()
    ) : [];
    return o`
      <pc-card outlined header="Workstations">
        <div class="card-content">
          <div class="layout horizontal center">
            <search-input
              label="Search workstations"
              .filter=${this._filter}
              .disabled=${((e = this._workstationInfo) == null ? void 0 : e.workstations.length) === 0}
              @value-changed=${this._filterChanged}
            ></search-input>
            <pc-icon-button
              .path=${y}
              @click=${this._fetchData.run}
            ></pc-icon-button>
          </div>
          ${this._fetchData.render({
      pending: () => o`<div>Fetching workstations...</div>`,
      complete: (s) => o` ${s.length === 0 ? o` <p>No workstations found</p> ` : t.length === 0 && this._filter ? o`<div>
                      ${"No workstation found called '" + this._filter + "'"}
                    </div>` : o`<div class="root">
                      <md-list role="menu"
                        >${t.map(
        (a) => {
          var i, n;
          return o`
                            <md-list-item
                              role="menuitem"
                              class="ws"
                              .ws=${a}
                            >
                              ${a.name}
                              ${a.id === ((i = this._workstationInfo) == null ? void 0 : i.current_ws.id) ? o`<div slot="supporting-text">
                                    Current workstation
                                  </div>` : ""}
                              ${this._loading && a.disabled ? o`<pc-circular-progress
                                    slot="end"
                                    indeterminate
                                  ></pc-circular-progress>` : a.disabled ? o`<md-filled-button
                                      unelevated
                                      slot="end"
                                      @click=${this._handleEnable}
                                      >ENABLE
                                    </md-filled-button>` : o`<md-text-button
                                      slot="end"
                                      @click=${this._showOptions}
                                      >CONFIGURE
                                    </md-text-button>`}
                              ${a.id === ((n = this._workstationInfo) == null ? void 0 : n.current_ws.id) ? "" : o` <pc-button-menu slot="end">
                                    <pc-icon-button
                                      slot="trigger"
                                      label="Menu"
                                      .path=${C}
                                    ></pc-icon-button>

                                    ${a.disabled ? o`<md-menu-item
                                          @close-menu=${this._handleEnable}
                                        >
                                          <div slot="headline">Enable</div>
                                          <pc-svg-icon
                                            slot="start"
                                            .path=${S}
                                          ></pc-svg-icon>
                                        </md-menu-item>` : o`<md-menu-item
                                          @close-menu=${this._handleDisable}
                                        >
                                          <div slot="headline">Disable</div>
                                          <pc-svg-icon
                                            slot="start"
                                            class="warning"
                                            .path=${O}
                                          ></pc-svg-icon>
                                        </md-menu-item>`}
                                    <md-menu-item
                                      @close-menu=${this._handleDelete}
                                    >
                                      <div slot="headline">Delete</div>
                                      <pc-svg-icon
                                        slot="start"
                                        class="warning"
                                        .path=${x}
                                      ></pc-svg-icon>
                                    </md-menu-item>
                                  </pc-button-menu>`}
                            </md-list-item>
                          `;
        }
      )}</md-list
                      >
                    </div>`}`
    })}
        </div>
      </pc-card>
    `;
  }
  _filterChanged(t) {
    this._filter = t.detail.value;
  }
  async _handleEnable(t) {
    await this._enableDisableWorkstation(
      t.target.closest(".ws").ws,
      !1
    );
  }
  async _handleDisable(t) {
    confirm("This will disable all related plugin entries.") && await this._enableDisableWorkstation(
      t.target.closest(".ws").ws,
      !0
    );
  }
  async _handleDelete(t) {
    confirm("This will remove all related plugin entries.") && await this._deleteWorkstation(
      t.target.closest(".ws").ws
    );
  }
  async _enableDisableWorkstation(t, e) {
    this._loading = !0, await h.postRequest("/config/workstations", {
      action: "disable",
      data: {
        id: t.id,
        disabled_by: e ? "workstation" : null
      }
    }).catch((s) => {
      var a, i;
      ((a = s.response) == null ? void 0 : a.status) === 400 && alert((i = s.response) == null ? void 0 : i.data.detail);
    }), await this._fetchData.run(), this._loading = !1;
  }
  async _deleteWorkstation(t) {
    this._loading = !0, await h.postRequest("/config/workstations", {
      action: "delete",
      data: { id: t.id }
    }).catch((e) => {
      var s, a;
      ((s = e.response) == null ? void 0 : s.status) === 400 && alert((a = e.response) == null ? void 0 : a.data.detail);
    }), await this._fetchData.run(), this._loading = !1;
  }
  _showOptions(t) {
    var a, i;
    const e = t.target.closest(".ws").ws, s = document.createElement("step-workstation-update");
    s.workstation = e, s.isCurrentWS = ((a = this._workstationInfo) == null ? void 0 : a.current_ws.id) === e.id, s.addEventListener(
      "data-updated",
      (n) => this._workstationUpdated(
        n
      )
    ), (i = this.shadowRoot) == null || i.appendChild(s);
  }
  _workstationUpdated(t) {
    var e;
    t.currentTarget.workstation.id === ((e = this._workstationInfo) == null ? void 0 : e.current_ws.id) && t.detail.data.dashboard_only ? (alert("You will be redirected to the home page."), P("/plugins", { replace: !0 })) : this._fetchData.run(), f(this, "config-updated");
  }
};
c.styles = [
  $,
  E,
  _`
      search-input {
        flex-grow: 1;
      }
    `
];
u([
  p()
], c.prototype, "_filter", 2);
u([
  p()
], c.prototype, "_loading", 2);
c = u([
  w("pc-settings-workstations")
], c);
export {
  c as PcWorkstationSettings
};
