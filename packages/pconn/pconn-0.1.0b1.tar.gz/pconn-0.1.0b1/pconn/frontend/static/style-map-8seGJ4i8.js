import { a6 as l, a7 as a, a8 as u, a9 as c } from "./index-Bs6A-haP.js";
/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const o = "important", d = " !" + o, h = l(class extends a {
  constructor(n) {
    var e;
    if (super(n), n.type !== u.ATTRIBUTE || n.name !== "style" || ((e = n.strings) == null ? void 0 : e.length) > 2) throw Error("The `styleMap` directive must be used in the `style` attribute and must be the only part in the attribute.");
  }
  render(n) {
    return Object.keys(n).reduce((e, s) => {
      const t = n[s];
      return t == null ? e : e + `${s = s.includes("-") ? s : s.replace(/(?:^(webkit|moz|ms|o)|)(?=[A-Z])/g, "-$&").toLowerCase()}:${t};`;
    }, "");
  }
  update(n, [e]) {
    const { style: s } = n.element;
    if (this.ft === void 0) return this.ft = new Set(Object.keys(e)), this.render(e);
    for (const t of this.ft) e[t] == null && (this.ft.delete(t), t.includes("-") ? s.removeProperty(t) : s[t] = null);
    for (const t in e) {
      const r = e[t];
      if (r != null) {
        this.ft.add(t);
        const i = typeof r == "string" && r.endsWith(d);
        t.includes("-") || i ? s.setProperty(t, i ? r.slice(0, -11) : r, i ? o : "") : s[t] = r;
      }
    }
    return c;
  }
});
export {
  h as o
};
