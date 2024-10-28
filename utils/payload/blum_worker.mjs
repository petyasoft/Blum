import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const self = global;


    "use strict";
    const v = globalThis || void 0 || self;
    let _;
    const g = new Array(128).fill(void 0);
    g.push(void 0, null, !0, !1);
    function c(e) {
        return g[e]
    }
    let m = g.length;
    function M(e) {
        e < 132 || (g[e] = m,
            m = e)
    }
    function w(e) {
        const n = c(e);
        return M(e),
            n
    }
    let d = 0
        , p = null;
    function S() {
        return (p === null || p.byteLength === 0) && (p = new Uint8Array(_.memory.buffer)),
            p
    }
    const O = typeof TextEncoder < "u" ? new TextEncoder("utf-8") : {
        encode: () => {
            throw Error("TextEncoder not available")
        }
    }
        , W = typeof O.encodeInto == "function" ? function (e, n) {
            return O.encodeInto(e, n)
        }
            : function (e, n) {
                const t = O.encode(e);
                return n.set(t),
                {
                    read: e.length,
                    written: t.length
                }
            }
        ;
    function h(e, n, t) {
        if (t === void 0) {
            const a = O.encode(e)
                , y = n(a.length, 1) >>> 0;
            return S().subarray(y, y + a.length).set(a),
                d = a.length,
                y
        }
        let r = e.length
            , o = n(r, 1) >>> 0;
        const f = S();
        let s = 0;
        for (; s < r; s++) {
            const a = e.charCodeAt(s);
            if (a > 127)
                break;
            f[o + s] = a
        }
        if (s !== r) {
            s !== 0 && (e = e.slice(s)),
                o = t(o, r, r = s + e.length * 3, 1) >>> 0;
            const a = S().subarray(o + s, o + r)
                , y = W(e, a);
            s += y.written,
                o = t(o, r, s, 1) >>> 0
        }
        return d = s,
            o
    }
    function I(e) {
        return e == null
    }
    let l = null;
    function u() {
        return (l === null || l.buffer.detached === !0 || l.buffer.detached === void 0 && l.buffer !== _.memory.buffer) && (l = new DataView(_.memory.buffer)),
            l
    }
    function i(e) {
        m === g.length && g.push(g.length + 1);
        const n = m;
        return m = g[n],
            g[n] = e,
            n
    }
    const E = typeof TextDecoder < "u" ? new TextDecoder("utf-8", {
        ignoreBOM: !0,
        fatal: !0
    }) : {
        decode: () => {
            throw Error("TextDecoder not available")
        }
    };
    typeof TextDecoder < "u" && E.decode();
    function A(e, n) {
        return e = e >>> 0,
            E.decode(S().subarray(e, e + n))
    }
    function T(e) {
        const n = typeof e;
        if (n == "number" || n == "boolean" || e == null)
            return `${e}`;
        if (n == "string")
            return `"${e}"`;
        if (n == "symbol") {
            const o = e.description;
            return o == null ? "Symbol" : `Symbol(${o})`
        }
        if (n == "function") {
            const o = e.name;
            return typeof o == "string" && o.length > 0 ? `Function(${o})` : "Function"
        }
        if (Array.isArray(e)) {
            const o = e.length;
            let f = "[";
            o > 0 && (f += T(e[0]));
            for (let s = 1; s < o; s++)
                f += ", " + T(e[s]);
            return f += "]",
                f
        }
        const t = /\[object ([^\]]+)\]/.exec(toString.call(e));
        let r;
        if (t.length > 1)
            r = t[1];
        else
            return toString.call(e);
        if (r == "Object")
            try {
                return "Object(" + JSON.stringify(e) + ")"
            } catch {
                return "Object"
            }
        return e instanceof Error ? `${e.name}: ${e.message}
${e.stack}` : r
    }
    function F(e) {
        try {
            const o = _.__wbindgen_add_to_stack_pointer(-16)
                , f = h(e, _.__wbindgen_malloc, _.__wbindgen_realloc)
                , s = d;
            _.proof(o, f, s);
            var n = u().getInt32(o + 4 * 0, !0)
                , t = u().getInt32(o + 4 * 1, !0)
                , r = u().getInt32(o + 4 * 2, !0);
            if (r)
                throw w(t);
            return w(n)
        } finally {
            _.__wbindgen_add_to_stack_pointer(16)
        }
    }
    function B(e, n, t) {
        let r, o;
        try {
            const j = _.__wbindgen_add_to_stack_pointer(-16)
                , q = h(e, _.__wbindgen_malloc, _.__wbindgen_realloc)
                , N = d;
            _.pack(j, q, N, i(n), i(t));
            var f = u().getInt32(j + 4 * 0, !0)
                , s = u().getInt32(j + 4 * 1, !0)
                , a = u().getInt32(j + 4 * 2, !0)
                , y = u().getInt32(j + 4 * 3, !0)
                , k = f
                , U = s;
            if (y)
                throw k = 0,
                U = 0,
                w(a);
            return r = k,
                o = U,
                A(k, U)
        } finally {
            _.__wbindgen_add_to_stack_pointer(16),
                _.__wbindgen_free(r, o, 1)
        }
    }
    function b(e, n) {
        try {
            return e.apply(this, n)
        } catch (t) {
            _.__wbindgen_exn_store(i(t))
        }
    }
    async function D(e, n) {
        if (typeof Response == "function" && e instanceof Response) {
            if (typeof WebAssembly.instantiateStreaming == "function")
                try {
                    return await WebAssembly.instantiateStreaming(e, n)
                } catch (r) {
                    if (e.headers.get("Content-Type") != "application/wasm")
                        console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n", r);
                    else
                        throw r
                }
            const t = await e.arrayBuffer();
            return await WebAssembly.instantiate(t, n)
        } else {
            const t = await WebAssembly.instantiate(e, n);
            return t instanceof WebAssembly.Instance ? {
                instance: t,
                module: e
            } : t
        }
    }
    function $() {
        const e = {};
        return e.wbg = {},
            e.wbg.__wbindgen_object_drop_ref = function (n) {
                w(n)
            }
            ,
            e.wbg.__wbindgen_string_get = function (n, t) {
                const r = c(t)
                    , o = typeof r == "string" ? r : void 0;
                var f = I(o) ? 0 : h(o, _.__wbindgen_malloc, _.__wbindgen_realloc)
                    , s = d;
                u().setInt32(n + 4 * 1, s, !0),
                    u().setInt32(n + 4 * 0, f, !0)
            }
            ,
            e.wbg.__wbindgen_is_object = function (n) {
                const t = c(n);
                return typeof t == "object" && t !== null
            }
            ,
            e.wbg.__wbindgen_is_undefined = function (n) {
                return c(n) === void 0
            }
            ,
            e.wbg.__wbindgen_in = function (n, t) {
                return c(n) in c(t)
            }
            ,
            e.wbg.__wbindgen_is_bigint = function (n) {
                return typeof c(n) == "bigint"
            }
            ,
            e.wbg.__wbindgen_bigint_from_u64 = function (n) {
                const t = BigInt.asUintN(64, n);
                return i(t)
            }
            ,
            e.wbg.__wbindgen_jsval_eq = function (n, t) {
                return c(n) === c(t)
            }
            ,
            e.wbg.__wbindgen_error_new = function (n, t) {
                const r = new Error(A(n, t));
                return i(r)
            }
            ,
            e.wbg.__wbg_crypto_1d1f22824a6a080c = function (n) {
                const t = c(n).crypto;
                return i(t)
            }
            ,
            e.wbg.__wbg_process_4a72847cc503995b = function (n) {
                const t = c(n).process;
                return i(t)
            }
            ,
            e.wbg.__wbg_versions_f686565e586dd935 = function (n) {
                const t = c(n).versions;
                return i(t)
            }
            ,
            e.wbg.__wbg_node_104a2ff8d6ea03a2 = function (n) {
                const t = c(n).node;
                return i(t)
            }
            ,
            e.wbg.__wbindgen_is_string = function (n) {
                return typeof c(n) == "string"
            }
            ,
            e.wbg.__wbg_require_cca90b1a94a0255b = function () {
                return b(function () {
                    const n = module.require;
                    return i(n)
                }, arguments)
            }
            ,
            e.wbg.__wbindgen_is_function = function (n) {
                return typeof c(n) == "function"
            }
            ,
            e.wbg.__wbindgen_string_new = function (n, t) {
                const r = A(n, t);
                return i(r)
            }
            ,
            e.wbg.__wbg_msCrypto_eb05e62b530a1508 = function (n) {
                const t = c(n).msCrypto;
                return i(t)
            }
            ,
            e.wbg.__wbg_randomFillSync_5c9c955aa56b6049 = function () {
                return b(function (n, t) {
                    c(n).randomFillSync(w(t))
                }, arguments)
            }
            ,
            e.wbg.__wbg_getRandomValues_3aa56aa6edec874c = function () {
                return b(function (n, t) {
                    c(n).getRandomValues(c(t))
                }, arguments)
            }
            ,
            e.wbg.__wbindgen_jsval_loose_eq = function (n, t) {
                return c(n) == c(t)
            }
            ,
            e.wbg.__wbindgen_boolean_get = function (n) {
                const t = c(n);
                return typeof t == "boolean" ? t ? 1 : 0 : 2
            }
            ,
            e.wbg.__wbindgen_number_get = function (n, t) {
                const r = c(t)
                    , o = typeof r == "number" ? r : void 0;
                u().setFloat64(n + 8 * 1, I(o) ? 0 : o, !0),
                    u().setInt32(n + 4 * 0, !I(o), !0)
            }
            ,
            e.wbg.__wbindgen_as_number = function (n) {
                return +c(n)
            }
            ,
            e.wbg.__wbg_String_b9412f8799faab3e = function (n, t) {
                const r = String(c(t))
                    , o = h(r, _.__wbindgen_malloc, _.__wbindgen_realloc)
                    , f = d;
                u().setInt32(n + 4 * 1, f, !0),
                    u().setInt32(n + 4 * 0, o, !0)
            }
            ,
            e.wbg.__wbindgen_number_new = function (n) {
                return i(n)
            }
            ,
            e.wbg.__wbindgen_object_clone_ref = function (n) {
                const t = c(n);
                return i(t)
            }
            ,
            e.wbg.__wbg_getwithrefkey_edc2c8960f0f1191 = function (n, t) {
                const r = c(n)[c(t)];
                return i(r)
            }
            ,
            e.wbg.__wbg_set_f975102236d3c502 = function (n, t, r) {
                c(n)[w(t)] = w(r)
            }
            ,
            e.wbg.__wbg_get_3baa728f9d58d3f6 = function (n, t) {
                const r = c(n)[t >>> 0];
                return i(r)
            }
            ,
            e.wbg.__wbg_length_ae22078168b726f5 = function (n) {
                return c(n).length
            }
            ,
            e.wbg.__wbg_newnoargs_76313bd6ff35d0f2 = function (n, t) {
                const r = new Function(A(n, t));
                return i(r)
            }
            ,
            e.wbg.__wbg_next_de3e9db4440638b2 = function (n) {
                const t = c(n).next;
                return i(t)
            }
            ,
            e.wbg.__wbg_next_f9cb570345655b9a = function () {
                return b(function (n) {
                    const t = c(n).next();
                    return i(t)
                }, arguments)
            }
            ,
            e.wbg.__wbg_done_bfda7aa8f252b39f = function (n) {
                return c(n).done
            }
            ,
            e.wbg.__wbg_value_6d39332ab4788d86 = function (n) {
                const t = c(n).value;
                return i(t)
            }
            ,
            e.wbg.__wbg_iterator_888179a48810a9fe = function () {
                return i(Symbol.iterator)
            }
            ,
            e.wbg.__wbg_get_224d16597dbbfd96 = function () {
                return b(function (n, t) {
                    const r = Reflect.get(c(n), c(t));
                    return i(r)
                }, arguments)
            }
            ,
            e.wbg.__wbg_call_1084a111329e68ce = function () {
                return b(function (n, t) {
                    const r = c(n).call(c(t));
                    return i(r)
                }, arguments)
            }
            ,
            e.wbg.__wbg_new_525245e2b9901204 = function () {
                const n = new Object;
                return i(n)
            }
            ,
            e.wbg.__wbg_self_3093d5d1f7bcb682 = function () {
                return b(function () {
                    const n = self.self;
                    return i(n)
                }, arguments)
            }
            ,
            e.wbg.__wbg_window_3bcfc4d31bc012f8 = function () {
                return b(function () {
                    const n = window.window;
                    return i(n)
                }, arguments)
            }
            ,
            e.wbg.__wbg_globalThis_86b222e13bdf32ed = function () {
                return b(function () {
                    const n = globalThis.globalThis;
                    return i(n)
                }, arguments)
            }
            ,
            e.wbg.__wbg_global_e5a3fe56f8be9485 = function () {
                return b(function () {
                    const n = v.global;
                    return i(n)
                }, arguments)
            }
            ,
            e.wbg.__wbg_instanceof_ArrayBuffer_61dfc3198373c902 = function (n) {
                let t;
                try {
                    t = c(n) instanceof ArrayBuffer
                } catch {
                    t = !1
                }
                return t
            }
            ,
            e.wbg.__wbg_call_89af060b4e1523f2 = function () {
                return b(function (n, t, r) {
                    const o = c(n).call(c(t), c(r));
                    return i(o)
                }, arguments)
            }
            ,
            e.wbg.__wbg_isSafeInteger_7f1ed56200d90674 = function (n) {
                return Number.isSafeInteger(c(n))
            }
            ,
            e.wbg.__wbg_entries_7a0e06255456ebcd = function (n) {
                const t = Object.entries(c(n));
                return i(t)
            }
            ,
            e.wbg.__wbg_buffer_b7b08af79b0b0974 = function (n) {
                const t = c(n).buffer;
                return i(t)
            }
            ,
            e.wbg.__wbg_newwithbyteoffsetandlength_8a2cb9ca96b27ec9 = function (n, t, r) {
                const o = new Uint8Array(c(n), t >>> 0, r >>> 0);
                return i(o)
            }
            ,
            e.wbg.__wbg_new_ea1883e1e5e86686 = function (n) {
                const t = new Uint8Array(c(n));
                return i(t)
            }
            ,
            e.wbg.__wbg_set_d1e79e2388520f18 = function (n, t, r) {
                c(n).set(c(t), r >>> 0)
            }
            ,
            e.wbg.__wbg_length_8339fcf5d8ecd12e = function (n) {
                return c(n).length
            }
            ,
            e.wbg.__wbg_instanceof_Uint8Array_247a91427532499e = function (n) {
                let t;
                try {
                    t = c(n) instanceof Uint8Array
                } catch {
                    t = !1
                }
                return t
            }
            ,
            e.wbg.__wbg_newwithlength_ec548f448387c968 = function (n) {
                const t = new Uint8Array(n >>> 0);
                return i(t)
            }
            ,
            e.wbg.__wbg_subarray_7c2e3576afe181d1 = function (n, t, r) {
                const o = c(n).subarray(t >>> 0, r >>> 0);
                return i(o)
            }
            ,
            e.wbg.__wbindgen_bigint_get_as_i64 = function (n, t) {
                const r = c(t)
                    , o = typeof r == "bigint" ? r : void 0;
                u().setBigInt64(n + 8 * 1, I(o) ? BigInt(0) : o, !0),
                    u().setInt32(n + 4 * 0, !I(o), !0)
            }
            ,
            e.wbg.__wbindgen_debug_string = function (n, t) {
                const r = T(c(t))
                    , o = h(r, _.__wbindgen_malloc, _.__wbindgen_realloc)
                    , f = d;
                u().setInt32(n + 4 * 1, f, !0),
                    u().setInt32(n + 4 * 0, o, !0)
            }
            ,
            e.wbg.__wbindgen_throw = function (n, t) {
                throw new Error(A(n, t))
            }
            ,
            e.wbg.__wbindgen_memory = function () {
                const n = _.memory;
                return i(n)
            }
            ,
            e
    }
    function L(e, n) {
        return _ = e.exports,
            R.__wbindgen_wasm_module = n,
            l = null,
            p = null,
            _
    }
    async function R(e) {
        if (_ !== void 0)
            return _;
        const n = $();
        e = fs.readFileSync(path.resolve(__dirname, './blum_wasm.wasm'));
        const { instance: t, module: r } = await D(await e, n);
        return L(t, r)
    }
    let x;
    const V = async () => {
        x === void 0 && (x = R()),
            await x
    };
    self.onmessage = async e => {
        await V();
        const { id: n, method: t, payload: r } = e.data;
        switch (t) {
            case "proof":
                {
                    const o = F(r);
                    return self.postMessage({
                        id: n,
                        ...o
                    })
                }
            case "pack":
                {
                    const o = B(r.gameId, r.challenge, r.earnedAssets);
                    return self.postMessage({
                        id: n,
                        hash: o
                    })
                }
            default:
                {
                    const o = t;
                    throw err(`Unknown method: ${o}`)
                }
        }
    }

    const uuid = () => "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, ue => {
        const Yi = Math.random() * 16 | 0;
        return (ue === "x" ? Yi : Yi & 3 | 8).toString(16)
    });

    export const Blum = {
        getUUID: null,
        getChallenge: null,
        getPayload: null,
        init: async function() {
            await V();
            this.getChallenge = F;
            this.getPayload = B;
            this.getUUID = uuid;
        }
    };
    await Blum.init();


