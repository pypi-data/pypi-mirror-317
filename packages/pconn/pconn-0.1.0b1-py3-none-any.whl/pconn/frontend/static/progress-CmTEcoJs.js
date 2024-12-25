import { J as o, _ as e, c as r, K as i, L as n, M as l, N as t } from "./index-Bs6A-haP.js";
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const u = o(i);
class a extends u {
  constructor() {
    super(...arguments), this.value = 0, this.max = 1, this.indeterminate = !1, this.fourColor = !1;
  }
  render() {
    const { ariaLabel: s } = this;
    return n`
      <div
        class="progress ${l(this.getRenderClasses())}"
        role="progressbar"
        aria-label="${s || t}"
        aria-valuemin="0"
        aria-valuemax=${this.max}
        aria-valuenow=${this.indeterminate ? t : this.value}
        >${this.renderIndicator()}</div
      >
    `;
  }
  getRenderClasses() {
    return {
      indeterminate: this.indeterminate,
      "four-color": this.fourColor
    };
  }
}
e([
  r({ type: Number })
], a.prototype, "value", void 0);
e([
  r({ type: Number })
], a.prototype, "max", void 0);
e([
  r({ type: Boolean })
], a.prototype, "indeterminate", void 0);
e([
  r({ type: Boolean, attribute: "four-color" })
], a.prototype, "fourColor", void 0);
export {
  a as P
};
