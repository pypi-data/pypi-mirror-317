import { g as $, w as v, d as ee, a as b } from "./Index-PjARxpAb.js";
const _ = window.ms_globals.React, G = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tag;
var K = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = _, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: le.current
  };
}
C.Fragment = re;
C.jsx = V;
C.jsxs = V;
K.exports = C;
var w = K.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: j,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: de,
  component_subscribe: A,
  compute_slots: ue,
  create_slot: fe,
  detach: h,
  element: J,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: x,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: we,
  transition_in: S,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: Ie,
  setContext: ve
} = window.__gradio__svelte__internal;
function F(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = fe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = q(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && be(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (S(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = J("react-portal-target"), o = we(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(h), o = de(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, t, c), n[8](t), x(l, o, c), e && e.m(l, c), x(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && S(e, 1)) : (e = F(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      r || (S(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Se(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const g = v(M(t)), u = v();
  A(n, u, (a) => o(0, s = a));
  const m = v();
  A(n, m, (a) => o(1, r = a));
  const d = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: g,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y,
    onDestroy(a) {
      d.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", E), ye(() => {
    g.set(M(t));
  }), Ie(() => {
    d.forEach((a) => a());
  });
  function I(a) {
    j[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  function Q(a) {
    j[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = L(L({}, t), D(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, t = D(t), [s, r, u, m, c, i, l, e, I, Q];
}
class Ce extends ce {
  constructor(t) {
    super(), he(this, t, Se, xe, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const s = v(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, l], W({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), W({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Oe(n) {
  const [t, o] = U(() => b(n));
  return H(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = G(() => ee(n, (o) => o), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !ke.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function T(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((r) => {
        if (_.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = T(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: l,
            children: [..._.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = T(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const z = X(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = Z(), [l, c] = U([]);
  return H(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Le(r, d), o && d.classList.add(...o.split(" ")), s) {
        const f = Te(s);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var y, E, I;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = T(n);
        return i = R, c(p), i.style.display = "contents", g(), (I = e.current) == null || I.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, s, r]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n, t) {
  const o = G(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const c = b(e.props.node.slotIndex) || 0, i = b(l.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(l.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(o);
}
const Ne = Re(({
  slots: n,
  value: t,
  children: o,
  ...s
}) => {
  const r = je(o);
  return /* @__PURE__ */ w.jsx(te, {
    ...s,
    icon: n.icon ? /* @__PURE__ */ w.jsx(z, {
      slot: n.icon
    }) : s.icon,
    closeIcon: n.closeIcon ? /* @__PURE__ */ w.jsx(z, {
      slot: n.closeIcon
    }) : s.closeIcon,
    children: r.length > 0 ? o : /* @__PURE__ */ w.jsxs(w.Fragment, {
      children: [o, t]
    })
  });
});
export {
  Ne as Tag,
  Ne as default
};
