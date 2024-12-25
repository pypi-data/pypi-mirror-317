import { p as r, i as l, a as d, x as p, n as g, t as h, d as m, e as P, f as u, g as v } from "./index-Bs6A-haP.js";
var f = Object.defineProperty, _ = Object.getOwnPropertyDescriptor, C = (s, e, i, n) => {
  for (var t = n > 1 ? void 0 : n ? _(e, i) : e, a = s.length - 1, o; a >= 0; a--)
    (o = s[a]) && (t = (n ? o(e, i, t) : o(t)) || t);
  return n && t && f(e, i, t), t;
};
const S = [
  {
    path: "/settings/plugins",
    name: "Plugin Entries",
    description: "Add and configure Plugins",
    iconPath: m,
    iconColor: "#0D47A1"
  },
  {
    path: "/settings/workstations",
    name: "Workstations",
    description: "Manage Workstations",
    iconPath: P,
    iconColor: "#301ABE"
  },
  {
    path: "/settings/logs",
    name: "Logs",
    description: "View and search logs to troubleshoot",
    iconPath: u,
    iconColor: "#C65326"
  },
  {
    path: "/settings/system",
    name: "System",
    description: "View system and license details",
    iconPath: v,
    iconColor: "#4A5963"
  }
];
let c = class extends d {
  render() {
    return p`<pc-card raised>
      <pc-navigation-list
        class="card-content"
        .pages=${S}
        hasSecondary
        @location-changed=${this._handleSelection}
      ></pc-navigation-list>
    </pc-card>`;
  }
  _handleSelection(s) {
    g(s.detail.path);
  }
};
c.styles = [
  r,
  l`
      pc-card {
        margin: auto;
        width: 600px;
      }
    `
];
c = C([
  h("pc-settings")
], c);
