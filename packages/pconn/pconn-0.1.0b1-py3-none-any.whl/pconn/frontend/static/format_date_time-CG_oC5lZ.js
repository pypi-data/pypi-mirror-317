import { m as e } from "./memoize-one.esm-DezIwejE.js";
var m, o, n;
const t = ((n = (m = Intl.DateTimeFormat) == null ? void 0 : (o = m.call(Intl)).resolvedOptions) == null ? void 0 : n.call(o).timeZone) ?? "UTC", c = (i) => r().format(i), r = e(
  () => new Intl.DateTimeFormat("en-GB", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
    timeZone: t
  })
);
e(
  () => new Intl.DateTimeFormat("en-GB", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
    timeZone: t
  })
);
e(
  () => new Intl.DateTimeFormat("en-GB", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
    timeZone: t
  })
);
const u = (i) => a().format(i), a = e(
  () => new Intl.DateTimeFormat("en-GB", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
    timeZone: t
  })
);
export {
  t as L,
  u as a,
  c as f
};
