var gt = Object.defineProperty;
var mt = (n, t, e) => t in n ? gt(n, t, { enumerable: !0, configurable: !0, writable: !0, value: e }) : n[t] = e;
var h = (n, t, e) => mt(n, typeof t != "symbol" ? t + "" : t, e);
import { Z as bt, y as Z, z as N, w as J, T as X, x as y, _ as O, c as v, a as Y, G as tt, p as ot, i as ht, h as at, b as W, s as U, H as yt, t as ct, I as wt, r as q, l as ut } from "./index-Bs6A-haP.js";
import "./outlined-text-field-BKI7dxSQ.js";
import "./search-input-B3lTuQnQ.js";
import "./filled-text-field-qW71ccQt.js";
import "./pc-circular-progress-CXHtR8Ql.js";
import "./pc-expansion-panel-COx4GI5O.js";
import "./pc-label-DgMf7W2p.js";
/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { I: vt } = bt, xt = (n) => n.strings === void 0, et = () => document.createComment(""), z = (n, t, e) => {
  var r;
  const s = n._$AA.parentNode, i = t === void 0 ? n._$AB : t._$AA;
  if (e === void 0) {
    const l = s.insertBefore(et(), i), a = s.insertBefore(et(), i);
    e = new vt(l, a, n, n.options);
  } else {
    const l = e._$AB.nextSibling, a = e._$AM, o = a !== n;
    if (o) {
      let u;
      (r = e._$AQ) == null || r.call(e, n), e._$AM = n, e._$AP !== void 0 && (u = n._$AU) !== a._$AU && e._$AP(u);
    }
    if (l !== i || o) {
      let u = e._$AA;
      for (; u !== l; ) {
        const g = u.nextSibling;
        s.insertBefore(u, i), u = g;
      }
    }
  }
  return e;
}, k = (n, t, e = n) => (n._$AI(t, e), n), St = {}, kt = (n, t = St) => n._$AH = t, Ct = (n) => n._$AH, j = (n) => {
  var s;
  (s = n._$AP) == null || s.call(n, !1, !0);
  let t = n._$AA;
  const e = n._$AB.nextSibling;
  for (; t !== e; ) {
    const i = t.nextSibling;
    t.remove(), t = i;
  }
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const I = (n, t) => {
  var s;
  const e = n._$AN;
  if (e === void 0) return !1;
  for (const i of e) (s = i._$AO) == null || s.call(i, t, !1), I(i, t);
  return !0;
}, T = (n) => {
  let t, e;
  do {
    if ((t = n._$AM) === void 0) break;
    e = t._$AN, e.delete(n), n = t;
  } while ((e == null ? void 0 : e.size) === 0);
}, dt = (n) => {
  for (let t; t = n._$AM; n = t) {
    let e = t._$AN;
    if (e === void 0) t._$AN = e = /* @__PURE__ */ new Set();
    else if (e.has(n)) break;
    e.add(n), Rt(t);
  }
};
function $t(n) {
  this._$AN !== void 0 ? (T(this), this._$AM = n, dt(this)) : this._$AM = n;
}
function Et(n, t = !1, e = 0) {
  const s = this._$AH, i = this._$AN;
  if (i !== void 0 && i.size !== 0) if (t) if (Array.isArray(s)) for (let r = e; r < s.length; r++) I(s[r], !1), T(s[r]);
  else s != null && (I(s, !1), T(s));
  else I(this, n);
}
const Rt = (n) => {
  n.type == N.CHILD && (n._$AP ?? (n._$AP = Et), n._$AQ ?? (n._$AQ = $t));
};
class Lt extends Z {
  constructor() {
    super(...arguments), this._$AN = void 0;
  }
  _$AT(t, e, s) {
    super._$AT(t, e, s), dt(this), this.isConnected = t._$AU;
  }
  _$AO(t, e = !0) {
    var s, i;
    t !== this.isConnected && (this.isConnected = t, t ? (s = this.reconnected) == null || s.call(this) : (i = this.disconnected) == null || i.call(this)), e && (I(this, t), T(this));
  }
  setValue(t) {
    if (xt(this._$Ct)) this._$Ct._$AI(t, this);
    else {
      const e = [...this._$Ct._$AH];
      e[this._$Ci] = t, this._$Ct._$AI(e, this, 0);
    }
  }
  disconnected() {
  }
  reconnected() {
  }
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const st = (n, t, e) => {
  const s = /* @__PURE__ */ new Map();
  for (let i = t; i <= e; i++) s.set(n[i], i);
  return s;
}, At = J(class extends Z {
  constructor(n) {
    if (super(n), n.type !== N.CHILD) throw Error("repeat() can only be used in text expressions");
  }
  dt(n, t, e) {
    let s;
    e === void 0 ? e = t : t !== void 0 && (s = t);
    const i = [], r = [];
    let l = 0;
    for (const a of n) i[l] = s ? s(a, l) : l, r[l] = e(a, l), l++;
    return { values: r, keys: i };
  }
  render(n, t, e) {
    return this.dt(n, t, e).values;
  }
  update(n, [t, e, s]) {
    const i = Ct(n), { values: r, keys: l } = this.dt(t, e, s);
    if (!Array.isArray(i)) return this.ut = l, r;
    const a = this.ut ?? (this.ut = []), o = [];
    let u, g, _ = 0, f = i.length - 1, d = 0, p = r.length - 1;
    for (; _ <= f && d <= p; ) if (i[_] === null) _++;
    else if (i[f] === null) f--;
    else if (a[_] === l[d]) o[d] = k(i[_], r[d]), _++, d++;
    else if (a[f] === l[p]) o[p] = k(i[f], r[p]), f--, p--;
    else if (a[_] === l[p]) o[p] = k(i[_], r[p]), z(n, o[p + 1], i[_]), _++, p--;
    else if (a[f] === l[d]) o[d] = k(i[f], r[d]), z(n, i[_], i[f]), f--, d++;
    else if (u === void 0 && (u = st(l, d, p), g = st(a, _, f)), u.has(a[_])) if (u.has(a[f])) {
      const m = g.get(l[d]), A = m !== void 0 ? i[m] : null;
      if (A === null) {
        const V = z(n, i[_]);
        k(V, r[d]), o[d] = V;
      } else o[d] = k(A, r[d]), z(n, i[_], A), i[m] = null;
      d++;
    } else j(i[f]), f--;
    else j(i[_]), _++;
    for (; d <= p; ) {
      const m = z(n, o[p + 1]);
      k(m, r[d]), o[d++] = m;
    }
    for (; _ <= f; ) {
      const m = i[_++];
      m !== null && j(m);
    }
    return this.ut = l, kt(n, o), X;
  }
});
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class H extends Event {
  constructor(t) {
    super(H.eventName, { bubbles: !1 }), this.first = t.first, this.last = t.last;
  }
}
H.eventName = "rangeChanged";
class D extends Event {
  constructor(t) {
    super(D.eventName, { bubbles: !1 }), this.first = t.first, this.last = t.last;
  }
}
D.eventName = "visibilityChanged";
class F extends Event {
  constructor() {
    super(F.eventName, { bubbles: !1 });
  }
}
F.eventName = "unpinned";
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class zt {
  constructor(t) {
    this._element = null;
    const e = t ?? window;
    this._node = e, t && (this._element = t);
  }
  get element() {
    return this._element || document.scrollingElement || document.documentElement;
  }
  get scrollTop() {
    return this.element.scrollTop || window.scrollY;
  }
  get scrollLeft() {
    return this.element.scrollLeft || window.scrollX;
  }
  get scrollHeight() {
    return this.element.scrollHeight;
  }
  get scrollWidth() {
    return this.element.scrollWidth;
  }
  get viewportHeight() {
    return this._element ? this._element.getBoundingClientRect().height : window.innerHeight;
  }
  get viewportWidth() {
    return this._element ? this._element.getBoundingClientRect().width : window.innerWidth;
  }
  get maxScrollTop() {
    return this.scrollHeight - this.viewportHeight;
  }
  get maxScrollLeft() {
    return this.scrollWidth - this.viewportWidth;
  }
}
class It extends zt {
  constructor(t, e) {
    super(e), this._clients = /* @__PURE__ */ new Set(), this._retarget = null, this._end = null, this.__destination = null, this.correctingScrollError = !1, this._checkForArrival = this._checkForArrival.bind(this), this._updateManagedScrollTo = this._updateManagedScrollTo.bind(this), this.scrollTo = this.scrollTo.bind(this), this.scrollBy = this.scrollBy.bind(this);
    const s = this._node;
    this._originalScrollTo = s.scrollTo, this._originalScrollBy = s.scrollBy, this._originalScroll = s.scroll, this._attach(t);
  }
  get _destination() {
    return this.__destination;
  }
  get scrolling() {
    return this._destination !== null;
  }
  scrollTo(t, e) {
    const s = typeof t == "number" && typeof e == "number" ? { left: t, top: e } : t;
    this._scrollTo(s);
  }
  scrollBy(t, e) {
    const s = typeof t == "number" && typeof e == "number" ? { left: t, top: e } : t;
    s.top !== void 0 && (s.top += this.scrollTop), s.left !== void 0 && (s.left += this.scrollLeft), this._scrollTo(s);
  }
  _nativeScrollTo(t) {
    this._originalScrollTo.bind(this._element || window)(t);
  }
  _scrollTo(t, e = null, s = null) {
    this._end !== null && this._end(), t.behavior === "smooth" ? (this._setDestination(t), this._retarget = e, this._end = s) : this._resetScrollState(), this._nativeScrollTo(t);
  }
  _setDestination(t) {
    let { top: e, left: s } = t;
    return e = e === void 0 ? void 0 : Math.max(0, Math.min(e, this.maxScrollTop)), s = s === void 0 ? void 0 : Math.max(0, Math.min(s, this.maxScrollLeft)), this._destination !== null && s === this._destination.left && e === this._destination.top ? !1 : (this.__destination = { top: e, left: s, behavior: "smooth" }, !0);
  }
  _resetScrollState() {
    this.__destination = null, this._retarget = null, this._end = null;
  }
  _updateManagedScrollTo(t) {
    this._destination && this._setDestination(t) && this._nativeScrollTo(this._destination);
  }
  managedScrollTo(t, e, s) {
    return this._scrollTo(t, e, s), this._updateManagedScrollTo;
  }
  correctScrollError(t) {
    this.correctingScrollError = !0, requestAnimationFrame(() => requestAnimationFrame(() => this.correctingScrollError = !1)), this._nativeScrollTo(t), this._retarget && this._setDestination(this._retarget()), this._destination && this._nativeScrollTo(this._destination);
  }
  _checkForArrival() {
    if (this._destination !== null) {
      const { scrollTop: t, scrollLeft: e } = this;
      let { top: s, left: i } = this._destination;
      s = Math.min(s || 0, this.maxScrollTop), i = Math.min(i || 0, this.maxScrollLeft);
      const r = Math.abs(s - t), l = Math.abs(i - e);
      r < 1 && l < 1 && (this._end && this._end(), this._resetScrollState());
    }
  }
  detach(t) {
    return this._clients.delete(t), this._clients.size === 0 && (this._node.scrollTo = this._originalScrollTo, this._node.scrollBy = this._originalScrollBy, this._node.scroll = this._originalScroll, this._node.removeEventListener("scroll", this._checkForArrival)), null;
  }
  _attach(t) {
    this._clients.add(t), this._clients.size === 1 && (this._node.scrollTo = this.scrollTo, this._node.scrollBy = this.scrollBy, this._node.scroll = this.scrollTo, this._node.addEventListener("scroll", this._checkForArrival));
  }
}
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
let it = typeof window < "u" ? window.ResizeObserver : void 0;
const Q = Symbol("virtualizerRef"), M = "virtualizer-sizer";
let nt;
class Ot {
  constructor(t) {
    if (this._benchmarkStart = null, this._layout = null, this._clippingAncestors = [], this._scrollSize = null, this._scrollError = null, this._childrenPos = null, this._childMeasurements = null, this._toBeMeasured = /* @__PURE__ */ new Map(), this._rangeChanged = !0, this._itemsChanged = !0, this._visibilityChanged = !0, this._scrollerController = null, this._isScroller = !1, this._sizer = null, this._hostElementRO = null, this._childrenRO = null, this._mutationObserver = null, this._scrollEventListeners = [], this._scrollEventListenerOptions = {
      passive: !0
    }, this._loadListener = this._childLoaded.bind(this), this._scrollIntoViewTarget = null, this._updateScrollIntoViewCoordinates = null, this._items = [], this._first = -1, this._last = -1, this._firstVisible = -1, this._lastVisible = -1, this._scheduled = /* @__PURE__ */ new WeakSet(), this._measureCallback = null, this._measureChildOverride = null, this._layoutCompletePromise = null, this._layoutCompleteResolver = null, this._layoutCompleteRejecter = null, this._pendingLayoutComplete = null, this._layoutInitialized = null, this._connected = !1, !t)
      throw new Error("Virtualizer constructor requires a configuration object");
    if (t.hostElement)
      this._init(t);
    else
      throw new Error('Virtualizer configuration requires the "hostElement" property');
  }
  set items(t) {
    Array.isArray(t) && t !== this._items && (this._itemsChanged = !0, this._items = t, this._schedule(this._updateLayout));
  }
  _init(t) {
    this._isScroller = !!t.scroller, this._initHostElement(t);
    const e = t.layout || {};
    this._layoutInitialized = this._initLayout(e);
  }
  _initObservers() {
    this._mutationObserver = new MutationObserver(this._finishDOMUpdate.bind(this)), this._hostElementRO = new it(() => this._hostElementSizeChanged()), this._childrenRO = new it(this._childrenSizeChanged.bind(this));
  }
  _initHostElement(t) {
    const e = this._hostElement = t.hostElement;
    this._applyVirtualizerStyles(), e[Q] = this;
  }
  connected() {
    this._initObservers();
    const t = this._isScroller;
    this._clippingAncestors = Mt(this._hostElement, t), this._scrollerController = new It(this, this._clippingAncestors[0]), this._schedule(this._updateLayout), this._observeAndListen(), this._connected = !0;
  }
  _observeAndListen() {
    this._mutationObserver.observe(this._hostElement, { childList: !0 }), this._hostElementRO.observe(this._hostElement), this._scrollEventListeners.push(window), window.addEventListener("scroll", this, this._scrollEventListenerOptions), this._clippingAncestors.forEach((t) => {
      t.addEventListener("scroll", this, this._scrollEventListenerOptions), this._scrollEventListeners.push(t), this._hostElementRO.observe(t);
    }), this._hostElementRO.observe(this._scrollerController.element), this._children.forEach((t) => this._childrenRO.observe(t)), this._scrollEventListeners.forEach((t) => t.addEventListener("scroll", this, this._scrollEventListenerOptions));
  }
  disconnected() {
    var t, e, s, i;
    this._scrollEventListeners.forEach((r) => r.removeEventListener("scroll", this, this._scrollEventListenerOptions)), this._scrollEventListeners = [], this._clippingAncestors = [], (t = this._scrollerController) == null || t.detach(this), this._scrollerController = null, (e = this._mutationObserver) == null || e.disconnect(), this._mutationObserver = null, (s = this._hostElementRO) == null || s.disconnect(), this._hostElementRO = null, (i = this._childrenRO) == null || i.disconnect(), this._childrenRO = null, this._rejectLayoutCompletePromise("disconnected"), this._connected = !1;
  }
  _applyVirtualizerStyles() {
    const e = this._hostElement.style;
    e.display = e.display || "block", e.position = e.position || "relative", e.contain = e.contain || "size layout", this._isScroller && (e.overflow = e.overflow || "auto", e.minHeight = e.minHeight || "150px");
  }
  _getSizer() {
    const t = this._hostElement;
    if (!this._sizer) {
      let e = t.querySelector(`[${M}]`);
      e || (e = document.createElement("div"), e.setAttribute(M, ""), t.appendChild(e)), Object.assign(e.style, {
        position: "absolute",
        margin: "-2px 0 0 0",
        padding: 0,
        visibility: "hidden",
        fontSize: "2px"
      }), e.textContent = "&nbsp;", e.setAttribute(M, ""), this._sizer = e;
    }
    return this._sizer;
  }
  async updateLayoutConfig(t) {
    await this._layoutInitialized;
    const e = t.type || // The new config is compatible with the current layout,
    // so we update the config and return true to indicate
    // a successful update
    nt;
    if (typeof e == "function" && this._layout instanceof e) {
      const s = { ...t };
      return delete s.type, this._layout.config = s, !0;
    }
    return !1;
  }
  async _initLayout(t) {
    let e, s;
    if (typeof t.type == "function") {
      s = t.type;
      const i = { ...t };
      delete i.type, e = i;
    } else
      e = t;
    s === void 0 && (nt = s = (await import("./flow-D-0MTYCm.js")).FlowLayout), this._layout = new s((i) => this._handleLayoutMessage(i), e), this._layout.measureChildren && typeof this._layout.updateItemSizes == "function" && (typeof this._layout.measureChildren == "function" && (this._measureChildOverride = this._layout.measureChildren), this._measureCallback = this._layout.updateItemSizes.bind(this._layout)), this._layout.listenForChildLoadEvents && this._hostElement.addEventListener("load", this._loadListener, !0), this._schedule(this._updateLayout);
  }
  // TODO (graynorton): Rework benchmarking so that it has no API and
  // instead is always on except in production builds
  startBenchmarking() {
    this._benchmarkStart === null && (this._benchmarkStart = window.performance.now());
  }
  stopBenchmarking() {
    if (this._benchmarkStart !== null) {
      const t = window.performance.now(), e = t - this._benchmarkStart, i = performance.getEntriesByName("uv-virtualizing", "measure").filter((r) => r.startTime >= this._benchmarkStart && r.startTime < t).reduce((r, l) => r + l.duration, 0);
      return this._benchmarkStart = null, { timeElapsed: e, virtualizationTime: i };
    }
    return null;
  }
  _measureChildren() {
    const t = {}, e = this._children, s = this._measureChildOverride || this._measureChild;
    for (let i = 0; i < e.length; i++) {
      const r = e[i], l = this._first + i;
      (this._itemsChanged || this._toBeMeasured.has(r)) && (t[l] = s.call(this, r, this._items[l]));
    }
    this._childMeasurements = t, this._schedule(this._updateLayout), this._toBeMeasured.clear();
  }
  /**
   * Returns the width, height, and margins of the given child.
   */
  _measureChild(t) {
    const { width: e, height: s } = t.getBoundingClientRect();
    return Object.assign({ width: e, height: s }, Bt(t));
  }
  async _schedule(t) {
    this._scheduled.has(t) || (this._scheduled.add(t), await Promise.resolve(), this._scheduled.delete(t), t.call(this));
  }
  async _updateDOM(t) {
    this._scrollSize = t.scrollSize, this._adjustRange(t.range), this._childrenPos = t.childPositions, this._scrollError = t.scrollError || null;
    const { _rangeChanged: e, _itemsChanged: s } = this;
    this._visibilityChanged && (this._notifyVisibility(), this._visibilityChanged = !1), (e || s) && (this._notifyRange(), this._rangeChanged = !1), this._finishDOMUpdate();
  }
  _finishDOMUpdate() {
    this._connected && (this._children.forEach((t) => this._childrenRO.observe(t)), this._checkScrollIntoViewTarget(this._childrenPos), this._positionChildren(this._childrenPos), this._sizeHostElement(this._scrollSize), this._correctScrollError(), this._benchmarkStart && "mark" in window.performance && window.performance.mark("uv-end"));
  }
  _updateLayout() {
    this._layout && this._connected && (this._layout.items = this._items, this._updateView(), this._childMeasurements !== null && (this._measureCallback && this._measureCallback(this._childMeasurements), this._childMeasurements = null), this._layout.reflowIfNeeded(), this._benchmarkStart && "mark" in window.performance && window.performance.mark("uv-end"));
  }
  _handleScrollEvent() {
    var t;
    if (this._benchmarkStart && "mark" in window.performance) {
      try {
        window.performance.measure("uv-virtualizing", "uv-start", "uv-end");
      } catch (e) {
        console.warn("Error measuring performance data: ", e);
      }
      window.performance.mark("uv-start");
    }
    this._scrollerController.correctingScrollError === !1 && ((t = this._layout) == null || t.unpin()), this._schedule(this._updateLayout);
  }
  handleEvent(t) {
    switch (t.type) {
      case "scroll":
        (t.currentTarget === window || this._clippingAncestors.includes(t.currentTarget)) && this._handleScrollEvent();
        break;
      default:
        console.warn("event not handled", t);
    }
  }
  _handleLayoutMessage(t) {
    t.type === "stateChanged" ? this._updateDOM(t) : t.type === "visibilityChanged" ? (this._firstVisible = t.firstVisible, this._lastVisible = t.lastVisible, this._notifyVisibility()) : t.type === "unpinned" && this._hostElement.dispatchEvent(new F());
  }
  get _children() {
    const t = [];
    let e = this._hostElement.firstElementChild;
    for (; e; )
      e.hasAttribute(M) || t.push(e), e = e.nextElementSibling;
    return t;
  }
  _updateView() {
    var i;
    const t = this._hostElement, e = (i = this._scrollerController) == null ? void 0 : i.element, s = this._layout;
    if (t && e && s) {
      let r, l, a, o;
      const u = t.getBoundingClientRect();
      r = 0, l = 0, a = window.innerHeight, o = window.innerWidth;
      const g = this._clippingAncestors.map((E) => E.getBoundingClientRect());
      g.unshift(u);
      for (const E of g)
        r = Math.max(r, E.top), l = Math.max(l, E.left), a = Math.min(a, E.bottom), o = Math.min(o, E.right);
      const _ = e.getBoundingClientRect(), f = {
        left: u.left - _.left,
        top: u.top - _.top
      }, d = {
        width: e.scrollWidth,
        height: e.scrollHeight
      }, p = r - u.top + t.scrollTop, m = l - u.left + t.scrollLeft, A = a - r, V = o - l;
      s.viewportSize = { width: V, height: A }, s.viewportScroll = { top: p, left: m }, s.totalScrollSize = d, s.offsetWithinScroller = f;
    }
  }
  /**
   * Styles the host element so that its size reflects the
   * total size of all items.
   */
  _sizeHostElement(t) {
    const s = t && t.width !== null ? Math.min(82e5, t.width) : 0, i = t && t.height !== null ? Math.min(82e5, t.height) : 0;
    if (this._isScroller)
      this._getSizer().style.transform = `translate(${s}px, ${i}px)`;
    else {
      const r = this._hostElement.style;
      r.minWidth = s ? `${s}px` : "100%", r.minHeight = i ? `${i}px` : "100%";
    }
  }
  /**
   * Sets the top and left transform style of the children from the values in
   * pos.
   */
  _positionChildren(t) {
    t && t.forEach(({ top: e, left: s, width: i, height: r, xOffset: l, yOffset: a }, o) => {
      const u = this._children[o - this._first];
      u && (u.style.position = "absolute", u.style.boxSizing = "border-box", u.style.transform = `translate(${s}px, ${e}px)`, i !== void 0 && (u.style.width = i + "px"), r !== void 0 && (u.style.height = r + "px"), u.style.left = l === void 0 ? null : l + "px", u.style.top = a === void 0 ? null : a + "px");
    });
  }
  async _adjustRange(t) {
    const { _first: e, _last: s, _firstVisible: i, _lastVisible: r } = this;
    this._first = t.first, this._last = t.last, this._firstVisible = t.firstVisible, this._lastVisible = t.lastVisible, this._rangeChanged = this._rangeChanged || this._first !== e || this._last !== s, this._visibilityChanged = this._visibilityChanged || this._firstVisible !== i || this._lastVisible !== r;
  }
  _correctScrollError() {
    if (this._scrollError) {
      const { scrollTop: t, scrollLeft: e } = this._scrollerController, { top: s, left: i } = this._scrollError;
      this._scrollError = null, this._scrollerController.correctScrollError({
        top: t - s,
        left: e - i
      });
    }
  }
  element(t) {
    var e;
    return t === 1 / 0 && (t = this._items.length - 1), ((e = this._items) == null ? void 0 : e[t]) === void 0 ? void 0 : {
      scrollIntoView: (s = {}) => this._scrollElementIntoView({ ...s, index: t })
    };
  }
  _scrollElementIntoView(t) {
    if (t.index >= this._first && t.index <= this._last)
      this._children[t.index - this._first].scrollIntoView(t);
    else if (t.index = Math.min(t.index, this._items.length - 1), t.behavior === "smooth") {
      const e = this._layout.getScrollIntoViewCoordinates(t), { behavior: s } = t;
      this._updateScrollIntoViewCoordinates = this._scrollerController.managedScrollTo(Object.assign(e, { behavior: s }), () => this._layout.getScrollIntoViewCoordinates(t), () => this._scrollIntoViewTarget = null), this._scrollIntoViewTarget = t;
    } else
      this._layout.pin = t;
  }
  /**
   * If we are smoothly scrolling to an element and the target element
   * is in the DOM, we update our target coordinates as needed
   */
  _checkScrollIntoViewTarget(t) {
    const { index: e } = this._scrollIntoViewTarget || {};
    e && (t != null && t.has(e)) && this._updateScrollIntoViewCoordinates(this._layout.getScrollIntoViewCoordinates(this._scrollIntoViewTarget));
  }
  /**
   * Emits a rangechange event with the current first, last, firstVisible, and
   * lastVisible.
   */
  _notifyRange() {
    this._hostElement.dispatchEvent(new H({ first: this._first, last: this._last }));
  }
  _notifyVisibility() {
    this._hostElement.dispatchEvent(new D({
      first: this._firstVisible,
      last: this._lastVisible
    }));
  }
  get layoutComplete() {
    return this._layoutCompletePromise || (this._layoutCompletePromise = new Promise((t, e) => {
      this._layoutCompleteResolver = t, this._layoutCompleteRejecter = e;
    })), this._layoutCompletePromise;
  }
  _rejectLayoutCompletePromise(t) {
    this._layoutCompleteRejecter !== null && this._layoutCompleteRejecter(t), this._resetLayoutCompleteState();
  }
  _scheduleLayoutComplete() {
    this._layoutCompletePromise && this._pendingLayoutComplete === null && (this._pendingLayoutComplete = requestAnimationFrame(() => requestAnimationFrame(() => this._resolveLayoutCompletePromise())));
  }
  _resolveLayoutCompletePromise() {
    this._layoutCompleteResolver !== null && this._layoutCompleteResolver(), this._resetLayoutCompleteState();
  }
  _resetLayoutCompleteState() {
    this._layoutCompletePromise = null, this._layoutCompleteResolver = null, this._layoutCompleteRejecter = null, this._pendingLayoutComplete = null;
  }
  /**
   * Render and update the view at the next opportunity with the given
   * hostElement size.
   */
  _hostElementSizeChanged() {
    this._schedule(this._updateLayout);
  }
  // TODO (graynorton): Rethink how this works. Probably child loading is too specific
  // to have dedicated support for; might want some more generic lifecycle hooks for
  // layouts to use. Possibly handle measurement this way, too, or maybe that remains
  // a first-class feature?
  _childLoaded() {
  }
  // This is the callback for the ResizeObserver that watches the
  // virtualizer's children. We land here at the end of every virtualizer
  // update cycle that results in changes to physical items, and we also
  // end up here if one or more children change size independently of
  // the virtualizer update cycle.
  _childrenSizeChanged(t) {
    var e;
    if ((e = this._layout) != null && e.measureChildren) {
      for (const s of t)
        this._toBeMeasured.set(s.target, s.contentRect);
      this._measureChildren();
    }
    this._scheduleLayoutComplete(), this._itemsChanged = !1, this._rangeChanged = !1;
  }
}
function Bt(n) {
  const t = window.getComputedStyle(n);
  return {
    marginTop: G(t.marginTop),
    marginRight: G(t.marginRight),
    marginBottom: G(t.marginBottom),
    marginLeft: G(t.marginLeft)
  };
}
function G(n) {
  const t = n ? parseFloat(n) : NaN;
  return Number.isNaN(t) ? 0 : t;
}
function rt(n) {
  if (n.assignedSlot !== null)
    return n.assignedSlot;
  if (n.parentElement !== null)
    return n.parentElement;
  const t = n.parentNode;
  return t && t.nodeType === Node.DOCUMENT_FRAGMENT_NODE && t.host || null;
}
function Vt(n, t = !1) {
  const e = [];
  let s = t ? n : rt(n);
  for (; s !== null; )
    e.push(s), s = rt(s);
  return e;
}
function Mt(n, t = !1) {
  let e = !1;
  return Vt(n, t).filter((s) => {
    if (e)
      return !1;
    const i = getComputedStyle(s);
    return e = i.position === "fixed", i.overflow !== "visible";
  });
}
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const pt = (n) => n, _t = (n, t) => y`${t}: ${JSON.stringify(n, null, 2)}`;
class Gt extends Lt {
  constructor(t) {
    if (super(t), this._virtualizer = null, this._first = 0, this._last = -1, this._renderItem = (e, s) => _t(e, s + this._first), this._keyFunction = (e, s) => pt(e, s + this._first), this._items = [], t.type !== N.CHILD)
      throw new Error("The virtualize directive can only be used in child expressions");
  }
  render(t) {
    t && this._setFunctions(t);
    const e = [];
    if (this._first >= 0 && this._last >= this._first)
      for (let s = this._first; s <= this._last; s++)
        e.push(this._items[s]);
    return At(e, this._keyFunction, this._renderItem);
  }
  update(t, [e]) {
    this._setFunctions(e);
    const s = this._items !== e.items;
    return this._items = e.items || [], this._virtualizer ? this._updateVirtualizerConfig(t, e) : this._initialize(t, e), s ? X : this.render();
  }
  async _updateVirtualizerConfig(t, e) {
    if (!await this._virtualizer.updateLayoutConfig(e.layout || {})) {
      const i = t.parentNode;
      this._makeVirtualizer(i, e);
    }
    this._virtualizer.items = this._items;
  }
  _setFunctions(t) {
    const { renderItem: e, keyFunction: s } = t;
    e && (this._renderItem = (i, r) => e(i, r + this._first)), s && (this._keyFunction = (i, r) => s(i, r + this._first));
  }
  _makeVirtualizer(t, e) {
    this._virtualizer && this._virtualizer.disconnected();
    const { layout: s, scroller: i, items: r } = e;
    this._virtualizer = new Ot({ hostElement: t, layout: s, scroller: i }), this._virtualizer.items = r, this._virtualizer.connected();
  }
  _initialize(t, e) {
    const s = t.parentNode;
    s && s.nodeType === 1 && (s.addEventListener("rangeChanged", (i) => {
      this._first = i.first, this._last = i.last, this.setValue(this.render());
    }), this._makeVirtualizer(s, e));
  }
  disconnected() {
    var t;
    (t = this._virtualizer) == null || t.disconnected();
  }
  reconnected() {
    var t;
    (t = this._virtualizer) == null || t.connected();
  }
}
const Tt = J(Gt);
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class L extends Y {
  constructor() {
    super(...arguments), this.items = [], this.renderItem = _t, this.keyFunction = pt, this.layout = {}, this.scroller = !1;
  }
  createRenderRoot() {
    return this;
  }
  render() {
    const { items: t, renderItem: e, keyFunction: s, layout: i, scroller: r } = this;
    return y`${Tt({
      items: t,
      renderItem: e,
      keyFunction: s,
      layout: i,
      scroller: r
    })}`;
  }
  element(t) {
    var e;
    return (e = this[Q]) == null ? void 0 : e.element(t);
  }
  get layoutComplete() {
    var t;
    return (t = this[Q]) == null ? void 0 : t.layoutComplete;
  }
  /**
   * This scrollToIndex() shim is here to provide backwards compatibility with other 0.x versions of
   * lit-virtualizer. It is deprecated and will likely be removed in the 1.0.0 release.
   */
  scrollToIndex(t, e = "start") {
    var s;
    (s = this.element(t)) == null || s.scrollIntoView({ block: e });
  }
}
O([
  v({ attribute: !1 })
], L.prototype, "items", void 0);
O([
  v()
], L.prototype, "renderItem", void 0);
O([
  v()
], L.prototype, "keyFunction", void 0);
O([
  v({ attribute: !1 })
], L.prototype, "layout", void 0);
O([
  v({ reflect: !0, type: Boolean })
], L.prototype, "scroller", void 0);
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
customElements.define("lit-virtualizer", L);
/*
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
class b {
  constructor(t, e = "") {
    h(this, "source");
    h(this, "flags");
    this.source = t.source, this.flags = e;
  }
  /**
   * Extend regular expression.
   *
   * @param groupName Regular expression for search a group name.
   * @param groupRegexp Regular expression of named group.
   */
  setGroup(t, e) {
    let s = typeof e == "string" ? e : e.source;
    return s = s.replace(/(^|[^\[])\^/g, "$1"), this.source = this.source.replace(t, s), this;
  }
  /**
   * Returns a result of extending a regular expression.
   */
  getRegexp() {
    return new RegExp(this.source, this.flags);
  }
}
/**
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
const Nt = /[&<>"']/, qt = /[&<>"']/g, lt = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  // tslint:disable-next-line:quotemark
  "'": "&#39;"
}, Ht = /[<>"']|&(?!#?\w+;)/, Dt = /[<>"']|&(?!#?\w+;)/g;
function Ft(n, t) {
  if (t) {
    if (Nt.test(n))
      return n.replace(qt, (e) => lt[e]);
  } else if (Ht.test(n))
    return n.replace(Dt, (e) => lt[e]);
  return n;
}
function jt(n) {
  return n.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi, function(t, e) {
    return e = e.toLowerCase(), e === "colon" ? ":" : e.charAt(0) === "#" ? e.charAt(1) === "x" ? String.fromCharCode(parseInt(e.substring(2), 16)) : String.fromCharCode(+e.substring(1)) : "";
  });
}
/**
 * @license
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
var c;
(function(n) {
  n[n.space = 1] = "space", n[n.text = 2] = "text", n[n.paragraph = 3] = "paragraph", n[n.heading = 4] = "heading", n[n.listStart = 5] = "listStart", n[n.listEnd = 6] = "listEnd", n[n.looseItemStart = 7] = "looseItemStart", n[n.looseItemEnd = 8] = "looseItemEnd", n[n.listItemStart = 9] = "listItemStart", n[n.listItemEnd = 10] = "listItemEnd", n[n.blockquoteStart = 11] = "blockquoteStart", n[n.blockquoteEnd = 12] = "blockquoteEnd", n[n.code = 13] = "code", n[n.table = 14] = "table", n[n.html = 15] = "html", n[n.hr = 16] = "hr";
})(c || (c = {}));
class Pt {
  constructor() {
    h(this, "gfm", !0);
    h(this, "tables", !0);
    h(this, "breaks", !1);
    h(this, "pedantic", !1);
    h(this, "sanitize", !1);
    h(this, "sanitizer");
    h(this, "mangle", !0);
    h(this, "smartLists", !1);
    h(this, "silent", !1);
    /**
     * @param code The section of code to pass to the highlighter.
     * @param lang The programming language specified in the code block.
     */
    h(this, "highlight");
    h(this, "langPrefix", "lang-");
    h(this, "smartypants", !1);
    h(this, "headerPrefix", "");
    /**
     * An object containing functions to render tokens to HTML. Default: `new Renderer()`
     */
    h(this, "renderer");
    /**
     * Self-close the tags for void elements (&lt;br/&gt;, &lt;img/&gt;, etc.)
     * with a "/" as required by XHTML.
     */
    h(this, "xhtml", !1);
    /**
     * The function that will be using to escape HTML entities.
     * By default using inner helper.
     */
    h(this, "escape", Ft);
    /**
     * The function that will be using to unescape HTML entities.
     * By default using inner helper.
     */
    h(this, "unescape", jt);
    /**
     * If set to `true`, an inline text will not be taken in paragraph.
     *
     * ```ts
     * // isNoP == false
     * Marked.parse('some text'); // returns '<p>some text</p>'
     *
     * Marked.setOptions({isNoP: true});
     *
     * Marked.parse('some text'); // returns 'some text'
     * ```
     */
    h(this, "isNoP");
  }
}
/**
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
class ft {
  constructor(t) {
    h(this, "options");
    this.options = t || C.options;
  }
  code(t, e, s, i) {
    if (this.options.highlight) {
      const a = this.options.highlight(t, e);
      a != null && a !== t && (s = !0, t = a);
    }
    const r = s ? t : this.options.escape(t, !0);
    return e ? `
<pre><code class="${this.options.langPrefix + this.options.escape(e, !0)}">${r}
</code></pre>
` : `
<pre><code>${r}
</code></pre>
`;
  }
  blockquote(t) {
    return `<blockquote>
${t}</blockquote>
`;
  }
  html(t) {
    return t;
  }
  heading(t, e, s) {
    const i = this.options.headerPrefix + s.toLowerCase().replace(/[^\w]+/g, "-");
    return `<h${e} id="${i}">${t}</h${e}>
`;
  }
  hr() {
    return this.options.xhtml ? `<hr/>
` : `<hr>
`;
  }
  list(t, e) {
    const s = e ? "ol" : "ul";
    return `
<${s}>
${t}</${s}>
`;
  }
  listitem(t) {
    return "<li>" + t + `</li>
`;
  }
  paragraph(t) {
    return "<p>" + t + `</p>
`;
  }
  table(t, e) {
    return `
<table>
<thead>
${t}</thead>
<tbody>
${e}</tbody>
</table>
`;
  }
  tablerow(t) {
    return `<tr>
` + t + `</tr>
`;
  }
  tablecell(t, e) {
    const s = e.header ? "th" : "td";
    return (e.align ? "<" + s + ' style="text-align:' + e.align + '">' : "<" + s + ">") + t + "</" + s + `>
`;
  }
  // *** Inline level renderer methods. ***
  strong(t) {
    return "<strong>" + t + "</strong>";
  }
  em(t) {
    return "<em>" + t + "</em>";
  }
  codespan(t) {
    return "<code>" + t + "</code>";
  }
  br() {
    return this.options.xhtml ? "<br/>" : "<br>";
  }
  del(t) {
    return "<del>" + t + "</del>";
  }
  link(t, e, s) {
    if (this.options.sanitize) {
      let r;
      try {
        r = decodeURIComponent(this.options.unescape(t)).replace(/[^\w:]/g, "").toLowerCase();
      } catch {
        return s;
      }
      if (r.indexOf("javascript:") === 0 || r.indexOf("vbscript:") === 0 || r.indexOf("data:") === 0)
        return s;
    }
    let i = '<a href="' + t + '"';
    return e && (i += ' title="' + e + '"'), i += ">" + s + "</a>", i;
  }
  image(t, e, s) {
    let i = '<img src="' + t + '" alt="' + s + '"';
    return e && (i += ' title="' + e + '"'), i += this.options.xhtml ? "/>" : ">", i;
  }
  text(t) {
    return t;
  }
}
/**
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
class x {
  constructor(t, e, s = C.options, i) {
    h(this, "staticThis");
    h(this, "links");
    h(this, "options");
    h(this, "rules");
    h(this, "renderer");
    h(this, "inLink");
    h(this, "hasRulesGfm");
    h(this, "ruleCallbacks");
    if (this.staticThis = t, this.links = e, this.options = s, this.renderer = i || this.options.renderer || new ft(this.options), !this.links)
      throw new Error("InlineLexer requires 'links' parameter.");
    this.setRules();
  }
  /**
   * Static Lexing/Compiling Method.
   */
  static output(t, e, s) {
    return new this(this, e, s).output(t);
  }
  static getRulesBase() {
    if (this.rulesBase)
      return this.rulesBase;
    const t = {
      escape: /^\\([\\`*{}\[\]()#+\-.!_>])/,
      autolink: /^<([^ <>]+(@|:\/)[^ <>]+)>/,
      tag: /^<!--[\s\S]*?-->|^<\/?\w+(?:"[^"]*"|'[^']*'|[^<'">])*?>/,
      link: /^!?\[(inside)\]\(href\)/,
      reflink: /^!?\[(inside)\]\s*\[([^\]]*)\]/,
      nolink: /^!?\[((?:\[[^\]]*\]|[^\[\]])*)\]/,
      strong: /^__([\s\S]+?)__(?!_)|^\*\*([\s\S]+?)\*\*(?!\*)/,
      em: /^\b_((?:[^_]|__)+?)_\b|^\*((?:\*\*|[\s\S])+?)\*(?!\*)/,
      code: /^(`+)([\s\S]*?[^`])\1(?!`)/,
      br: /^ {2,}\n(?!\s*$)/,
      text: /^[\s\S]+?(?=[\\<!\[_*`]| {2,}\n|$)/,
      _inside: /(?:\[[^\]]*\]|[^\[\]]|\](?=[^\[]*\]))*/,
      _href: /\s*<?([\s\S]*?)>?(?:\s+['"]([\s\S]*?)['"])?\s*/
    };
    return t.link = new b(t.link).setGroup("inside", t._inside).setGroup("href", t._href).getRegexp(), t.reflink = new b(t.reflink).setGroup("inside", t._inside).getRegexp(), this.rulesBase = t;
  }
  static getRulesPedantic() {
    return this.rulesPedantic ? this.rulesPedantic : this.rulesPedantic = {
      ...this.getRulesBase(),
      strong: /^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,
      em: /^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/
    };
  }
  static getRulesGfm() {
    if (this.rulesGfm)
      return this.rulesGfm;
    const t = this.getRulesBase(), e = new b(t.escape).setGroup("])", "~|])").getRegexp(), s = new b(t.text).setGroup("]|", "~]|").setGroup("|", "|https?://|").getRegexp();
    return this.rulesGfm = {
      ...t,
      escape: e,
      url: /^(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/,
      del: /^~~(?=\S)([\s\S]*?\S)~~/,
      text: s
    };
  }
  static getRulesBreaks() {
    if (this.rulesBreaks)
      return this.rulesBreaks;
    const t = this.getRulesGfm(), e = this.getRulesGfm();
    return this.rulesBreaks = {
      ...e,
      br: new b(t.br).setGroup("{2,}", "*").getRegexp(),
      text: new b(e.text).setGroup("{2,}", "*").getRegexp()
    };
  }
  setRules() {
    this.options.gfm ? this.options.breaks ? this.rules = this.staticThis.getRulesBreaks() : this.rules = this.staticThis.getRulesGfm() : this.options.pedantic ? this.rules = this.staticThis.getRulesPedantic() : this.rules = this.staticThis.getRulesBase(), this.hasRulesGfm = this.rules.url !== void 0;
  }
  /**
   * Lexing/Compiling.
   */
  output(t) {
    let e, s = "";
    for (; t; ) {
      if (e = this.rules.escape.exec(t)) {
        t = t.substring(e[0].length), s += e[1];
        continue;
      }
      if (e = this.rules.autolink.exec(t)) {
        let i, r;
        t = t.substring(e[0].length), e[2] === "@" ? (i = this.options.escape(e[1].charAt(6) === ":" ? this.mangle(e[1].substring(7)) : this.mangle(e[1])), r = this.mangle("mailto:") + i) : (i = this.options.escape(e[1]), r = i), s += this.renderer.link(r, null, i);
        continue;
      }
      if (!this.inLink && this.hasRulesGfm && (e = this.rules.url.exec(t))) {
        t = t.substring(e[0].length);
        const i = this.options.escape(e[1]), r = i;
        s += this.renderer.link(r, null, i);
        continue;
      }
      if (e = this.rules.tag.exec(t)) {
        !this.inLink && /^<a /i.test(e[0]) ? this.inLink = !0 : this.inLink && /^<\/a>/i.test(e[0]) && (this.inLink = !1), t = t.substring(e[0].length), s += this.options.sanitize ? this.options.sanitizer ? this.options.sanitizer(e[0]) : this.options.escape(e[0]) : e[0];
        continue;
      }
      if (e = this.rules.link.exec(t)) {
        t = t.substring(e[0].length), this.inLink = !0, s += this.outputLink(e, {
          href: e[2],
          title: e[3]
        }), this.inLink = !1;
        continue;
      }
      if ((e = this.rules.reflink.exec(t)) || (e = this.rules.nolink.exec(t))) {
        t = t.substring(e[0].length);
        const i = (e[2] || e[1]).replace(/\s+/g, " "), r = this.links[i.toLowerCase()];
        if (!r || !r.href) {
          s += e[0].charAt(0), t = e[0].substring(1) + t;
          continue;
        }
        this.inLink = !0, s += this.outputLink(e, r), this.inLink = !1;
        continue;
      }
      if (e = this.rules.strong.exec(t)) {
        t = t.substring(e[0].length), s += this.renderer.strong(this.output(e[2] || e[1]));
        continue;
      }
      if (e = this.rules.em.exec(t)) {
        t = t.substring(e[0].length), s += this.renderer.em(this.output(e[2] || e[1]));
        continue;
      }
      if (e = this.rules.code.exec(t)) {
        t = t.substring(e[0].length), s += this.renderer.codespan(this.options.escape(e[2].trim(), !0));
        continue;
      }
      if (e = this.rules.br.exec(t)) {
        t = t.substring(e[0].length), s += this.renderer.br();
        continue;
      }
      if (this.hasRulesGfm && (e = this.rules.del.exec(t))) {
        t = t.substring(e[0].length), s += this.renderer.del(this.output(e[1]));
        continue;
      }
      if (e = this.rules.text.exec(t)) {
        t = t.substring(e[0].length), s += this.renderer.text(this.options.escape(this.smartypants(e[0])));
        continue;
      }
      if (t)
        throw new Error("Infinite loop on byte: " + t.charCodeAt(0));
    }
    return s;
  }
  /**
   * Compile Link.
   */
  outputLink(t, e) {
    const s = this.options.escape(e.href), i = e.title ? this.options.escape(e.title) : null;
    return t[0].charAt(0) !== "!" ? this.renderer.link(s, i, this.output(t[1])) : this.renderer.image(s, i, this.options.escape(t[1]));
  }
  /**
   * Smartypants Transformations.
   */
  smartypants(t) {
    return this.options.smartypants ? t.replace(/---/g, "—").replace(/--/g, "–").replace(/(^|[-\u2014/([{"\s])'/g, "$1‘").replace(/'/g, "’").replace(/(^|[-\u2014/([{\u2018\s])"/g, "$1“").replace(/"/g, "”").replace(/\.{3}/g, "…") : t;
  }
  /**
   * Mangle Links.
   */
  mangle(t) {
    if (!this.options.mangle)
      return t;
    let e = "";
    const s = t.length;
    for (let i = 0; i < s; i++) {
      let r;
      Math.random() > 0.5 && (r = "x" + t.charCodeAt(i).toString(16)), e += "&#" + r + ";";
    }
    return e;
  }
}
h(x, "rulesBase", null), /**
 * Pedantic Inline Grammar.
 */
h(x, "rulesPedantic", null), /**
 * GFM Inline Grammar
 */
h(x, "rulesGfm", null), /**
 * GFM + Line Breaks Inline Grammar.
 */
h(x, "rulesBreaks", null);
/**
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
class P {
  constructor(t) {
    h(this, "simpleRenderers", []);
    h(this, "tokens");
    h(this, "token");
    h(this, "inlineLexer");
    h(this, "options");
    h(this, "renderer");
    h(this, "line", 0);
    this.tokens = [], this.token = null, this.options = t || C.options, this.renderer = this.options.renderer || new ft(this.options);
  }
  static parse(t, e, s) {
    return new this(s).parse(e, t);
  }
  parse(t, e) {
    this.inlineLexer = new x(x, t, this.options, this.renderer), this.tokens = e.reverse();
    let s = "";
    for (; this.next(); )
      s += this.tok();
    return s;
  }
  debug(t, e) {
    this.inlineLexer = new x(x, t, this.options, this.renderer), this.tokens = e.reverse();
    let s = "";
    for (; this.next(); ) {
      const i = this.tok();
      this.token.line = this.line += i.split(`
`).length - 1, s += i;
    }
    return s;
  }
  next() {
    return this.token = this.tokens.pop();
  }
  getNextElement() {
    return this.tokens[this.tokens.length - 1];
  }
  parseText() {
    let t = this.token.text, e;
    for (; (e = this.getNextElement()) && e.type == c.text; )
      t += `
` + this.next().text;
    return this.inlineLexer.output(t);
  }
  tok() {
    switch (this.token.type) {
      case c.space:
        return "";
      case c.paragraph:
        return this.renderer.paragraph(this.inlineLexer.output(this.token.text));
      case c.text:
        return this.options.isNoP ? this.parseText() : this.renderer.paragraph(this.parseText());
      case c.heading:
        return this.renderer.heading(this.inlineLexer.output(this.token.text), this.token.depth, this.token.text);
      case c.listStart: {
        let t = "";
        const e = this.token.ordered;
        for (; this.next().type != c.listEnd; )
          t += this.tok();
        return this.renderer.list(t, e);
      }
      case c.listItemStart: {
        let t = "";
        for (; this.next().type != c.listItemEnd; )
          t += this.token.type == c.text ? this.parseText() : this.tok();
        return this.renderer.listitem(t);
      }
      case c.looseItemStart: {
        let t = "";
        for (; this.next().type != c.listItemEnd; )
          t += this.tok();
        return this.renderer.listitem(t);
      }
      case c.code:
        return this.renderer.code(this.token.text, this.token.lang, this.token.escaped, this.token.meta);
      case c.table: {
        let t = "", e = "", s;
        s = "";
        for (let i = 0; i < this.token.header.length; i++) {
          const r = { header: !0, align: this.token.align[i] }, l = this.inlineLexer.output(this.token.header[i]);
          s += this.renderer.tablecell(l, r);
        }
        t += this.renderer.tablerow(s);
        for (const i of this.token.cells) {
          s = "";
          for (let r = 0; r < i.length; r++)
            s += this.renderer.tablecell(this.inlineLexer.output(i[r]), {
              header: !1,
              align: this.token.align[r]
            });
          e += this.renderer.tablerow(s);
        }
        return this.renderer.table(t, e);
      }
      case c.blockquoteStart: {
        let t = "";
        for (; this.next().type != c.blockquoteEnd; )
          t += this.tok();
        return this.renderer.blockquote(t);
      }
      case c.hr:
        return this.renderer.hr();
      case c.html: {
        const t = !this.token.pre && !this.options.pedantic ? this.inlineLexer.output(this.token.text) : this.token.text;
        return this.renderer.html(t);
      }
      default: {
        if (this.simpleRenderers.length) {
          for (let e = 0; e < this.simpleRenderers.length; e++)
            if (this.token.type == "simpleRule" + (e + 1))
              return this.simpleRenderers[e].call(this.renderer, this.token.execArr);
        }
        const t = `Token with "${this.token.type}" type was not found.`;
        if (this.options.silent)
          console.log(t);
        else
          throw new Error(t);
      }
    }
  }
}
/**
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
class C {
  /**
   * Merges the default options with options that will be set.
   *
   * @param options Hash of options.
   */
  static setOptions(t) {
    return Object.assign(this.options, t), this;
  }
  /**
   * Setting simple block rule.
   */
  static setBlockRule(t, e = () => "") {
    return R.simpleRules.push(t), this.simpleRenderers.push(e), this;
  }
  /**
   * Accepts Markdown text and returns text in HTML format.
   *
   * @param src String of markdown source to be compiled.
   * @param options Hash of options. They replace, but do not merge with the default options.
   * If you want the merging, you can to do this via `Marked.setOptions()`.
   */
  static parse(t, e) {
    try {
      e = { ...this.options, ...e };
      const { tokens: s, links: i } = this.callBlockLexer(t, e);
      return this.callParser(s, i, e);
    } catch (s) {
      return this.callMe(s);
    }
  }
  /**
   * Accepts Markdown text and returns object with text in HTML format,
   * tokens and links from `BlockLexer.parser()`.
   *
   * @param src String of markdown source to be compiled.
   * @param options Hash of options. They replace, but do not merge with the default options.
   * If you want the merging, you can to do this via `Marked.setOptions()`.
   */
  static debug(t, e = this.options) {
    const { tokens: s, links: i } = this.callBlockLexer(t, e);
    let r = s.slice();
    const l = new P(e);
    l.simpleRenderers = this.simpleRenderers;
    const a = l.debug(i, s);
    return r = r.map((o) => {
      o.type = c[o.type] || o.type;
      const u = o.line;
      return delete o.line, u ? { line: u, ...o } : o;
    }), { tokens: r, links: i, result: a };
  }
  static callBlockLexer(t = "", e) {
    if (typeof t != "string")
      throw new Error(`Expected that the 'src' parameter would have a 'string' type, got '${typeof t}'`);
    return t = t.replace(/\r\n|\r/g, `
`).replace(/\t/g, "    ").replace(/\u00a0/g, " ").replace(/\u2424/g, `
`).replace(/^ +$/gm, ""), R.lex(t, e, !0);
  }
  static callParser(t, e, s) {
    if (this.simpleRenderers.length) {
      const i = new P(s);
      return i.simpleRenderers = this.simpleRenderers, i.parse(e, t);
    } else
      return P.parse(t, e, s);
  }
  static callMe(t) {
    if (t.message += `
Please report this to https://github.com/ts-stack/markdown`, this.options.silent)
      return "<p>An error occured:</p><pre>" + this.options.escape(t.message + "", !0) + "</pre>";
    throw t;
  }
}
h(C, "options", new Pt()), h(C, "simpleRenderers", []);
/**
 * @license
 *
 * Copyright (c) 2011-2014, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/chjj/marked
 *
 * Copyright (c) 2018-2021, Костя Третяк. (MIT Licensed)
 * https://github.com/ts-stack/markdown
 */
class R {
  constructor(t, e) {
    h(this, "staticThis");
    h(this, "rules");
    h(this, "options");
    h(this, "links", {});
    h(this, "tokens", []);
    h(this, "hasRulesGfm");
    h(this, "hasRulesTables");
    this.staticThis = t, this.options = e || C.options, this.setRules();
  }
  /**
   * Accepts Markdown text and returns object with tokens and links.
   *
   * @param src String of markdown source to be compiled.
   * @param options Hash of options.
   */
  static lex(t, e, s, i) {
    return new this(this, e).getTokens(t, s, i);
  }
  static getRulesBase() {
    if (this.rulesBase)
      return this.rulesBase;
    const t = {
      newline: /^\n+/,
      code: /^( {4}[^\n]+\n*)+/,
      hr: /^( *[-*_]){3,} *(?:\n+|$)/,
      heading: /^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)/,
      lheading: /^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,
      blockquote: /^( *>[^\n]+(\n[^\n]+)*\n*)+/,
      list: /^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,
      html: /^ *(?:comment *(?:\n|\s*$)|closed *(?:\n{2,}|\s*$)|closing *(?:\n{2,}|\s*$))/,
      def: /^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +["(]([^\n]+)[")])? *(?:\n+|$)/,
      paragraph: /^((?:[^\n]+\n?(?!hr|heading|lheading|blockquote|tag|def))+)\n*/,
      text: /^[^\n]+/,
      bullet: /(?:[*+-]|\d+\.)/,
      item: /^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/
    };
    t.item = new b(t.item, "gm").setGroup(/bull/g, t.bullet).getRegexp(), t.list = new b(t.list).setGroup(/bull/g, t.bullet).setGroup("hr", "\\n+(?=\\1?(?:[-*_] *){3,}(?:\\n+|$))").setGroup("def", "\\n+(?=" + t.def.source + ")").getRegexp();
    const e = "(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:/|[^\\w\\s@]*@)\\b";
    return t.html = new b(t.html).setGroup("comment", /<!--[\s\S]*?-->/).setGroup("closed", /<(tag)[\s\S]+?<\/\1>/).setGroup("closing", /<tag(?:"[^"]*"|'[^']*'|[^'">])*?>/).setGroup(/tag/g, e).getRegexp(), t.paragraph = new b(t.paragraph).setGroup("hr", t.hr).setGroup("heading", t.heading).setGroup("lheading", t.lheading).setGroup("blockquote", t.blockquote).setGroup("tag", "<" + e).setGroup("def", t.def).getRegexp(), this.rulesBase = t;
  }
  static getRulesGfm() {
    if (this.rulesGfm)
      return this.rulesGfm;
    const t = this.getRulesBase(), e = {
      ...t,
      fences: /^ *(`{3,}|~{3,})[ \.]*((\S+)? *[^\n]*)\n([\s\S]*?)\s*\1 *(?:\n+|$)/,
      paragraph: /^/,
      heading: /^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/
    }, s = e.fences.source.replace("\\1", "\\2"), i = t.list.source.replace("\\1", "\\3");
    return e.paragraph = new b(t.paragraph).setGroup("(?!", `(?!${s}|${i}|`).getRegexp(), this.rulesGfm = e;
  }
  static getRulesTable() {
    return this.rulesTables ? this.rulesTables : this.rulesTables = {
      ...this.getRulesGfm(),
      nptable: /^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*/,
      table: /^ *\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*/
    };
  }
  setRules() {
    this.options.gfm ? this.options.tables ? this.rules = this.staticThis.getRulesTable() : this.rules = this.staticThis.getRulesGfm() : this.rules = this.staticThis.getRulesBase(), this.hasRulesGfm = this.rules.fences !== void 0, this.hasRulesTables = this.rules.table !== void 0;
  }
  /**
   * Lexing.
   */
  getTokens(t, e, s) {
    let i = t, r;
    t: for (; i; ) {
      if ((r = this.rules.newline.exec(i)) && (i = i.substring(r[0].length), r[0].length > 1 && this.tokens.push({ type: c.space })), r = this.rules.code.exec(i)) {
        i = i.substring(r[0].length);
        const l = r[0].replace(/^ {4}/gm, "");
        this.tokens.push({
          type: c.code,
          text: this.options.pedantic ? l : l.replace(/\n+$/, "")
        });
        continue;
      }
      if (this.hasRulesGfm && (r = this.rules.fences.exec(i))) {
        i = i.substring(r[0].length), this.tokens.push({
          type: c.code,
          meta: r[2],
          lang: r[3],
          text: r[4] || ""
        });
        continue;
      }
      if (r = this.rules.heading.exec(i)) {
        i = i.substring(r[0].length), this.tokens.push({
          type: c.heading,
          depth: r[1].length,
          text: r[2]
        });
        continue;
      }
      if (e && this.hasRulesTables && (r = this.rules.nptable.exec(i))) {
        i = i.substring(r[0].length);
        const l = {
          type: c.table,
          header: r[1].replace(/^ *| *\| *$/g, "").split(/ *\| */),
          align: r[2].replace(/^ *|\| *$/g, "").split(/ *\| */),
          cells: []
        };
        for (let o = 0; o < l.align.length; o++)
          /^ *-+: *$/.test(l.align[o]) ? l.align[o] = "right" : /^ *:-+: *$/.test(l.align[o]) ? l.align[o] = "center" : /^ *:-+ *$/.test(l.align[o]) ? l.align[o] = "left" : l.align[o] = null;
        const a = r[3].replace(/\n$/, "").split(`
`);
        for (let o = 0; o < a.length; o++)
          l.cells[o] = a[o].split(/ *\| */);
        this.tokens.push(l);
        continue;
      }
      if (r = this.rules.lheading.exec(i)) {
        i = i.substring(r[0].length), this.tokens.push({
          type: c.heading,
          depth: r[2] === "=" ? 1 : 2,
          text: r[1]
        });
        continue;
      }
      if (r = this.rules.hr.exec(i)) {
        i = i.substring(r[0].length), this.tokens.push({ type: c.hr });
        continue;
      }
      if (r = this.rules.blockquote.exec(i)) {
        i = i.substring(r[0].length), this.tokens.push({ type: c.blockquoteStart });
        const l = r[0].replace(/^ *> ?/gm, "");
        this.getTokens(l), this.tokens.push({ type: c.blockquoteEnd });
        continue;
      }
      if (r = this.rules.list.exec(i)) {
        i = i.substring(r[0].length);
        const l = r[2];
        this.tokens.push({ type: c.listStart, ordered: l.length > 1 });
        const a = r[0].match(this.rules.item), o = a.length;
        let u = !1, g, _, f;
        for (let d = 0; d < o; d++) {
          let p = a[d];
          g = p.length, p = p.replace(/^ *([*+-]|\d+\.) +/, ""), p.indexOf(`
 `) !== -1 && (g -= p.length, p = this.options.pedantic ? p.replace(/^ {1,4}/gm, "") : p.replace(new RegExp("^ {1," + g + "}", "gm"), "")), this.options.smartLists && d !== o - 1 && (_ = this.staticThis.getRulesBase().bullet.exec(a[d + 1])[0], l !== _ && !(l.length > 1 && _.length > 1) && (i = a.slice(d + 1).join(`
`) + i, d = o - 1)), f = u || /\n\n(?!\s*$)/.test(p), d !== o - 1 && (u = p.charAt(p.length - 1) === `
`, f || (f = u)), this.tokens.push({ type: f ? c.looseItemStart : c.listItemStart }), this.getTokens(p, !1, s), this.tokens.push({ type: c.listItemEnd });
        }
        this.tokens.push({ type: c.listEnd });
        continue;
      }
      if (r = this.rules.html.exec(i)) {
        i = i.substring(r[0].length);
        const l = r[1], a = l === "pre" || l === "script" || l === "style";
        this.tokens.push({
          type: this.options.sanitize ? c.paragraph : c.html,
          pre: !this.options.sanitizer && a,
          text: r[0]
        });
        continue;
      }
      if (e && (r = this.rules.def.exec(i))) {
        i = i.substring(r[0].length), this.links[r[1].toLowerCase()] = {
          href: r[2],
          title: r[3]
        };
        continue;
      }
      if (e && this.hasRulesTables && (r = this.rules.table.exec(i))) {
        i = i.substring(r[0].length);
        const l = {
          type: c.table,
          header: r[1].replace(/^ *| *\| *$/g, "").split(/ *\| */),
          align: r[2].replace(/^ *|\| *$/g, "").split(/ *\| */),
          cells: []
        };
        for (let o = 0; o < l.align.length; o++)
          /^ *-+: *$/.test(l.align[o]) ? l.align[o] = "right" : /^ *:-+: *$/.test(l.align[o]) ? l.align[o] = "center" : /^ *:-+ *$/.test(l.align[o]) ? l.align[o] = "left" : l.align[o] = null;
        const a = r[3].replace(/(?: *\| *)?\n$/, "").split(`
`);
        for (let o = 0; o < a.length; o++)
          l.cells[o] = a[o].replace(/^ *\| *| *\| *$/g, "").split(/ *\| */);
        this.tokens.push(l);
        continue;
      }
      if (this.staticThis.simpleRules.length) {
        const l = this.staticThis.simpleRules;
        for (let a = 0; a < l.length; a++)
          if (r = l[a].exec(i)) {
            i = i.substring(r[0].length);
            const o = "simpleRule" + (a + 1);
            this.tokens.push({ type: o, execArr: r });
            continue t;
          }
      }
      if (e && (r = this.rules.paragraph.exec(i))) {
        i = i.substring(r[0].length), r[1].slice(-1) === `
` ? this.tokens.push({
          type: c.paragraph,
          text: r[1].slice(0, -1)
        }) : this.tokens.push({
          type: this.tokens.length > 0 ? c.paragraph : c.text,
          text: r[1]
        });
        continue;
      }
      if (r = this.rules.text.exec(i)) {
        i = i.substring(r[0].length), this.tokens.push({ type: c.text, text: r[0] });
        continue;
      }
      if (i)
        throw new Error("Infinite loop on byte: " + i.charCodeAt(0) + `, near text '${i.slice(0, 30)}...'`);
    }
    return { tokens: this.tokens, links: this.links };
  }
}
h(R, "simpleRules", []), h(R, "rulesBase", null), /**
 * GFM Block Grammar.
 */
h(R, "rulesGfm", null), /**
 * GFM + Tables Block Grammar.
 */
h(R, "rulesTables", null);
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class K extends Z {
  constructor(t) {
    if (super(t), this.it = tt, t.type !== N.CHILD) throw Error(this.constructor.directiveName + "() can only be used in child bindings");
  }
  render(t) {
    if (t === tt || t == null) return this._t = void 0, this.it = t;
    if (t === X) return t;
    if (typeof t != "string") throw Error(this.constructor.directiveName + "() called with a non-string value");
    if (t === this.it) return this._t;
    this.it = t;
    const e = [t];
    return e.raw = e, this._t = { _$litType$: this.constructor.resultType, strings: e, values: [] };
  }
}
K.directiveName = "unsafeHTML", K.resultType = 1;
const Wt = J(K);
var Ut = Object.defineProperty, Qt = Object.getOwnPropertyDescriptor, B = (n, t, e, s) => {
  for (var i = s > 1 ? void 0 : s ? Qt(t, e) : t, r = n.length - 1, l; r >= 0; r--)
    (l = n[r]) && (i = (s ? l(t, e, i) : l(i)) || i);
  return s && i && Ut(t, e, i), i;
};
let $ = class extends Y {
  constructor() {
    super(...arguments), this.answer = "", this.expanded = !1, this._fetchData = new at(
      this,
      async () => {
        this.entryId && (this.dataStream = W.getDataStream(
          this,
          this.entryId,
          this._updateAnswer
        ), await W.postRequest(`/plugins/${this.entryId}`, {
          action: "ask_question",
          user_input: {
            question: this.question
          }
        }));
      },
      () => []
    ), this._updateAnswer = async (n) => {
      var t;
      n === "finished" ? (t = this.dataStream) == null || t.close() : this.answer += n, U(this, "data-updated");
    };
  }
  disconnectedCallback() {
    var n;
    super.disconnectedCallback(), (n = this.dataStream) == null || n.close();
  }
  render() {
    return y`
      <pc-expansion-panel .expanded=${this.expanded}>
        <div slot="header" class="header">
          <div class="layout horizontal center">
            <strong class="question">${this.question}</strong>
            <pc-icon-button
              .path=${yt}
              label="edit"
              @click=${this._handleClick}
            ></pc-icon-button>
          </div>
        </div>
        <div class="answer">
          ${this._fetchData.render({
      complete: () => y`${this.answer.length > 0 ? Wt(C.parse(this.answer)) : y`<pc-circular-progress
                    size="small"
                    indeterminate
                  ></pc-circular-progress>`}`
    })}
        </div>
      </pc-expansion-panel>
    `;
  }
  _handleClick(n) {
    n.stopPropagation(), U(this, "value-changed", { value: this.question });
  }
};
$.styles = [
  ot,
  ht`
      :host {
        width: 100%;
      }
      pc-expansion-panel div.answer {
        background-color: rgb(243, 243, 243);
      }
      pc-icon-button {
        --md-icon-button-icon-size: 20px;
        display: none;
        margin-left: 8px;
      }
      .header:hover pc-icon-button {
        display: inline-block;
      }
      .answer {
        min-height: 60px;
      }
      pc-circular-progress {
        --md-circular-progress-active-indicator-width: 20;
      }
    `
];
B([
  v({ attribute: !1 })
], $.prototype, "entryId", 2);
B([
  v({ attribute: !1 })
], $.prototype, "question", 2);
B([
  v({ attribute: !1 })
], $.prototype, "answer", 2);
B([
  v({ attribute: !1 })
], $.prototype, "expanded", 2);
$ = B([
  ct("conversation-card")
], $);
var Kt = Object.defineProperty, Zt = Object.getOwnPropertyDescriptor, S = (n, t, e, s) => {
  for (var i = s > 1 ? void 0 : s ? Zt(t, e) : t, r = n.length - 1, l; r >= 0; r--)
    (l = n[r]) && (i = (s ? l(t, e, i) : l(i)) || i);
  return s && i && Kt(t, e, i), i;
};
let w = class extends Y {
  constructor() {
    super(...arguments), this.chatHistory = [], this._loading = !1, this.prompt = "", this._numOfRows = 1, this._fetchData = new at(
      this,
      async () => {
        await W.postRequest(`/plugins/${this.entry.entry_id}`, {
          action: "get_chat_history"
        }).then((n) => {
          this.chatHistory = n.data.result;
        }).catch((n) => {
          var t;
          if (((t = n.response) == null ? void 0 : t.status) === 400)
            throw new Error(n.response.data.detail);
        });
      },
      () => []
    ), this._checkOverflow = () => {
      var t;
      const n = (t = this._textField.shadowRoot) == null ? void 0 : t.querySelector(
        ".input"
      );
      n && (n.style.height = "auto", n.style.height = `${Math.min(n.scrollHeight, 96)}px`);
    }, this._renderConversation = (n) => y`<conversation-card
      .entryId=${n.entryId}
      .question=${n.question}
      .answer=${n.answer ?? ""}
      .expanded=${n.expanded ?? !1}
    ></conversation-card>`;
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this.removeEventListener(
      "value-changed",
      this._updatePrompt
    ), this.removeEventListener(
      "data-updated",
      this._scrollToView
    ), this._resizeObserver && this._resizeObserver.disconnect();
  }
  firstUpdated(n) {
    this.addEventListener("value-changed", (t) => {
      this._updatePrompt(t);
    }), this.addEventListener("data-updated", () => {
      this._scrollToView(), this.prompt = "";
    });
  }
  _handleKeyDown(n) {
    n.key === "Enter" && (n.shiftKey || (n.preventDefault(), this.prompt && this.prompt.replace(/\n/g, "").length > 0 && this._submitQuestion()));
  }
  async _scrollToView() {
    if (this._scroller) {
      await this._scroller.updateComplete;
      const n = this._scroller.element(this._scroller.items.length - 1);
      n && n.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }
  }
  render() {
    return y`<pc-card raised .header=${this.entry.title}
      ><div class="card-content">
        <div class="flex">
          ${this._fetchData.render({
      complete: () => y` ${this.chatHistory.length === 0 ? "" : y` <lit-virtualizer
                    id="scroller"
                    scroller
                    .items=${this.chatHistory}
                    .renderItem=${this._renderConversation}
                  ></lit-virtualizer>`}`
    })}
        </div>
        <md-outlined-text-field
          id="prompt"
          type="textarea"
          placeholder="Ask AI"
          rows=${this._numOfRows}
          .value=${this.prompt}
          @input=${this._valueChanged}
          @keydown=${this._handleKeyDown}
          >${!this.prompt || this.prompt.replace(/\n/g, "").length === 0 ? "" : y`<pc-icon-button
                label="Submit"
                slot="trailing-icon"
                @click=${this._submitQuestion}
                .path=${wt}
              ></pc-icon-button>`}</md-outlined-text-field
        >
      </div>
    </pc-card>`;
  }
  _valueChanged(n) {
    this.prompt = n.target.value, this._checkOverflow();
  }
  _updatePrompt(n) {
    this.prompt = n.detail.value;
  }
  async _submitQuestion() {
    this.chatHistory = [
      ...this.chatHistory,
      { entryId: this.entry.entry_id, question: this.prompt, expanded: !0 }
    ], await this.updateComplete, this._scroller && await this._scroller.updateComplete, U(this, "data-updated");
  }
};
w.styles = [
  ot,
  ht`
      pc-card {
        height: 100%;
      }
      conversation-card {
        display: block;
      }
      lit-virtualizer {
        height: 100%;
        margin-bottom: 8px;
      }
      md-outlined-text-field {
        resize: none;
        --md-outlined-text-field-container-shape: 24px;
        margin: 0px 16px;
        height: auto; /* Initial height: auto */
        max-height: 96px; /* Set a maximum height */
        overflow-y: hidden; /* Hide vertical scrollbar initially */
        transition: height 0.2s; /* Add a transition for smooth resizing */
        box-sizing: border-box;
      }
    `
];
S([
  v({ attribute: !1 })
], w.prototype, "entry", 2);
S([
  q()
], w.prototype, "chatHistory", 2);
S([
  q()
], w.prototype, "_loading", 2);
S([
  q()
], w.prototype, "prompt", 2);
S([
  q()
], w.prototype, "_numOfRows", 2);
S([
  ut("#scroller")
], w.prototype, "_scroller", 2);
S([
  ut("#prompt")
], w.prototype, "_textField", 2);
w = S([
  ct("pc-plugin-gallagher_ai_analyzer")
], w);
export {
  w as PcPluginGallagherAiAnalyzer
};
