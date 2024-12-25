import { p as o, a as m, h as c, b as p, x as d, t as u } from "./index-Bs6A-haP.js";
import "./filled-button-DK7nEDMp.js";
import "./pc-expansion-panel-COx4GI5O.js";
import { s as h } from "./styles-BLMRQn28.js";
var v = Object.defineProperty, _ = Object.getOwnPropertyDescriptor, f = (t, e, l, i) => {
  for (var s = i > 1 ? void 0 : i ? _(e, l) : e, n = t.length - 1, r; n >= 0; n--)
    (r = t[n]) && (s = (i ? r(e, l, s) : r(s)) || s);
  return i && s && v(e, l, s), s;
};
let a = class extends m {
  constructor() {
    super(...arguments), this._fetchData = new c(
      this,
      async () => (await p.getRequest("/config/system")).data.result,
      () => []
    );
  }
  render() {
    return d`
      <pc-card outlined header="Platform Connectors">
        ${this._fetchData.render({
      complete: (t) => d`
            <div class="card-content">
              <md-list>
                <md-list-item>
                  <div slot="headline">Version <b>${t.version}</b></div>

                  <md-filled-button slot="end" @click=${this._updateLicense}
                    >UPDATE LICENSE</md-filled-button
                  >
                </md-list-item>
                <md-list-item>
                  <div slot="headline">Workstations</div>
                  <div slot="end">
                    ${t.assigned_workstations}/${t.licensed_workstations}
                  </div>
                </md-list-item>
                <md-list-item>
                  <pc-expansion-panel header="Plugins">
                    <md-list
                      >${t.plugins.map(
        (e) => d`<md-list-item>${e}</md-list-item>`
      )}</md-list
                    >
                  </pc-expansion-panel>
                </md-list-item>
              </md-list>
            </div>
          `
    })}
      </pc-card>
    `;
  }
  _updateLicense() {
    import("./pc-license-BsER0U1K.js").then(() => {
      var e;
      const t = document.createElement("pc-license");
      t.allowClose = !0, (e = this.shadowRoot) == null || e.appendChild(t);
    });
  }
};
a.styles = [o, h];
a = f([
  u("pc-settings-system")
], a);
export {
  a as SystemSettings
};
