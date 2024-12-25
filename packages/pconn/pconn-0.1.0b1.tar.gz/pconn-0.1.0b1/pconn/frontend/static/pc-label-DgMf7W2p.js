import { t as n, a as p, x as s, i as x } from "./index-Bs6A-haP.js";
var b = Object.defineProperty, d = Object.getOwnPropertyDescriptor, g = (i, l, o, e) => {
  for (var r = e > 1 ? void 0 : e ? d(l, o) : l, t = i.length - 1, a; t >= 0; t--)
    (a = i[t]) && (r = (e ? a(l, o, r) : a(r)) || r);
  return e && r && b(l, o, r), r;
};
let c = class extends p {
  render() {
    return s`
      <span class="label">
        <slot name="icon"></slot>
        <slot></slot>
      </span>
    `;
  }
  static get styles() {
    return [
      x`
        :host {
          --pc-label-text-color: var(--primary-text-color);
          --pc-label-icon-color: var(--primary-text-color);
          --pc-label-background-color: rgba(
            var(--rgb-primary-text-color),
            0.15
          );
        }
        .label {
          display: inline-flex;
          flex-direction: row;
          align-items: center;
          font-size: 16px;
          font-weight: 500;
          line-height: 16px;
          letter-spacing: 0.1px;
          vertical-align: middle;
          height: 32px;
          padding: 0 16px;
          border-radius: 18px;
          background-color: var(--pc-label-background-color);
          color: var(--pc-label-text-color);
          --md-icon-button-icon-size: 24px;
        }
        ::slotted([slot="icon"]) {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          margin-right: 16px;
          margin-left: -8px;
          display: flex;
          color: var(--pc-label-icon-color);
        }
        span {
          display: inline-flex;
        }
      `
    ];
  }
};
c = g([
  n("pc-label")
], c);
