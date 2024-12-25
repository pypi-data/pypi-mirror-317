import { p, i as h, r as d, a as u, h as g, b as v, x as n, m, n as f, t as _ } from "./index-Bs6A-haP.js";
import "./search-input-B3lTuQnQ.js";
import "./pc-settings-C9AXcJ5E.js";
var $ = Object.defineProperty, b = Object.getOwnPropertyDescriptor, c = (e, t, i, l) => {
  for (var s = l > 1 ? void 0 : l ? b(t, i) : t, a = e.length - 1, o; a >= 0; a--)
    (o = e[a]) && (s = (l ? o(t, i, s) : o(s)) || s);
  return l && s && $(t, i, s), s;
};
let r = class extends u {
  constructor() {
    super(...arguments), this._filter = "", this.pluginEntries = [], this._fetchData = new g(
      this,
      async () => {
        var e;
        await ((e = v) == null ? void 0 : e.getRequest("/plugins/workstation_entries").then((t) => {
          this.pluginEntries = t.data.result;
        }));
      },
      () => []
    );
  }
  render() {
    var t;
    const e = (t = this.pluginEntries) == null ? void 0 : t.filter(
      (i) => i.title.toLowerCase().includes(this._filter.toLowerCase())
    );
    return n`
      ${this._fetchData.render({
      complete: () => n` ${this.pluginEntries.length === 0 ? n`
                <div class="content">
                  <h2>No plugins available. Check the configuration tab.</h2>
                  <md-text-button href="/settings/plugins"
                    >Go to plugin entries</md-text-button
                  >
                </div>
              ` : n`<pc-card header="Installed Plugins">
                <div class="card-content">
                  <search-input
                    label="Search Plugins"
                    .filter=${this._filter}
                    @value-changed=${this._filterChanged}
                  ></search-input>
                  <div class="root">
                    <md-list role="button">
                      ${e.map(
        (i) => n`<md-list-item
                            type="button"
                            .pluginEntry=${i}
                            @click=${this._handleSelection}
                          >
                            <div slot="headline">${i.title}</div>
                            <div slot="end">
                              <pc-svg-icon
                                .path=${m}
                              ></pc-svg-icon>
                            </div>
                          </md-list-item>`
      )}
                    </md-list>
                  </div>
                </div>
              </pc-card>`}`
    })}
    `;
  }
  _filterChanged(e) {
    this._filter = e.detail.value;
  }
  _handleSelection(e) {
    const t = e.target.closest("md-list-item").pluginEntry, i = `/plugins/${t.domain}/${t.entry_id}`;
    f(i);
  }
};
r.styles = [
  p,
  h`
      pc-card {
        margin: auto;
        width: 600px;
      }
    `
];
c([
  d()
], r.prototype, "_filter", 2);
r = c([
  _("pc-plugins")
], r);
export {
  r as Plugins
};
