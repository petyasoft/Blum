import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const self = global;

    "use strict";
    const j = globalThis || void 0 || self;
    let c, b = 0, w = null;
    function m() {
        return (w === null || w.byteLength === 0) && (w = new Uint8Array(c.memory.buffer)),
        w
    }
    const h = typeof TextEncoder < "u" ? new TextEncoder("utf-8") : {
        encode: () => {
            throw Error("TextEncoder not available")
        }
    }
      , E = typeof h.encodeInto == "function" ? function(n, e) {
        return h.encodeInto(n, e)
    }
    : function(n, e) {
        const t = h.encode(n);
        return e.set(t),
        {
            read: n.length,
            written: t.length
        }
    }
    ;
    function d(n, e, t) {
        if (t === void 0) {
            const _ = h.encode(n)
              , g = e(_.length, 1) >>> 0;
            return m().subarray(g, g + _.length).set(_),
            b = _.length,
            g
        }
        let r = n.length
          , o = e(r, 1) >>> 0;
        const s = m();
        let i = 0;
        for (; i < r; i++) {
            const _ = n.charCodeAt(i);
            if (_ > 127)
                break;
            s[o + i] = _
        }
        if (i !== r) {
            i !== 0 && (n = n.slice(i)),
            o = t(o, r, r = i + n.length * 3, 1) >>> 0;
            const _ = m().subarray(o + i, o + r)
              , g = E(n, _);
            i += g.written,
            o = t(o, r, i, 1) >>> 0
        }
        return b = i,
        o
    }
    function l(n) {
        return n == null
    }
    let a = null;
    function u() {
        return (a === null || a.buffer.detached === !0 || a.buffer.detached === void 0 && a.buffer !== c.memory.buffer) && (a = new DataView(c.memory.buffer)),
        a
    }
    const I = typeof TextDecoder < "u" ? new TextDecoder("utf-8",{
        ignoreBOM: !0,
        fatal: !0
    }) : {
        decode: () => {
            throw Error("TextDecoder not available")
        }
    };
    typeof TextDecoder < "u" && I.decode();
    function y(n, e) {
        return n = n >>> 0,
        I.decode(m().subarray(n, n + e))
    }
    function x(n) {
        const e = typeof n;
        if (e == "number" || e == "boolean" || n == null)
            return `${n}`;
        if (e == "string")
            return `"${n}"`;
        if (e == "symbol") {
            const o = n.description;
            return o == null ? "Symbol" : `Symbol(${o})`
        }
        if (e == "function") {
            const o = n.name;
            return typeof o == "string" && o.length > 0 ? `Function(${o})` : "Function"
        }
        if (Array.isArray(n)) {
            const o = n.length;
            let s = "[";
            o > 0 && (s += x(n[0]));
            for (let i = 1; i < o; i++)
                s += ", " + x(n[i]);
            return s += "]",
            s
        }
        const t = /\[object ([^\]]+)\]/.exec(toString.call(n));
        let r;
        if (t.length > 1)
            r = t[1];
        else
            return toString.call(n);
        if (r == "Object")
            try {
                return "Object(" + JSON.stringify(n) + ")"
            } catch {
                return "Object"
            }
        return n instanceof Error ? `${n.name}: ${n.message}
${n.stack}` : r
    }
    function A(n) {
        const e = c.__wbindgen_export_2.get(n);
        return c.__externref_table_dealloc(n),
        e
    }
    function U(n) {
        const e = d(n, c.__wbindgen_malloc, c.__wbindgen_realloc)
          , t = b
          , r = c.proof(e, t);
        if (r[2])
            throw A(r[1]);
        return A(r[0])
    }
    function R(n, e, t, r) {
        let o, s;
        try {
            const g = d(n, c.__wbindgen_malloc, c.__wbindgen_realloc)
              , B = b
              , p = c.pack(g, B, e, t, r);
            var i = p[0]
              , _ = p[1];
            if (p[3])
                throw i = 0,
                _ = 0,
                A(p[2]);
            return o = i,
            s = _,
            y(i, _)
        } finally {
            c.__wbindgen_free(o, s, 1)
        }
    }
    function O(n) {
        const e = c.__externref_table_alloc();
        return c.__wbindgen_export_2.set(e, n),
        e
    }
    function f(n, e) {
        try {
            return n.apply(this, e)
        } catch (t) {
            const r = O(t);
            c.__wbindgen_exn_store(r)
        }
    }
    async function W(n, e) {
        if (typeof Response == "function" && n instanceof Response) {
            if (typeof WebAssembly.instantiateStreaming == "function")
                try {
                    return await WebAssembly.instantiateStreaming(n, e)
                } catch (r) {
                    if (n.headers.get("Content-Type") != "application/wasm")
                        console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve Wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n", r);
                    else
                        throw r
                }
            const t = await n.arrayBuffer();
            return await WebAssembly.instantiate(t, e)
        } else {
            const t = await WebAssembly.instantiate(n, e);
            return t instanceof WebAssembly.Instance ? {
                instance: t,
                module: n
            } : t
        }
    }
    function k() {
        const n = {};
        return n.wbg = {},
        n.wbg.__wbindgen_string_get = function(e, t) {
            const r = t
              , o = typeof r == "string" ? r : void 0;
            var s = l(o) ? 0 : d(o, c.__wbindgen_malloc, c.__wbindgen_realloc)
              , i = b;
            u().setInt32(e + 4 * 1, i, !0),
            u().setInt32(e + 4 * 0, s, !0)
        }
        ,
        n.wbg.__wbindgen_error_new = function(e, t) {
            return new Error(y(e, t))
        }
        ,
        n.wbg.__wbindgen_string_new = function(e, t) {
            return y(e, t)
        }
        ,
        n.wbg.__wbindgen_is_object = function(e) {
            const t = e;
            return typeof t == "object" && t !== null
        }
        ,
        n.wbg.__wbindgen_is_string = function(e) {
            return typeof e == "string"
        }
        ,
        n.wbg.__wbindgen_is_bigint = function(e) {
            return typeof e == "bigint"
        }
        ,
        n.wbg.__wbindgen_bigint_from_u64 = function(e) {
            return BigInt.asUintN(64, e)
        }
        ,
        n.wbg.__wbindgen_jsval_eq = function(e, t) {
            return e === t
        }
        ,
        n.wbg.__wbindgen_is_undefined = function(e) {
            return e === void 0
        }
        ,
        n.wbg.__wbindgen_in = function(e, t) {
            return e in t
        }
        ,
        n.wbg.__wbg_crypto_1d1f22824a6a080c = function(e) {
            return e.crypto
        }
        ,
        n.wbg.__wbg_process_4a72847cc503995b = function(e) {
            return e.process
        }
        ,
        n.wbg.__wbg_versions_f686565e586dd935 = function(e) {
            return e.versions
        }
        ,
        n.wbg.__wbg_node_104a2ff8d6ea03a2 = function(e) {
            return e.node
        }
        ,
        n.wbg.__wbg_require_cca90b1a94a0255b = function() {
            return f(function() {
                return module.require
            }, arguments)
        }
        ,
        n.wbg.__wbindgen_is_function = function(e) {
            return typeof e == "function"
        }
        ,
        n.wbg.__wbg_msCrypto_eb05e62b530a1508 = function(e) {
            return e.msCrypto
        }
        ,
        n.wbg.__wbg_randomFillSync_5c9c955aa56b6049 = function() {
            return f(function(e, t) {
                e.randomFillSync(t)
            }, arguments)
        }
        ,
        n.wbg.__wbg_getRandomValues_3aa56aa6edec874c = function() {
            return f(function(e, t) {
                e.getRandomValues(t)
            }, arguments)
        }
        ,
        n.wbg.__wbindgen_jsval_loose_eq = function(e, t) {
            return e == t
        }
        ,
        n.wbg.__wbindgen_boolean_get = function(e) {
            const t = e;
            return typeof t == "boolean" ? t ? 1 : 0 : 2
        }
        ,
        n.wbg.__wbindgen_number_get = function(e, t) {
            const r = t
              , o = typeof r == "number" ? r : void 0;
            u().setFloat64(e + 8 * 1, l(o) ? 0 : o, !0),
            u().setInt32(e + 4 * 0, !l(o), !0)
        }
        ,
        n.wbg.__wbindgen_as_number = function(e) {
            return +e
        }
        ,
        n.wbg.__wbg_String_b9412f8799faab3e = function(e, t) {
            const r = String(t)
              , o = d(r, c.__wbindgen_malloc, c.__wbindgen_realloc)
              , s = b;
            u().setInt32(e + 4 * 1, s, !0),
            u().setInt32(e + 4 * 0, o, !0)
        }
        ,
        n.wbg.__wbindgen_number_new = function(e) {
            return e
        }
        ,
        n.wbg.__wbg_getwithrefkey_edc2c8960f0f1191 = function(e, t) {
            return e[t]
        }
        ,
        n.wbg.__wbg_set_f975102236d3c502 = function(e, t, r) {
            e[t] = r
        }
        ,
        n.wbg.__wbg_get_5419cf6b954aa11d = function(e, t) {
            return e[t >>> 0]
        }
        ,
        n.wbg.__wbg_length_f217bbbf7e8e4df4 = function(e) {
            return e.length
        }
        ,
        n.wbg.__wbg_newnoargs_1ede4bf2ebbaaf43 = function(e, t) {
            return new Function(y(e, t))
        }
        ,
        n.wbg.__wbg_next_13b477da1eaa3897 = function(e) {
            return e.next
        }
        ,
        n.wbg.__wbg_next_b06e115d1b01e10b = function() {
            return f(function(e) {
                return e.next()
            }, arguments)
        }
        ,
        n.wbg.__wbg_done_983b5ffcaec8c583 = function(e) {
            return e.done
        }
        ,
        n.wbg.__wbg_value_2ab8a198c834c26a = function(e) {
            return e.value
        }
        ,
        n.wbg.__wbg_iterator_695d699a44d6234c = function() {
            return Symbol.iterator
        }
        ,
        n.wbg.__wbg_get_ef828680c64da212 = function() {
            return f(function(e, t) {
                return Reflect.get(e, t)
            }, arguments)
        }
        ,
        n.wbg.__wbg_call_a9ef466721e824f2 = function() {
            return f(function(e, t) {
                return e.call(t)
            }, arguments)
        }
        ,
        n.wbg.__wbg_new_e69b5f66fda8f13c = function() {
            return new Object
        }
        ,
        n.wbg.__wbg_self_bf91bf94d9e04084 = function() {
            return f(function() {
                return self.self
            }, arguments)
        }
        ,
        n.wbg.__wbg_window_52dd9f07d03fd5f8 = function() {
            return f(function() {
                return window.window
            }, arguments)
        }
        ,
        n.wbg.__wbg_globalThis_05c129bf37fcf1be = function() {
            return f(function() {
                return globalThis.globalThis
            }, arguments)
        }
        ,
        n.wbg.__wbg_global_3eca19bb09e9c484 = function() {
            return f(function() {
                return j.global
            }, arguments)
        }
        ,
        n.wbg.__wbg_instanceof_ArrayBuffer_74945570b4a62ec7 = function(e) {
            let t;
            try {
                t = e instanceof ArrayBuffer
            } catch {
                t = !1
            }
            return t
        }
        ,
        n.wbg.__wbg_call_3bfa248576352471 = function() {
            return f(function(e, t, r) {
                return e.call(t, r)
            }, arguments)
        }
        ,
        n.wbg.__wbg_isSafeInteger_b9dff570f01a9100 = function(e) {
            return Number.isSafeInteger(e)
        }
        ,
        n.wbg.__wbg_entries_c02034de337d3ee2 = function(e) {
            return Object.entries(e)
        }
        ,
        n.wbg.__wbg_buffer_ccaed51a635d8a2d = function(e) {
            return e.buffer
        }
        ,
        n.wbg.__wbg_newwithbyteoffsetandlength_7e3eb787208af730 = function(e, t, r) {
            return new Uint8Array(e,t >>> 0,r >>> 0)
        }
        ,
        n.wbg.__wbg_new_fec2611eb9180f95 = function(e) {
            return new Uint8Array(e)
        }
        ,
        n.wbg.__wbg_set_ec2fcf81bc573fd9 = function(e, t, r) {
            e.set(t, r >>> 0)
        }
        ,
        n.wbg.__wbg_length_9254c4bd3b9f23c4 = function(e) {
            return e.length
        }
        ,
        n.wbg.__wbg_instanceof_Uint8Array_df0761410414ef36 = function(e) {
            let t;
            try {
                t = e instanceof Uint8Array
            } catch {
                t = !1
            }
            return t
        }
        ,
        n.wbg.__wbg_newwithlength_76462a666eca145f = function(e) {
            return new Uint8Array(e >>> 0)
        }
        ,
        n.wbg.__wbg_subarray_975a06f9dbd16995 = function(e, t, r) {
            return e.subarray(t >>> 0, r >>> 0)
        }
        ,
        n.wbg.__wbg_has_bd717f25f195f23d = function() {
            return f(function(e, t) {
                return Reflect.has(e, t)
            }, arguments)
        }
        ,
        n.wbg.__wbindgen_bigint_get_as_i64 = function(e, t) {
            const r = t
              , o = typeof r == "bigint" ? r : void 0;
            u().setBigInt64(e + 8 * 1, l(o) ? BigInt(0) : o, !0),
            u().setInt32(e + 4 * 0, !l(o), !0)
        }
        ,
        n.wbg.__wbindgen_debug_string = function(e, t) {
            const r = x(t)
              , o = d(r, c.__wbindgen_malloc, c.__wbindgen_realloc)
              , s = b;
            u().setInt32(e + 4 * 1, s, !0),
            u().setInt32(e + 4 * 0, o, !0)
        }
        ,
        n.wbg.__wbindgen_throw = function(e, t) {
            throw new Error(y(e, t))
        }
        ,
        n.wbg.__wbindgen_memory = function() {
            return c.memory
        }
        ,
        n.wbg.__wbindgen_init_externref_table = function() {
            const e = c.__wbindgen_export_2
              , t = e.grow(4);
            e.set(0, void 0),
            e.set(t + 0, void 0),
            e.set(t + 1, null),
            e.set(t + 2, !0),
            e.set(t + 3, !1)
        }
        ,
        n
    }
    function M(n, e) {
        return c = n.exports,
        T.__wbindgen_wasm_module = e,
        a = null,
        w = null,
        c.__wbindgen_start(),
        c
    }
    async function T(n) {
        if (c !== void 0)
            return c;
        n = fs.readFileSync(path.resolve(__dirname, './blum_wasm.wasm'));
        const e = k();
        (typeof n == "string" || typeof Request == "function" && n instanceof Request || typeof URL == "function" && n instanceof URL) && (n = fetch(n));
        const {instance: t, module: r} = await W(await n, e);
        return M(t, r)
    }
    let S;
    const F = async () => {
        S === void 0 && (S = T()),
        await S
    }
    ;
    self.onmessage = async n => {
        await F();
        const {id: e, method: t, payload: r} = n.data;
        switch (t) {
        case "proof":
            {
                const o = U(r);
                return self.postMessage({
                    id: e,
                    ...o
                })
            }
        case "pack":
            {
                const o = R(r.gameId, r.challenge, r.earnedPoints, r.assetClicks);
                return self.postMessage({
                    id: e,
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
            await F();
            this.getChallenge = U;
            this.getPayload = R;
            this.getUUID = uuid;
        }
    };
    await Blum.init();
