import { g as Y, w as p, d as H, a as _ } from "./Index-DvEmeGlF.js";
const C = window.ms_globals.React, j = window.ms_globals.React.useMemo, G = window.ms_globals.React.useState, J = window.ms_globals.React.useEffect, h = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Tag;
var A = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var X = C, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(o, t, n) {
  var r, l = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) ee.call(t, r) && !se.hasOwnProperty(r) && (l[r] = t[r]);
  if (o && o.defaultProps) for (r in t = o.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: Z,
    type: o,
    key: e,
    ref: s,
    props: l,
    _owner: te.current
  };
}
b.Fragment = $;
b.jsx = D;
b.jsxs = D;
A.exports = b;
var oe = A.exports;
const {
  SvelteComponent: ne,
  assign: S,
  binding_callbacks: x,
  check_outros: re,
  children: L,
  claim_element: N,
  claim_space: le,
  component_subscribe: k,
  compute_slots: ae,
  create_slot: ce,
  detach: i,
  element: q,
  empty: R,
  exclude_internal_props: E,
  get_all_dirty_from_scope: ue,
  get_slot_changes: ie,
  group_outros: _e,
  init: fe,
  insert_hydration: m,
  safe_not_equal: de,
  set_custom_element_data: K,
  space: pe,
  transition_in: g,
  transition_out: I,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: we,
  setContext: Ie
} = window.__gradio__svelte__internal;
function T(o) {
  let t, n;
  const r = (
    /*#slots*/
    o[7].default
  ), l = ce(
    r,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = N(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = L(t);
      l && l.l(s), s.forEach(i), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      m(e, t, s), l && l.m(t, null), o[9](t), n = !0;
    },
    p(e, s) {
      l && l.p && (!n || s & /*$$scope*/
      64) && me(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        n ? ie(
          r,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (g(l, e), n = !0);
    },
    o(e) {
      I(l, e), n = !1;
    },
    d(e) {
      e && i(t), l && l.d(e), o[9](null);
    }
  };
}
function ve(o) {
  let t, n, r, l, e = (
    /*$$slots*/
    o[4].default && T(o)
  );
  return {
    c() {
      t = q("react-portal-target"), n = pe(), e && e.c(), r = R(), this.h();
    },
    l(s) {
      t = N(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), L(t).forEach(i), n = le(s), e && e.l(s), r = R(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      m(s, t, c), o[8](t), m(s, n, c), e && e.m(s, c), m(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && g(e, 1)) : (e = T(s), e.c(), g(e, 1), e.m(r.parentNode, r)) : e && (_e(), I(e, 1, 1, () => {
        e = null;
      }), re());
    },
    i(s) {
      l || (g(e), l = !0);
    },
    o(s) {
      I(e), l = !1;
    },
    d(s) {
      s && (i(t), i(n), i(r)), o[8](null), e && e.d(s);
    }
  };
}
function O(o) {
  const {
    svelteInit: t,
    ...n
  } = o;
  return n;
}
function ye(o, t, n) {
  let r, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ae(e);
  let {
    svelteInit: u
  } = t;
  const v = p(O(t)), f = p();
  k(o, f, (a) => n(0, r = a));
  const d = p();
  k(o, d, (a) => n(1, l = a));
  const y = [], M = be("$$ms-gr-react-wrapper"), {
    slotKey: U,
    slotIndex: B,
    subSlotIndex: F
  } = Y() || {}, V = u({
    parent: M,
    props: v,
    target: f,
    slot: d,
    slotKey: U,
    slotIndex: B,
    subSlotIndex: F,
    onDestroy(a) {
      y.push(a);
    }
  });
  Ie("$$ms-gr-react-wrapper", V), ge(() => {
    v.set(O(t));
  }), we(() => {
    y.forEach((a) => a());
  });
  function W(a) {
    x[a ? "unshift" : "push"](() => {
      r = a, f.set(r);
    });
  }
  function z(a) {
    x[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  return o.$$set = (a) => {
    n(17, t = S(S({}, t), E(a))), "svelteInit" in a && n(5, u = a.svelteInit), "$$scope" in a && n(6, s = a.$$scope);
  }, t = E(t), [r, l, f, d, c, u, s, e, W, z];
}
class he extends ne {
  constructor(t) {
    super(), fe(this, t, ye, ve, de, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function Se(o) {
  function t(n) {
    const r = p(), l = new he({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? w;
          return c.nodes = [...c.nodes, s], P({
            createPortal: h,
            node: w
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== r), P({
              createPortal: h,
              node: w
            });
          }), s;
        },
        ...n.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
function xe(o) {
  const [t, n] = G(() => _(o));
  return J(() => {
    let r = !0;
    return o.subscribe((e) => {
      r && (r = !1, e === t) || n(e);
    });
  }, [o]), t;
}
function ke(o) {
  const t = j(() => H(o, (n) => n), [o]);
  return xe(t);
}
function Re(o, t) {
  const n = j(() => C.Children.toArray(o).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = _(e.props.node.slotIndex) || 0, u = _(s.props.node.slotIndex) || 0;
      return c - u === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (_(e.props.node.subSlotIndex) || 0) - (_(s.props.node.subSlotIndex) || 0) : c - u;
    }
    return 0;
  }).map((e) => e.props.node.target), [o, t]);
  return ke(n);
}
const Te = Se(({
  onChange: o,
  onValueChange: t,
  children: n,
  label: r,
  ...l
}) => {
  const e = Re(n);
  return /* @__PURE__ */ oe.jsx(Q.CheckableTag, {
    ...l,
    onChange: (s) => {
      o == null || o(s), t(s);
    },
    children: e.length > 0 ? n : r
  });
});
export {
  Te as CheckableTag,
  Te as default
};
