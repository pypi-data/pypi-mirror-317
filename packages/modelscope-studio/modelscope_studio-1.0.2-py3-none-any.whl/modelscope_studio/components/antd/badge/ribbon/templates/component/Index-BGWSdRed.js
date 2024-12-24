var vt = typeof global == "object" && global && global.Object === Object && global, nn = typeof self == "object" && self && self.Object === Object && self, S = vt || nn || Function("return this")(), w = S.Symbol, Tt = Object.prototype, rn = Tt.hasOwnProperty, on = Tt.toString, q = w ? w.toStringTag : void 0;
function an(e) {
  var t = rn.call(e, q), n = e[q];
  try {
    e[q] = void 0;
    var r = !0;
  } catch {
  }
  var o = on.call(e);
  return r && (t ? e[q] = n : delete e[q]), o;
}
var sn = Object.prototype, un = sn.toString;
function ln(e) {
  return un.call(e);
}
var fn = "[object Null]", cn = "[object Undefined]", Ge = w ? w.toStringTag : void 0;
function D(e) {
  return e == null ? e === void 0 ? cn : fn : Ge && Ge in Object(e) ? an(e) : ln(e);
}
function j(e) {
  return e != null && typeof e == "object";
}
var pn = "[object Symbol]";
function Ae(e) {
  return typeof e == "symbol" || j(e) && D(e) == pn;
}
function Ot(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, o = Array(r); ++n < r; )
    o[n] = t(e[n], n, e);
  return o;
}
var $ = Array.isArray, gn = 1 / 0, Be = w ? w.prototype : void 0, ze = Be ? Be.toString : void 0;
function wt(e) {
  if (typeof e == "string")
    return e;
  if ($(e))
    return Ot(e, wt) + "";
  if (Ae(e))
    return ze ? ze.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -gn ? "-0" : t;
}
function H(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function At(e) {
  return e;
}
var dn = "[object AsyncFunction]", _n = "[object Function]", bn = "[object GeneratorFunction]", hn = "[object Proxy]";
function $t(e) {
  if (!H(e))
    return !1;
  var t = D(e);
  return t == _n || t == bn || t == dn || t == hn;
}
var pe = S["__core-js_shared__"], He = function() {
  var e = /[^.]+$/.exec(pe && pe.keys && pe.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function yn(e) {
  return !!He && He in e;
}
var mn = Function.prototype, vn = mn.toString;
function K(e) {
  if (e != null) {
    try {
      return vn.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var Tn = /[\\^$.*+?()[\]{}|]/g, On = /^\[object .+?Constructor\]$/, wn = Function.prototype, An = Object.prototype, $n = wn.toString, Pn = An.hasOwnProperty, Sn = RegExp("^" + $n.call(Pn).replace(Tn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function xn(e) {
  if (!H(e) || yn(e))
    return !1;
  var t = $t(e) ? Sn : On;
  return t.test(K(e));
}
function Cn(e, t) {
  return e == null ? void 0 : e[t];
}
function U(e, t) {
  var n = Cn(e, t);
  return xn(n) ? n : void 0;
}
var ye = U(S, "WeakMap"), qe = Object.create, jn = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!H(t))
      return {};
    if (qe)
      return qe(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function En(e, t, n) {
  switch (n.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, n[0]);
    case 2:
      return e.call(t, n[0], n[1]);
    case 3:
      return e.call(t, n[0], n[1], n[2]);
  }
  return e.apply(t, n);
}
function In(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Mn = 800, Ln = 16, Rn = Date.now;
function Fn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Rn(), o = Ln - (r - n);
    if (n = r, o > 0) {
      if (++t >= Mn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Nn(e) {
  return function() {
    return e;
  };
}
var ne = function() {
  try {
    var e = U(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Dn = ne ? function(e, t) {
  return ne(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Nn(t),
    writable: !0
  });
} : At, Kn = Fn(Dn);
function Un(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var Gn = 9007199254740991, Bn = /^(?:0|[1-9]\d*)$/;
function Pt(e, t) {
  var n = typeof e;
  return t = t ?? Gn, !!t && (n == "number" || n != "symbol" && Bn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function $e(e, t, n) {
  t == "__proto__" && ne ? ne(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function Pe(e, t) {
  return e === t || e !== e && t !== t;
}
var zn = Object.prototype, Hn = zn.hasOwnProperty;
function St(e, t, n) {
  var r = e[t];
  (!(Hn.call(e, t) && Pe(r, n)) || n === void 0 && !(t in e)) && $e(e, t, n);
}
function W(e, t, n, r) {
  var o = !n;
  n || (n = {});
  for (var i = -1, a = t.length; ++i < a; ) {
    var s = t[i], f = void 0;
    f === void 0 && (f = e[s]), o ? $e(n, s, f) : St(n, s, f);
  }
  return n;
}
var Ye = Math.max;
function qn(e, t, n) {
  return t = Ye(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, o = -1, i = Ye(r.length - t, 0), a = Array(i); ++o < i; )
      a[o] = r[t + o];
    o = -1;
    for (var s = Array(t + 1); ++o < t; )
      s[o] = r[o];
    return s[t] = n(a), En(e, this, s);
  };
}
var Yn = 9007199254740991;
function Se(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Yn;
}
function xt(e) {
  return e != null && Se(e.length) && !$t(e);
}
var Xn = Object.prototype;
function xe(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || Xn;
  return e === n;
}
function Jn(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var Zn = "[object Arguments]";
function Xe(e) {
  return j(e) && D(e) == Zn;
}
var Ct = Object.prototype, Wn = Ct.hasOwnProperty, Qn = Ct.propertyIsEnumerable, Ce = Xe(/* @__PURE__ */ function() {
  return arguments;
}()) ? Xe : function(e) {
  return j(e) && Wn.call(e, "callee") && !Qn.call(e, "callee");
};
function Vn() {
  return !1;
}
var jt = typeof exports == "object" && exports && !exports.nodeType && exports, Je = jt && typeof module == "object" && module && !module.nodeType && module, kn = Je && Je.exports === jt, Ze = kn ? S.Buffer : void 0, er = Ze ? Ze.isBuffer : void 0, re = er || Vn, tr = "[object Arguments]", nr = "[object Array]", rr = "[object Boolean]", ir = "[object Date]", or = "[object Error]", ar = "[object Function]", sr = "[object Map]", ur = "[object Number]", lr = "[object Object]", fr = "[object RegExp]", cr = "[object Set]", pr = "[object String]", gr = "[object WeakMap]", dr = "[object ArrayBuffer]", _r = "[object DataView]", br = "[object Float32Array]", hr = "[object Float64Array]", yr = "[object Int8Array]", mr = "[object Int16Array]", vr = "[object Int32Array]", Tr = "[object Uint8Array]", Or = "[object Uint8ClampedArray]", wr = "[object Uint16Array]", Ar = "[object Uint32Array]", v = {};
v[br] = v[hr] = v[yr] = v[mr] = v[vr] = v[Tr] = v[Or] = v[wr] = v[Ar] = !0;
v[tr] = v[nr] = v[dr] = v[rr] = v[_r] = v[ir] = v[or] = v[ar] = v[sr] = v[ur] = v[lr] = v[fr] = v[cr] = v[pr] = v[gr] = !1;
function $r(e) {
  return j(e) && Se(e.length) && !!v[D(e)];
}
function je(e) {
  return function(t) {
    return e(t);
  };
}
var Et = typeof exports == "object" && exports && !exports.nodeType && exports, Y = Et && typeof module == "object" && module && !module.nodeType && module, Pr = Y && Y.exports === Et, ge = Pr && vt.process, z = function() {
  try {
    var e = Y && Y.require && Y.require("util").types;
    return e || ge && ge.binding && ge.binding("util");
  } catch {
  }
}(), We = z && z.isTypedArray, It = We ? je(We) : $r, Sr = Object.prototype, xr = Sr.hasOwnProperty;
function Mt(e, t) {
  var n = $(e), r = !n && Ce(e), o = !n && !r && re(e), i = !n && !r && !o && It(e), a = n || r || o || i, s = a ? Jn(e.length, String) : [], f = s.length;
  for (var c in e)
    (t || xr.call(e, c)) && !(a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (c == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    o && (c == "offset" || c == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    i && (c == "buffer" || c == "byteLength" || c == "byteOffset") || // Skip index properties.
    Pt(c, f))) && s.push(c);
  return s;
}
function Lt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var Cr = Lt(Object.keys, Object), jr = Object.prototype, Er = jr.hasOwnProperty;
function Ir(e) {
  if (!xe(e))
    return Cr(e);
  var t = [];
  for (var n in Object(e))
    Er.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function Q(e) {
  return xt(e) ? Mt(e) : Ir(e);
}
function Mr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Lr = Object.prototype, Rr = Lr.hasOwnProperty;
function Fr(e) {
  if (!H(e))
    return Mr(e);
  var t = xe(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Rr.call(e, r)) || n.push(r);
  return n;
}
function Ee(e) {
  return xt(e) ? Mt(e, !0) : Fr(e);
}
var Nr = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Dr = /^\w*$/;
function Ie(e, t) {
  if ($(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Ae(e) ? !0 : Dr.test(e) || !Nr.test(e) || t != null && e in Object(t);
}
var X = U(Object, "create");
function Kr() {
  this.__data__ = X ? X(null) : {}, this.size = 0;
}
function Ur(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Gr = "__lodash_hash_undefined__", Br = Object.prototype, zr = Br.hasOwnProperty;
function Hr(e) {
  var t = this.__data__;
  if (X) {
    var n = t[e];
    return n === Gr ? void 0 : n;
  }
  return zr.call(t, e) ? t[e] : void 0;
}
var qr = Object.prototype, Yr = qr.hasOwnProperty;
function Xr(e) {
  var t = this.__data__;
  return X ? t[e] !== void 0 : Yr.call(t, e);
}
var Jr = "__lodash_hash_undefined__";
function Zr(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = X && t === void 0 ? Jr : t, this;
}
function N(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
N.prototype.clear = Kr;
N.prototype.delete = Ur;
N.prototype.get = Hr;
N.prototype.has = Xr;
N.prototype.set = Zr;
function Wr() {
  this.__data__ = [], this.size = 0;
}
function se(e, t) {
  for (var n = e.length; n--; )
    if (Pe(e[n][0], t))
      return n;
  return -1;
}
var Qr = Array.prototype, Vr = Qr.splice;
function kr(e) {
  var t = this.__data__, n = se(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : Vr.call(t, n, 1), --this.size, !0;
}
function ei(e) {
  var t = this.__data__, n = se(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function ti(e) {
  return se(this.__data__, e) > -1;
}
function ni(e, t) {
  var n = this.__data__, r = se(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function E(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
E.prototype.clear = Wr;
E.prototype.delete = kr;
E.prototype.get = ei;
E.prototype.has = ti;
E.prototype.set = ni;
var J = U(S, "Map");
function ri() {
  this.size = 0, this.__data__ = {
    hash: new N(),
    map: new (J || E)(),
    string: new N()
  };
}
function ii(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function ue(e, t) {
  var n = e.__data__;
  return ii(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function oi(e) {
  var t = ue(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function ai(e) {
  return ue(this, e).get(e);
}
function si(e) {
  return ue(this, e).has(e);
}
function ui(e, t) {
  var n = ue(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function I(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
I.prototype.clear = ri;
I.prototype.delete = oi;
I.prototype.get = ai;
I.prototype.has = si;
I.prototype.set = ui;
var li = "Expected a function";
function Me(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(li);
  var n = function() {
    var r = arguments, o = t ? t.apply(this, r) : r[0], i = n.cache;
    if (i.has(o))
      return i.get(o);
    var a = e.apply(this, r);
    return n.cache = i.set(o, a) || i, a;
  };
  return n.cache = new (Me.Cache || I)(), n;
}
Me.Cache = I;
var fi = 500;
function ci(e) {
  var t = Me(e, function(r) {
    return n.size === fi && n.clear(), r;
  }), n = t.cache;
  return t;
}
var pi = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, gi = /\\(\\)?/g, di = ci(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(pi, function(n, r, o, i) {
    t.push(o ? i.replace(gi, "$1") : r || n);
  }), t;
});
function _i(e) {
  return e == null ? "" : wt(e);
}
function le(e, t) {
  return $(e) ? e : Ie(e, t) ? [e] : di(_i(e));
}
var bi = 1 / 0;
function V(e) {
  if (typeof e == "string" || Ae(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -bi ? "-0" : t;
}
function Le(e, t) {
  t = le(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[V(t[n++])];
  return n && n == r ? e : void 0;
}
function hi(e, t, n) {
  var r = e == null ? void 0 : Le(e, t);
  return r === void 0 ? n : r;
}
function Re(e, t) {
  for (var n = -1, r = t.length, o = e.length; ++n < r; )
    e[o + n] = t[n];
  return e;
}
var Qe = w ? w.isConcatSpreadable : void 0;
function yi(e) {
  return $(e) || Ce(e) || !!(Qe && e && e[Qe]);
}
function mi(e, t, n, r, o) {
  var i = -1, a = e.length;
  for (n || (n = yi), o || (o = []); ++i < a; ) {
    var s = e[i];
    n(s) ? Re(o, s) : o[o.length] = s;
  }
  return o;
}
function vi(e) {
  var t = e == null ? 0 : e.length;
  return t ? mi(e) : [];
}
function Ti(e) {
  return Kn(qn(e, void 0, vi), e + "");
}
var Fe = Lt(Object.getPrototypeOf, Object), Oi = "[object Object]", wi = Function.prototype, Ai = Object.prototype, Rt = wi.toString, $i = Ai.hasOwnProperty, Pi = Rt.call(Object);
function Si(e) {
  if (!j(e) || D(e) != Oi)
    return !1;
  var t = Fe(e);
  if (t === null)
    return !0;
  var n = $i.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Rt.call(n) == Pi;
}
function xi(e, t, n) {
  var r = -1, o = e.length;
  t < 0 && (t = -t > o ? 0 : o + t), n = n > o ? o : n, n < 0 && (n += o), o = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var i = Array(o); ++r < o; )
    i[r] = e[r + t];
  return i;
}
function Ci() {
  this.__data__ = new E(), this.size = 0;
}
function ji(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Ei(e) {
  return this.__data__.get(e);
}
function Ii(e) {
  return this.__data__.has(e);
}
var Mi = 200;
function Li(e, t) {
  var n = this.__data__;
  if (n instanceof E) {
    var r = n.__data__;
    if (!J || r.length < Mi - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new I(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function P(e) {
  var t = this.__data__ = new E(e);
  this.size = t.size;
}
P.prototype.clear = Ci;
P.prototype.delete = ji;
P.prototype.get = Ei;
P.prototype.has = Ii;
P.prototype.set = Li;
function Ri(e, t) {
  return e && W(t, Q(t), e);
}
function Fi(e, t) {
  return e && W(t, Ee(t), e);
}
var Ft = typeof exports == "object" && exports && !exports.nodeType && exports, Ve = Ft && typeof module == "object" && module && !module.nodeType && module, Ni = Ve && Ve.exports === Ft, ke = Ni ? S.Buffer : void 0, et = ke ? ke.allocUnsafe : void 0;
function Di(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = et ? et(n) : new e.constructor(n);
  return e.copy(r), r;
}
function Ki(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, o = 0, i = []; ++n < r; ) {
    var a = e[n];
    t(a, n, e) && (i[o++] = a);
  }
  return i;
}
function Nt() {
  return [];
}
var Ui = Object.prototype, Gi = Ui.propertyIsEnumerable, tt = Object.getOwnPropertySymbols, Ne = tt ? function(e) {
  return e == null ? [] : (e = Object(e), Ki(tt(e), function(t) {
    return Gi.call(e, t);
  }));
} : Nt;
function Bi(e, t) {
  return W(e, Ne(e), t);
}
var zi = Object.getOwnPropertySymbols, Dt = zi ? function(e) {
  for (var t = []; e; )
    Re(t, Ne(e)), e = Fe(e);
  return t;
} : Nt;
function Hi(e, t) {
  return W(e, Dt(e), t);
}
function Kt(e, t, n) {
  var r = t(e);
  return $(e) ? r : Re(r, n(e));
}
function me(e) {
  return Kt(e, Q, Ne);
}
function Ut(e) {
  return Kt(e, Ee, Dt);
}
var ve = U(S, "DataView"), Te = U(S, "Promise"), Oe = U(S, "Set"), nt = "[object Map]", qi = "[object Object]", rt = "[object Promise]", it = "[object Set]", ot = "[object WeakMap]", at = "[object DataView]", Yi = K(ve), Xi = K(J), Ji = K(Te), Zi = K(Oe), Wi = K(ye), A = D;
(ve && A(new ve(new ArrayBuffer(1))) != at || J && A(new J()) != nt || Te && A(Te.resolve()) != rt || Oe && A(new Oe()) != it || ye && A(new ye()) != ot) && (A = function(e) {
  var t = D(e), n = t == qi ? e.constructor : void 0, r = n ? K(n) : "";
  if (r)
    switch (r) {
      case Yi:
        return at;
      case Xi:
        return nt;
      case Ji:
        return rt;
      case Zi:
        return it;
      case Wi:
        return ot;
    }
  return t;
});
var Qi = Object.prototype, Vi = Qi.hasOwnProperty;
function ki(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && Vi.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var ie = S.Uint8Array;
function De(e) {
  var t = new e.constructor(e.byteLength);
  return new ie(t).set(new ie(e)), t;
}
function eo(e, t) {
  var n = t ? De(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var to = /\w*$/;
function no(e) {
  var t = new e.constructor(e.source, to.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var st = w ? w.prototype : void 0, ut = st ? st.valueOf : void 0;
function ro(e) {
  return ut ? Object(ut.call(e)) : {};
}
function io(e, t) {
  var n = t ? De(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var oo = "[object Boolean]", ao = "[object Date]", so = "[object Map]", uo = "[object Number]", lo = "[object RegExp]", fo = "[object Set]", co = "[object String]", po = "[object Symbol]", go = "[object ArrayBuffer]", _o = "[object DataView]", bo = "[object Float32Array]", ho = "[object Float64Array]", yo = "[object Int8Array]", mo = "[object Int16Array]", vo = "[object Int32Array]", To = "[object Uint8Array]", Oo = "[object Uint8ClampedArray]", wo = "[object Uint16Array]", Ao = "[object Uint32Array]";
function $o(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case go:
      return De(e);
    case oo:
    case ao:
      return new r(+e);
    case _o:
      return eo(e, n);
    case bo:
    case ho:
    case yo:
    case mo:
    case vo:
    case To:
    case Oo:
    case wo:
    case Ao:
      return io(e, n);
    case so:
      return new r();
    case uo:
    case co:
      return new r(e);
    case lo:
      return no(e);
    case fo:
      return new r();
    case po:
      return ro(e);
  }
}
function Po(e) {
  return typeof e.constructor == "function" && !xe(e) ? jn(Fe(e)) : {};
}
var So = "[object Map]";
function xo(e) {
  return j(e) && A(e) == So;
}
var lt = z && z.isMap, Co = lt ? je(lt) : xo, jo = "[object Set]";
function Eo(e) {
  return j(e) && A(e) == jo;
}
var ft = z && z.isSet, Io = ft ? je(ft) : Eo, Mo = 1, Lo = 2, Ro = 4, Gt = "[object Arguments]", Fo = "[object Array]", No = "[object Boolean]", Do = "[object Date]", Ko = "[object Error]", Bt = "[object Function]", Uo = "[object GeneratorFunction]", Go = "[object Map]", Bo = "[object Number]", zt = "[object Object]", zo = "[object RegExp]", Ho = "[object Set]", qo = "[object String]", Yo = "[object Symbol]", Xo = "[object WeakMap]", Jo = "[object ArrayBuffer]", Zo = "[object DataView]", Wo = "[object Float32Array]", Qo = "[object Float64Array]", Vo = "[object Int8Array]", ko = "[object Int16Array]", ea = "[object Int32Array]", ta = "[object Uint8Array]", na = "[object Uint8ClampedArray]", ra = "[object Uint16Array]", ia = "[object Uint32Array]", y = {};
y[Gt] = y[Fo] = y[Jo] = y[Zo] = y[No] = y[Do] = y[Wo] = y[Qo] = y[Vo] = y[ko] = y[ea] = y[Go] = y[Bo] = y[zt] = y[zo] = y[Ho] = y[qo] = y[Yo] = y[ta] = y[na] = y[ra] = y[ia] = !0;
y[Ko] = y[Bt] = y[Xo] = !1;
function ee(e, t, n, r, o, i) {
  var a, s = t & Mo, f = t & Lo, c = t & Ro;
  if (n && (a = o ? n(e, r, o, i) : n(e)), a !== void 0)
    return a;
  if (!H(e))
    return e;
  var d = $(e);
  if (d) {
    if (a = ki(e), !s)
      return In(e, a);
  } else {
    var g = A(e), _ = g == Bt || g == Uo;
    if (re(e))
      return Di(e, s);
    if (g == zt || g == Gt || _ && !o) {
      if (a = f || _ ? {} : Po(e), !s)
        return f ? Hi(e, Fi(a, e)) : Bi(e, Ri(a, e));
    } else {
      if (!y[g])
        return o ? e : {};
      a = $o(e, g, s);
    }
  }
  i || (i = new P());
  var h = i.get(e);
  if (h)
    return h;
  i.set(e, a), Io(e) ? e.forEach(function(l) {
    a.add(ee(l, t, n, l, e, i));
  }) : Co(e) && e.forEach(function(l, m) {
    a.set(m, ee(l, t, n, m, e, i));
  });
  var u = c ? f ? Ut : me : f ? Ee : Q, p = d ? void 0 : u(e);
  return Un(p || e, function(l, m) {
    p && (m = l, l = e[m]), St(a, m, ee(l, t, n, m, e, i));
  }), a;
}
var oa = "__lodash_hash_undefined__";
function aa(e) {
  return this.__data__.set(e, oa), this;
}
function sa(e) {
  return this.__data__.has(e);
}
function oe(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new I(); ++t < n; )
    this.add(e[t]);
}
oe.prototype.add = oe.prototype.push = aa;
oe.prototype.has = sa;
function ua(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function la(e, t) {
  return e.has(t);
}
var fa = 1, ca = 2;
function Ht(e, t, n, r, o, i) {
  var a = n & fa, s = e.length, f = t.length;
  if (s != f && !(a && f > s))
    return !1;
  var c = i.get(e), d = i.get(t);
  if (c && d)
    return c == t && d == e;
  var g = -1, _ = !0, h = n & ca ? new oe() : void 0;
  for (i.set(e, t), i.set(t, e); ++g < s; ) {
    var u = e[g], p = t[g];
    if (r)
      var l = a ? r(p, u, g, t, e, i) : r(u, p, g, e, t, i);
    if (l !== void 0) {
      if (l)
        continue;
      _ = !1;
      break;
    }
    if (h) {
      if (!ua(t, function(m, O) {
        if (!la(h, O) && (u === m || o(u, m, n, r, i)))
          return h.push(O);
      })) {
        _ = !1;
        break;
      }
    } else if (!(u === p || o(u, p, n, r, i))) {
      _ = !1;
      break;
    }
  }
  return i.delete(e), i.delete(t), _;
}
function pa(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, o) {
    n[++t] = [o, r];
  }), n;
}
function ga(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var da = 1, _a = 2, ba = "[object Boolean]", ha = "[object Date]", ya = "[object Error]", ma = "[object Map]", va = "[object Number]", Ta = "[object RegExp]", Oa = "[object Set]", wa = "[object String]", Aa = "[object Symbol]", $a = "[object ArrayBuffer]", Pa = "[object DataView]", ct = w ? w.prototype : void 0, de = ct ? ct.valueOf : void 0;
function Sa(e, t, n, r, o, i, a) {
  switch (n) {
    case Pa:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case $a:
      return !(e.byteLength != t.byteLength || !i(new ie(e), new ie(t)));
    case ba:
    case ha:
    case va:
      return Pe(+e, +t);
    case ya:
      return e.name == t.name && e.message == t.message;
    case Ta:
    case wa:
      return e == t + "";
    case ma:
      var s = pa;
    case Oa:
      var f = r & da;
      if (s || (s = ga), e.size != t.size && !f)
        return !1;
      var c = a.get(e);
      if (c)
        return c == t;
      r |= _a, a.set(e, t);
      var d = Ht(s(e), s(t), r, o, i, a);
      return a.delete(e), d;
    case Aa:
      if (de)
        return de.call(e) == de.call(t);
  }
  return !1;
}
var xa = 1, Ca = Object.prototype, ja = Ca.hasOwnProperty;
function Ea(e, t, n, r, o, i) {
  var a = n & xa, s = me(e), f = s.length, c = me(t), d = c.length;
  if (f != d && !a)
    return !1;
  for (var g = f; g--; ) {
    var _ = s[g];
    if (!(a ? _ in t : ja.call(t, _)))
      return !1;
  }
  var h = i.get(e), u = i.get(t);
  if (h && u)
    return h == t && u == e;
  var p = !0;
  i.set(e, t), i.set(t, e);
  for (var l = a; ++g < f; ) {
    _ = s[g];
    var m = e[_], O = t[_];
    if (r)
      var M = a ? r(O, m, _, t, e, i) : r(m, O, _, e, t, i);
    if (!(M === void 0 ? m === O || o(m, O, n, r, i) : M)) {
      p = !1;
      break;
    }
    l || (l = _ == "constructor");
  }
  if (p && !l) {
    var x = e.constructor, L = t.constructor;
    x != L && "constructor" in e && "constructor" in t && !(typeof x == "function" && x instanceof x && typeof L == "function" && L instanceof L) && (p = !1);
  }
  return i.delete(e), i.delete(t), p;
}
var Ia = 1, pt = "[object Arguments]", gt = "[object Array]", k = "[object Object]", Ma = Object.prototype, dt = Ma.hasOwnProperty;
function La(e, t, n, r, o, i) {
  var a = $(e), s = $(t), f = a ? gt : A(e), c = s ? gt : A(t);
  f = f == pt ? k : f, c = c == pt ? k : c;
  var d = f == k, g = c == k, _ = f == c;
  if (_ && re(e)) {
    if (!re(t))
      return !1;
    a = !0, d = !1;
  }
  if (_ && !d)
    return i || (i = new P()), a || It(e) ? Ht(e, t, n, r, o, i) : Sa(e, t, f, n, r, o, i);
  if (!(n & Ia)) {
    var h = d && dt.call(e, "__wrapped__"), u = g && dt.call(t, "__wrapped__");
    if (h || u) {
      var p = h ? e.value() : e, l = u ? t.value() : t;
      return i || (i = new P()), o(p, l, n, r, i);
    }
  }
  return _ ? (i || (i = new P()), Ea(e, t, n, r, o, i)) : !1;
}
function Ke(e, t, n, r, o) {
  return e === t ? !0 : e == null || t == null || !j(e) && !j(t) ? e !== e && t !== t : La(e, t, n, r, Ke, o);
}
var Ra = 1, Fa = 2;
function Na(e, t, n, r) {
  var o = n.length, i = o;
  if (e == null)
    return !i;
  for (e = Object(e); o--; ) {
    var a = n[o];
    if (a[2] ? a[1] !== e[a[0]] : !(a[0] in e))
      return !1;
  }
  for (; ++o < i; ) {
    a = n[o];
    var s = a[0], f = e[s], c = a[1];
    if (a[2]) {
      if (f === void 0 && !(s in e))
        return !1;
    } else {
      var d = new P(), g;
      if (!(g === void 0 ? Ke(c, f, Ra | Fa, r, d) : g))
        return !1;
    }
  }
  return !0;
}
function qt(e) {
  return e === e && !H(e);
}
function Da(e) {
  for (var t = Q(e), n = t.length; n--; ) {
    var r = t[n], o = e[r];
    t[n] = [r, o, qt(o)];
  }
  return t;
}
function Yt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function Ka(e) {
  var t = Da(e);
  return t.length == 1 && t[0][2] ? Yt(t[0][0], t[0][1]) : function(n) {
    return n === e || Na(n, e, t);
  };
}
function Ua(e, t) {
  return e != null && t in Object(e);
}
function Ga(e, t, n) {
  t = le(t, e);
  for (var r = -1, o = t.length, i = !1; ++r < o; ) {
    var a = V(t[r]);
    if (!(i = e != null && n(e, a)))
      break;
    e = e[a];
  }
  return i || ++r != o ? i : (o = e == null ? 0 : e.length, !!o && Se(o) && Pt(a, o) && ($(e) || Ce(e)));
}
function Ba(e, t) {
  return e != null && Ga(e, t, Ua);
}
var za = 1, Ha = 2;
function qa(e, t) {
  return Ie(e) && qt(t) ? Yt(V(e), t) : function(n) {
    var r = hi(n, e);
    return r === void 0 && r === t ? Ba(n, e) : Ke(t, r, za | Ha);
  };
}
function Ya(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Xa(e) {
  return function(t) {
    return Le(t, e);
  };
}
function Ja(e) {
  return Ie(e) ? Ya(V(e)) : Xa(e);
}
function Za(e) {
  return typeof e == "function" ? e : e == null ? At : typeof e == "object" ? $(e) ? qa(e[0], e[1]) : Ka(e) : Ja(e);
}
function Wa(e) {
  return function(t, n, r) {
    for (var o = -1, i = Object(t), a = r(t), s = a.length; s--; ) {
      var f = a[++o];
      if (n(i[f], f, i) === !1)
        break;
    }
    return t;
  };
}
var Qa = Wa();
function Va(e, t) {
  return e && Qa(e, t, Q);
}
function ka(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function es(e, t) {
  return t.length < 2 ? e : Le(e, xi(t, 0, -1));
}
function ts(e) {
  return e === void 0;
}
function ns(e, t) {
  var n = {};
  return t = Za(t), Va(e, function(r, o, i) {
    $e(n, t(r, o, i), r);
  }), n;
}
function rs(e, t) {
  return t = le(t, e), e = es(e, t), e == null || delete e[V(ka(t))];
}
function is(e) {
  return Si(e) ? void 0 : e;
}
var os = 1, as = 2, ss = 4, Xt = Ti(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = Ot(t, function(i) {
    return i = le(i, e), r || (r = i.length > 1), i;
  }), W(e, Ut(e), n), r && (n = ee(n, os | as | ss, is));
  for (var o = t.length; o--; )
    rs(n, t[o]);
  return n;
});
async function us() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function ls(e) {
  return await us(), e().then((t) => t.default);
}
function fs(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, o) => o === 0 ? r.toLowerCase() : r.toUpperCase());
}
const Jt = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "_selectable", "loading_status", "value_is_output"], cs = Jt.concat(["attached_events"]);
function ps(e, t = {}) {
  return ns(Xt(e, Jt), (n, r) => t[r] || fs(r));
}
function _t(e, t) {
  const {
    gradio: n,
    _internal: r,
    restProps: o,
    originalRestProps: i,
    ...a
  } = e, s = (o == null ? void 0 : o.attachedEvents) || [];
  return Array.from(/* @__PURE__ */ new Set([...Object.keys(r).map((f) => {
    const c = f.match(/bind_(.+)_event/);
    return c && c[1] ? c[1] : null;
  }).filter(Boolean), ...s.map((f) => f)])).reduce((f, c) => {
    const d = c.split("_"), g = (...h) => {
      const u = h.map((l) => h && typeof l == "object" && (l.nativeEvent || l instanceof Event) ? {
        type: l.type,
        detail: l.detail,
        timestamp: l.timeStamp,
        clientX: l.clientX,
        clientY: l.clientY,
        targetId: l.target.id,
        targetClassName: l.target.className,
        altKey: l.altKey,
        ctrlKey: l.ctrlKey,
        shiftKey: l.shiftKey,
        metaKey: l.metaKey
      } : l);
      let p;
      try {
        p = JSON.parse(JSON.stringify(u));
      } catch {
        p = u.map((l) => l && typeof l == "object" ? Object.fromEntries(Object.entries(l).filter(([, m]) => {
          try {
            return JSON.stringify(m), !0;
          } catch {
            return !1;
          }
        })) : l);
      }
      return n.dispatch(c.replace(/[A-Z]/g, (l) => "_" + l.toLowerCase()), {
        payload: p,
        component: {
          ...a,
          ...Xt(i, cs)
        }
      });
    };
    if (d.length > 1) {
      let h = {
        ...a.props[d[0]] || (o == null ? void 0 : o[d[0]]) || {}
      };
      f[d[0]] = h;
      for (let p = 1; p < d.length - 1; p++) {
        const l = {
          ...a.props[d[p]] || (o == null ? void 0 : o[d[p]]) || {}
        };
        h[d[p]] = l, h = l;
      }
      const u = d[d.length - 1];
      return h[`on${u.slice(0, 1).toUpperCase()}${u.slice(1)}`] = g, f;
    }
    const _ = d[0];
    return f[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = g, f;
  }, {});
}
function te() {
}
function gs(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function ds(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return te;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function R(e) {
  let t;
  return ds(e, (n) => t = n)(), t;
}
const G = [];
function F(e, t = te) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function o(s) {
    if (gs(e, s) && (e = s, n)) {
      const f = !G.length;
      for (const c of r)
        c[1](), G.push(c, e);
      if (f) {
        for (let c = 0; c < G.length; c += 2)
          G[c][0](G[c + 1]);
        G.length = 0;
      }
    }
  }
  function i(s) {
    o(s(e));
  }
  function a(s, f = te) {
    const c = [s, f];
    return r.add(c), r.size === 1 && (n = t(o, i) || te), s(e), () => {
      r.delete(c), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: i,
    subscribe: a
  };
}
const {
  getContext: _s,
  setContext: Qs
} = window.__gradio__svelte__internal, bs = "$$ms-gr-loading-status-key";
function hs() {
  const e = window.ms_globals.loadingKey++, t = _s(bs);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: o
    } = t, {
      generating: i,
      error: a
    } = R(o);
    (n == null ? void 0 : n.status) === "pending" || a && (n == null ? void 0 : n.status) === "error" || (i && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
      map: s
    }) => (s.set(e, n), {
      map: s
    })) : r.update(({
      map: s
    }) => (s.delete(e), {
      map: s
    }));
  };
}
const {
  getContext: fe,
  setContext: ce
} = window.__gradio__svelte__internal, ys = "$$ms-gr-slots-key";
function ms() {
  const e = F({});
  return ce(ys, e);
}
const vs = "$$ms-gr-context-key";
function _e(e) {
  return ts(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Zt = "$$ms-gr-sub-index-context-key";
function Ts() {
  return fe(Zt) || null;
}
function bt(e) {
  return ce(Zt, e);
}
function Os(e, t, n) {
  var _, h;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = As(), o = $s({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), i = Ts();
  typeof i == "number" && bt(void 0);
  const a = hs();
  typeof e._internal.subIndex == "number" && bt(e._internal.subIndex), r && r.subscribe((u) => {
    o.slotKey.set(u);
  }), ws();
  const s = fe(vs), f = ((_ = R(s)) == null ? void 0 : _.as_item) || e.as_item, c = _e(s ? f ? ((h = R(s)) == null ? void 0 : h[f]) || {} : R(s) || {} : {}), d = (u, p) => u ? ps({
    ...u,
    ...p || {}
  }, t) : void 0, g = F({
    ...e,
    _internal: {
      ...e._internal,
      index: i ?? e._internal.index
    },
    ...c,
    restProps: d(e.restProps, c),
    originalRestProps: e.restProps
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: p
    } = R(g);
    p && (u = u == null ? void 0 : u[p]), u = _e(u), g.update((l) => ({
      ...l,
      ...u || {},
      restProps: d(l.restProps, u)
    }));
  }), [g, (u) => {
    var l, m;
    const p = _e(u.as_item ? ((l = R(s)) == null ? void 0 : l[u.as_item]) || {} : R(s) || {});
    return a((m = u.restProps) == null ? void 0 : m.loading_status), g.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      ...p,
      restProps: d(u.restProps, p),
      originalRestProps: u.restProps
    });
  }]) : [g, (u) => {
    var p;
    a((p = u.restProps) == null ? void 0 : p.loading_status), g.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      restProps: d(u.restProps),
      originalRestProps: u.restProps
    });
  }];
}
const Wt = "$$ms-gr-slot-key";
function ws() {
  ce(Wt, F(void 0));
}
function As() {
  return fe(Wt);
}
const Qt = "$$ms-gr-component-slot-context-key";
function $s({
  slot: e,
  index: t,
  subIndex: n
}) {
  return ce(Qt, {
    slotKey: F(e),
    slotIndex: F(t),
    subSlotIndex: F(n)
  });
}
function Vs() {
  return fe(Qt);
}
function Ps(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Vt = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function n() {
      for (var i = "", a = 0; a < arguments.length; a++) {
        var s = arguments[a];
        s && (i = o(i, r(s)));
      }
      return i;
    }
    function r(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return n.apply(null, i);
      if (i.toString !== Object.prototype.toString && !i.toString.toString().includes("[native code]"))
        return i.toString();
      var a = "";
      for (var s in i)
        t.call(i, s) && i[s] && (a = o(a, s));
      return a;
    }
    function o(i, a) {
      return a ? i ? i + " " + a : i + a : i;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(Vt);
var Ss = Vt.exports;
const ht = /* @__PURE__ */ Ps(Ss), {
  SvelteComponent: xs,
  assign: we,
  check_outros: Cs,
  claim_component: js,
  component_subscribe: be,
  compute_rest_props: yt,
  create_component: Es,
  create_slot: Is,
  destroy_component: Ms,
  detach: kt,
  empty: ae,
  exclude_internal_props: Ls,
  flush: C,
  get_all_dirty_from_scope: Rs,
  get_slot_changes: Fs,
  get_spread_object: he,
  get_spread_update: Ns,
  group_outros: Ds,
  handle_promise: Ks,
  init: Us,
  insert_hydration: en,
  mount_component: Gs,
  noop: T,
  safe_not_equal: Bs,
  transition_in: B,
  transition_out: Z,
  update_await_block_branch: zs,
  update_slot_base: Hs
} = window.__gradio__svelte__internal;
function mt(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Js,
    then: Ys,
    catch: qs,
    value: 20,
    blocks: [, , ,]
  };
  return Ks(
    /*AwaitedBadgeRibbon*/
    e[2],
    r
  ), {
    c() {
      t = ae(), r.block.c();
    },
    l(o) {
      t = ae(), r.block.l(o);
    },
    m(o, i) {
      en(o, t, i), r.block.m(o, r.anchor = i), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(o, i) {
      e = o, zs(r, e, i);
    },
    i(o) {
      n || (B(r.block), n = !0);
    },
    o(o) {
      for (let i = 0; i < 3; i += 1) {
        const a = r.blocks[i];
        Z(a);
      }
      n = !1;
    },
    d(o) {
      o && kt(t), r.block.d(o), r.token = null, r = null;
    }
  };
}
function qs(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function Ys(e) {
  let t, n;
  const r = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: ht(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-badge-ribbon"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].restProps,
    /*$mergedProps*/
    e[0].props,
    _t(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      text: (
        /*$mergedProps*/
        e[0].props.text || /*$mergedProps*/
        e[0].text
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Xs]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let i = 0; i < r.length; i += 1)
    o = we(o, r[i]);
  return t = new /*BadgeRibbon*/
  e[20]({
    props: o
  }), {
    c() {
      Es(t.$$.fragment);
    },
    l(i) {
      js(t.$$.fragment, i);
    },
    m(i, a) {
      Gs(t, i, a), n = !0;
    },
    p(i, a) {
      const s = a & /*$mergedProps, $slots*/
      3 ? Ns(r, [a & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          i[0].elem_style
        )
      }, a & /*$mergedProps*/
      1 && {
        className: ht(
          /*$mergedProps*/
          i[0].elem_classes,
          "ms-gr-antd-badge-ribbon"
        )
      }, a & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          i[0].elem_id
        )
      }, a & /*$mergedProps*/
      1 && he(
        /*$mergedProps*/
        i[0].restProps
      ), a & /*$mergedProps*/
      1 && he(
        /*$mergedProps*/
        i[0].props
      ), a & /*$mergedProps*/
      1 && he(_t(
        /*$mergedProps*/
        i[0]
      )), a & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          i[1]
        )
      }, a & /*$mergedProps*/
      1 && {
        text: (
          /*$mergedProps*/
          i[0].props.text || /*$mergedProps*/
          i[0].text
        )
      }]) : {};
      a & /*$$scope*/
      131072 && (s.$$scope = {
        dirty: a,
        ctx: i
      }), t.$set(s);
    },
    i(i) {
      n || (B(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Z(t.$$.fragment, i), n = !1;
    },
    d(i) {
      Ms(t, i);
    }
  };
}
function Xs(e) {
  let t;
  const n = (
    /*#slots*/
    e[16].default
  ), r = Is(
    n,
    e,
    /*$$scope*/
    e[17],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(o) {
      r && r.l(o);
    },
    m(o, i) {
      r && r.m(o, i), t = !0;
    },
    p(o, i) {
      r && r.p && (!t || i & /*$$scope*/
      131072) && Hs(
        r,
        n,
        o,
        /*$$scope*/
        o[17],
        t ? Fs(
          n,
          /*$$scope*/
          o[17],
          i,
          null
        ) : Rs(
          /*$$scope*/
          o[17]
        ),
        null
      );
    },
    i(o) {
      t || (B(r, o), t = !0);
    },
    o(o) {
      Z(r, o), t = !1;
    },
    d(o) {
      r && r.d(o);
    }
  };
}
function Js(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function Zs(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && mt(e)
  );
  return {
    c() {
      r && r.c(), t = ae();
    },
    l(o) {
      r && r.l(o), t = ae();
    },
    m(o, i) {
      r && r.m(o, i), en(o, t, i), n = !0;
    },
    p(o, [i]) {
      /*$mergedProps*/
      o[0].visible ? r ? (r.p(o, i), i & /*$mergedProps*/
      1 && B(r, 1)) : (r = mt(o), r.c(), B(r, 1), r.m(t.parentNode, t)) : r && (Ds(), Z(r, 1, 1, () => {
        r = null;
      }), Cs());
    },
    i(o) {
      n || (B(r), n = !0);
    },
    o(o) {
      Z(r), n = !1;
    },
    d(o) {
      o && kt(t), r && r.d(o);
    }
  };
}
function Ws(e, t, n) {
  const r = ["gradio", "props", "_internal", "text", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = yt(t, r), i, a, s, {
    $$slots: f = {},
    $$scope: c
  } = t;
  const d = ls(() => import("./badge.ribbon-Csm6ChEx.js"));
  let {
    gradio: g
  } = t, {
    props: _ = {}
  } = t;
  const h = F(_);
  be(e, h, (b) => n(15, i = b));
  let {
    _internal: u = {}
  } = t, {
    text: p = ""
  } = t, {
    as_item: l
  } = t, {
    visible: m = !0
  } = t, {
    elem_id: O = ""
  } = t, {
    elem_classes: M = []
  } = t, {
    elem_style: x = {}
  } = t;
  const [L, tn] = Os({
    gradio: g,
    props: i,
    _internal: u,
    visible: m,
    elem_id: O,
    elem_classes: M,
    elem_style: x,
    as_item: l,
    text: p,
    restProps: o
  });
  be(e, L, (b) => n(0, a = b));
  const Ue = ms();
  return be(e, Ue, (b) => n(1, s = b)), e.$$set = (b) => {
    t = we(we({}, t), Ls(b)), n(19, o = yt(t, r)), "gradio" in b && n(6, g = b.gradio), "props" in b && n(7, _ = b.props), "_internal" in b && n(8, u = b._internal), "text" in b && n(9, p = b.text), "as_item" in b && n(10, l = b.as_item), "visible" in b && n(11, m = b.visible), "elem_id" in b && n(12, O = b.elem_id), "elem_classes" in b && n(13, M = b.elem_classes), "elem_style" in b && n(14, x = b.elem_style), "$$scope" in b && n(17, c = b.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && h.update((b) => ({
      ...b,
      ..._
    })), tn({
      gradio: g,
      props: i,
      _internal: u,
      visible: m,
      elem_id: O,
      elem_classes: M,
      elem_style: x,
      as_item: l,
      text: p,
      restProps: o
    });
  }, [a, s, d, h, L, Ue, g, _, u, p, l, m, O, M, x, i, f, c];
}
class ks extends xs {
  constructor(t) {
    super(), Us(this, t, Ws, Zs, Bs, {
      gradio: 6,
      props: 7,
      _internal: 8,
      text: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), C();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), C();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), C();
  }
  get text() {
    return this.$$.ctx[9];
  }
  set text(t) {
    this.$$set({
      text: t
    }), C();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), C();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), C();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), C();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), C();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), C();
  }
}
export {
  ks as I,
  Vs as g,
  F as w
};
