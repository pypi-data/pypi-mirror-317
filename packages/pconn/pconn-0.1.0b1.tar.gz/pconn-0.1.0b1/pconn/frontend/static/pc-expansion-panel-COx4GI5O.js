import { i as f, aa as y, ab as m, t as v, c as p, r as g, l as _, a as b, x as c, A as h, ac as u, s as x } from "./index-Bs6A-haP.js";
const w = (e) => {
  requestAnimationFrame(() => setTimeout(e, 0));
}, C = () => new Promise((e) => {
  w(e);
});
var $ = Object.defineProperty, P = Object.getOwnPropertyDescriptor, T = Object.getPrototypeOf, E = Reflect.get, O = (e, t, r, a) => {
  for (var o = a > 1 ? void 0 : a ? P(t, r) : t, s = e.length - 1, d; s >= 0; s--)
    (d = e[s]) && (o = (a ? d(t, r, o) : d(o)) || o);
  return a && o && $(t, r, o), o;
}, D = (e, t, r) => E(T(e), r, t);
let l = class extends y {
  constructor() {
    super(...arguments), this.attachableTouchController = new m(
      this,
      this._onTouchControlChange.bind(this)
    ), this._handleTouchEnd = () => {
      this.disabled || super.endPressAnimation();
    };
  }
  attach(e) {
    super.attach(e), this.attachableTouchController.attach(e);
  }
  detach() {
    super.detach(), this.attachableTouchController.detach();
  }
  _onTouchControlChange(e, t) {
    e == null || e.removeEventListener("touchend", this._handleTouchEnd), t == null || t.addEventListener("touchend", this._handleTouchEnd);
  }
};
l.styles = [
  ...D(l, l, "styles"),
  f`
      :host {
        --md-ripple-hover-opacity: var(--pc-ripple-hover-opacity, 0.08);
        --md-ripple-pressed-opacity: var(--pc-ripple-pressed-opacity, 0.12);
        --md-ripple-hover-color: var(
          --pc-ripple-hover-color,
          var(--pc-ripple-color, var(--secondary-text-color))
        );
        --md-ripple-pressed-color: var(
          --pc-ripple-pressed-color,
          var(--pc-ripple-color, var(--secondary-text-color))
        );
      }
    `
];
l = O([
  v("pc-ripple")
], l);
var R = Object.defineProperty, j = Object.getOwnPropertyDescriptor, i = (e, t, r, a) => {
  for (var o = a > 1 ? void 0 : a ? j(t, r) : t, s = e.length - 1, d; s >= 0; s--)
    (d = e[s]) && (o = (a ? d(t, r, o) : d(o)) || o);
  return a && o && R(t, r, o), o;
};
let n = class extends b {
  constructor() {
    super(...arguments), this.expanded = !1, this.outlined = !1, this.leftChevron = !1, this._showContent = this.expanded;
  }
  render() {
    return c`
      <div class="top ${h({ expanded: this.expanded })}">
        <div
          id="summary"
          @click=${this._toggleContainer}
          @keydown=${this._toggleContainer}
          @focus=${this._focusChanged}
          @blur=${this._focusChanged}
          role="button"
          tabindex="0"
          aria-expanded=${this.expanded}
          aria-controls="sect1"
        >
          ${this.leftChevron ? c`
                <pc-svg-icon
                  .path=${u}
                  class="summary-icon ${h({ expanded: this.expanded })}"
                ></pc-svg-icon>
              ` : ""}
          <slot name="header">
            <div class="header">
              ${this.header}
              <slot class="secondary" name="secondary">${this.secondary}</slot>
            </div>
          </slot>
          ${this.leftChevron ? "" : c`
                <pc-svg-icon
                  .path=${u}
                  class="summary-icon ${h({ expanded: this.expanded })}"
                ></pc-svg-icon>
              `}
          <pc-ripple .disabled=${this.expanded}></pc-ripple>
        </div>
        <slot name="icons"></slot>
      </div>
      <div
        class="container ${h({ expanded: this.expanded })}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent ? c`<slot></slot>` : ""}
      </div>
    `;
  }
  willUpdate(e) {
    super.willUpdate(e), e.has("expanded") && (this._showContent = this.expanded, setTimeout(() => {
      this._container.style.overflow = this.expanded ? "initial" : "hidden";
    }, 300));
  }
  _handleTransitionEnd() {
    this._container.style.removeProperty("height"), this._container.style.overflow = this.expanded ? "initial" : "hidden", this._showContent = this.expanded;
  }
  async _toggleContainer(e) {
    if (e.defaultPrevented || e.type === "keydown" && e.key !== "Enter" && e.key !== " ")
      return;
    e.preventDefault();
    const t = !this.expanded;
    x(this, "expanded-will-change", { expanded: t }), this._container.style.overflow = "hidden", t && (this._showContent = !0, await C());
    const r = this._container.scrollHeight;
    this._container.style.height = `${r}px`, t || setTimeout(() => {
      this._container.style.height = "0px";
    }, 0), this.expanded = t, x(this, "expanded-changed", { expanded: this.expanded });
  }
  _focusChanged(e) {
    this.shadowRoot.querySelector(".top").classList.toggle(
      "focused",
      e.type === "focus"
    );
  }
};
n.styles = f`
    :host {
      display: block;
    }

    .top {
      display: flex;
      align-items: center;
      border-radius: var(--pc-card-border-radius, 12px);
    }

    .top.expanded {
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }

    .top.focused {
      background: var(--input-fill-color);
    }

    :host([outlined]) {
      box-shadow: none;
      border-width: 1px;
      border-style: solid;
      border-color: var(--outline-color);
      border-radius: var(--pc-card-border-radius, 12px);
    }

    .summary-icon {
      transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
      direction: var(--direction);
      margin-left: 8px;
      margin-inline-start: 8px;
      margin-inline-end: initial;
    }

    :host([leftchevron]) .summary-icon {
      margin-left: 0;
      margin-right: 8px;
      margin-inline-start: 0;
      margin-inline-end: 8px;
    }

    #summary {
      flex: 1;
      display: flex;
      padding: var(--expansion-panel-summary-padding, 0 8px);
      min-height: 48px;
      align-items: center;
      cursor: pointer;
      overflow: hidden;
      font-weight: 500;
      outline: none;
    }

    .summary-icon.expanded {
      transform: rotate(180deg);
    }

    .header,
    ::slotted([slot="header"]) {
      flex: 1;
    }

    .container {
      padding: var(--expansion-panel-content-padding, 0 8px);
      overflow: hidden;
      transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
    }

    .container.expanded {
      height: auto;
    }

    .secondary {
      display: block;
      color: var(--secondary-text-color);
      font-size: 12px;
    }
  `;
i([
  p({ type: Boolean, reflect: !0 })
], n.prototype, "expanded", 2);
i([
  p({ type: Boolean, reflect: !0 })
], n.prototype, "outlined", 2);
i([
  p({ attribute: !1, type: Boolean, reflect: !0 })
], n.prototype, "leftChevron", 2);
i([
  p()
], n.prototype, "header", 2);
i([
  p()
], n.prototype, "secondary", 2);
i([
  g()
], n.prototype, "_showContent", 2);
i([
  _(".container")
], n.prototype, "_container", 2);
n = i([
  v("pc-expansion-panel")
], n);
