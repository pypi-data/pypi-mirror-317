import { p as g, i as h, r as p, a as v, h as _, b as d, x as l, P as f, U as w, t as L } from "./index-Bs6A-haP.js";
import "./filled-button-DK7nEDMp.js";
import "./pc-select-Cl_dw0CS.js";
import { m as a } from "./memoize-one.esm-DezIwejE.js";
import "./pc-circular-progress-CXHtR8Ql.js";
import "./pc-selector-text-G95jpLoy.js";
import "./search-input-B3lTuQnQ.js";
import { s as b } from "./styles-BLMRQn28.js";
import { L as u, a as C } from "./format_date_time-CG_oC5lZ.js";
const $ = (e, o = "") => {
  const t = document.createElement("a");
  t.target = "_blank", t.href = e, t.download = o, document.body.appendChild(t), t.click(), document.body.removeChild(t);
};
a(
  () => new Intl.DateTimeFormat("en-GB", {
    hour: "numeric",
    minute: "2-digit",
    hourCycle: "h23",
    timeZone: u
  })
);
const y = (e) => D().format(e), D = a(
  () => new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
    timeZone: u
  })
);
a(
  () => new Intl.DateTimeFormat("en-GB", {
    weekday: "long",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
    timeZone: u
  })
);
a(
  () => (
    // en-GB to fix Chrome 24:59 to 0:59 https://stackoverflow.com/a/60898146
    new Intl.DateTimeFormat("en-GB", {
      hour: "numeric",
      minute: "2-digit",
      hour12: !1,
      timeZone: u
    })
  )
);
const x = (e) => {
  const o = (/* @__PURE__ */ new Date()).setHours(0, 0, 0, 0), t = new Date(e * 1e3);
  return new Date(e * 1e3).setHours(0, 0, 0, 0) < o ? C(t) : y(t);
};
var S = Object.defineProperty, T = Object.getOwnPropertyDescriptor, c = (e, o, t, s) => {
  for (var i = s > 1 ? void 0 : s ? T(o, t) : o, r = e.length - 1, m; r >= 0; r--)
    (m = e[r]) && (i = (s ? m(o, t, i) : m(i)) || i);
  return s && i && S(o, t, i), i;
};
const F = [
  { value: "critical", label: "Critical" },
  { value: "error", label: "Error" },
  { value: "warning", label: "Warning" },
  { value: "info", label: "Info" },
  { value: "debug", label: "Debug" }
], I = (e) => {
  if (e.name.startsWith("pconn.plugins."))
    return e.name.split(".")[2];
  if (e.source[0].startsWith("pconn/plugins/"))
    return e.source[0].split("/")[2];
};
let n = class extends v {
  constructor() {
    super(...arguments), this._filter = "", this._loading = !1, this._fetchData = new _(
      this,
      async () => {
        const o = (await d.getRequest("/logs")).data.result;
        for (const t of o)
          t.level = t.level.toLowerCase();
        return this._items = o, o;
      },
      () => []
    ), this._getFilteredItems = a(
      (e, o) => e.filter((t) => o ? t.message.some(
        (s) => s.toLowerCase().includes(o)
      ) || t.source[0].toLowerCase().includes(o) || t.name.toLowerCase().includes(o) || this._timestamp(t).toLowerCase().includes(o) : t)
    );
  }
  _timestamp(e) {
    return x(e.timestamp);
  }
  render() {
    var t;
    const e = this._items ? this._getFilteredItems(this._items, this._filter.toLowerCase()) : [], o = e.length ? e.map((s) => I(s)) : [];
    return l`<div class="root">
      <pc-card outlined header="Logger Settings">
        <div class="card-content">
          <div class="row">
            <md-filled-text-field
              label="Component"
              placeholder="pconn.plugins.demo"
              .required=${!0}
              @input=${this._updateComponent}
            ></md-filled-text-field>
            <pc-select label="Log levels" .required=${!0}>
              ${F.map(
      (s) => l`<md-select-option
                    value=${s.value}
                    @request-selection=${this._logLevelChanged}
                  >
                    <div slot="headline">${s.label}</div>
                  </md-select-option>`
    )}
            </pc-select>
          </div>
        </div>
        <div class="card-actions right">
          ${this._loading ? l`<pc-circular-progress indeterminate></pc-circular-progress>` : l` <md-text-button
                @click=${this._updateComponentLogLevel}
                .disabled=${!this._selectedComponent || !this._selectedLogLevel}
              >
                SAVE
              </md-text-button>`}
          <md-text-button outlined @click=${this._resetLogs}>
            RESET LOGS
          </md-text-button>
        </div>
      </pc-card>
      <pc-card outlined header="Logs">
        <div class="card-content">
          <div class="layout horizontal center-center">
            <search-input
              label="Search logs"
              .filter=${this._filter}
              .disabled=${((t = this._items) == null ? void 0 : t.length) === 0}
              @value-changed=${this._filterChanged}
            ></search-input>
            <pc-icon-button
              .path=${f}
              @click=${this._updateLogs}
            ></pc-icon-button>
          </div>
          ${this._fetchData.render({
      pending: () => l`<div>Fetching logs...</div>`,
      complete: (s) => l` ${s.length === 0 ? l` <p>No issues found</p> ` : e.length === 0 && this._filter ? l`<div>
                      ${"No logs found for '" + this._filter + "'"}
                    </div>` : l`<div class="root">
                      <md-list
                        >${e.map(
        (i, r) => l`
                            <md-list-item>
                              <div slot="headline">${i.message}</div>

                              <div slot="supporting-text">
                                ${this._timestamp(i)} – (<span
                                  class=${i.level}
                                  >${i.level.toUpperCase()}</span
                                >) ${o[r] || i.source[0]}
                              </div>
                            </md-list-item>
                          `
      )}</md-list
                      >
                    </div>`}`
    })}
        </div>
        <div class="card-actions">
          <md-filled-button outlined @click=${this._downloadLogFile}>
            <pc-svg-icon .path=${w}></pc-svg-icon>
            Download Logs
          </md-filled-button>
        </div></pc-card
      >
    </div>`;
  }
  _filterChanged(e) {
    this._filter = e.detail.value;
  }
  _updateLogs() {
    this._fetchData.run();
  }
  async _downloadLogFile() {
    const o = `gallagher_plugins_${(/* @__PURE__ */ new Date()).toISOString().replace(/:/g, "-")}.log`, t = await d.getFile("/logs/download"), s = window.URL.createObjectURL(t.data);
    $(s, o);
  }
  _updateComponent(e) {
    this._selectedComponent = e.target.value;
  }
  _logLevelChanged(e) {
    var o;
    this._selectedLogLevel = (o = e.target) == null ? void 0 : o.value;
  }
  async _updateComponentLogLevel() {
    this._loading = !0, await d.postRequest("/config/logs/set_level", {
      component: this._selectedComponent,
      level: this._selectedLogLevel,
      save: !0
    }), this._loading = !1;
  }
  async _resetLogs() {
    await d.postRequest("/config/logs/reset_levels");
  }
};
n.styles = [
  g,
  b,
  h`
      .row {
        display: flex;
        justify-content: space-between;
      }
      .row > * {
        flex: 1;
        margin: 0 8px;
      }
      .card-actions {
        display: flex;
        justify-content: space-between;
        flex-direction: row-reverse;
      }
      .error {
        color: var(--error-color);
      }

      .warning {
        color: var(--warning-color);
      }
      search-input {
        display: block;
        flex-grow: 1;
      }
    `
];
c([
  p()
], n.prototype, "_filter", 2);
c([
  p()
], n.prototype, "_selectedComponent", 2);
c([
  p()
], n.prototype, "_selectedLogLevel", 2);
c([
  p()
], n.prototype, "_items", 2);
n = c([
  L("pc-logs")
], n);
export {
  n as PcLogs
};
