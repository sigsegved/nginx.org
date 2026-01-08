# Совместимость

**Revision:** 44  
**Language:** ru

njs совместим с [ECMAScript 5.1](http://www.ecma-international.org/ecma-262/5.1/) (строгий режим) c некоторыми расширениями [ECMAScript 6](http://www.ecma-international.org/ecma-262/6.0/) и позже. Совместимость находится в стадии развития.

Описания методов и свойств, доступных только в njs и не соответствующих стандарту ECMAScript, доступны в [справочнике](reference.xml) . Описания методов и свойств njs, соответствующих стандарту, доступны в [спецификации ECMAScript](http://www.ecma-international.org/ecma-262/) .

# Готовая функциональность {#supported}

- Логические значения, числа, строки, объекты, массивы,
функции, конструкторы функций
( [0.3.6](changes.xml#njs0.3.6) )
и регулярные выражения
- ES5.1 операторы, ES7 операторы возведения в степень
- ES5.1 инструкции: `break` , `catch` , `continue` , `do while` , `else` , `finally` , `for` , `for in` , `if` , `return` , `switch` , `throw` , `try` , `var` , `while` ,
инструкции меток (labels) ( [0.2.8](changes.xml#njs0.2.8) )
- ES6 инструкции: `let` ( [0.6.0](changes.xml#njs0.6.0) ), `const` ( [0.6.0](changes.xml#njs0.6.0) ), `async` ( [0.7.0](changes.xml#njs0.7.0) ), `await` ( [0.7.0](changes.xml#njs0.7.0) )
- Свойства `Math` :
  - ES6: `E` , `LN10` , `LN2` , `LOG10E` , `LOG2E` , `PI` , `SQRT1_2` , `SQRT2`
  
- Методы `Math` :
  - ES6: `abs` , `acos` , `acosh` , `asin` , `asinh` , `atan` , `atan2` , `atanh` , `cbrt` , `ceil` , `clz32` , `cos` , `cosh` , `exp` , `expm1` , `floor` , `fround` , `hypot` , `imul` , `log` , `log10` , `log1p` , `log2` , `max` , `min` , `pow` , `random` , `round` , `sign` , `sin` , `sinh` , `sqrt` , `tan` , `tanh` , `trunc`
  
- Свойства `Number` :
  - ES6: `EPSILON` , `MAX_SAFE_INTEGER` , `MAX_VALUE` , `MIN_SAFE_INTEGER` , `MIN_VALUE` , `NEGATIVE_INFINITY` , `NaN` , `POSITIVE_INFINITY`
  
- Методы `Number` :
  - ES6: `isFinite` , `isInteger` , `isNaN` , `isSafeInteger` , `parseFloat` , `parseInt`
  
- Методы прототипа `Number` :
  - ES6: `toExponential` ( [0.3.6](changes.xml#njs0.3.6) ), `toFixed` ( [0.3.6](changes.xml#njs0.3.6) ), `toPrecision` ( [0.3.6](changes.xml#njs0.3.6) )
  
- Методы `String` :
  - ES5.1: `fromCharCode`
  - ES6: `fromCodePoint`
  
- Методы прототипа `String` :
  - ES5.1: `charAt` , `concat` , `indexOf` , `lastIndexOf` , `match` , `replace` , `search` , `slice` , `split` , `substr` , `substring` , `toLowerCase` , `trim` , `toUpperCase`
  - ES6: `codePointAt` , `endsWith` , `includes` , `repeat` , `startsWith`
  - ES8: `padEnd` , `padStart`
  - ES9: `trimEnd` ( [0.3.4](changes.xml#njs0.3.4) ), `trimStart` ( [0.3.4](changes.xml#njs0.3.4) )
  - ES12: `replaceAll` ( [0.7.10](changes.xml#njs0.7.10) )
  
- Методы `Object` :
  - ES5.1: `create` (поддержка без списка свойств), `defineProperties` (поддержка дескрипторов доступа
начиная с версии [0.3.3](changes.xml#njs0.3.3) ), `defineProperty` (поддержка дескрипторов доступа
начиная с версии [0.3.3](changes.xml#njs0.3.3) ), `freeze` , `getOwnPropertyDescriptor` , `getOwnPropertyDescriptors` ( [0.3.1](changes.xml#njs0.3.1) ), `getOwnPropertyNames` ( [0.3.1](changes.xml#njs0.3.1) ), `getPrototypeOf` , `isExtensible` , `isFrozen` , `isSealed` , `keys` , `preventExtensions` , `seal`
  - ES6: `assign` ( [0.3.7](changes.xml#njs0.3.7) )
  - ES8: `entries` ( [0.2.7](changes.xml#njs0.2.7) ), `values` ( [0.2.7](changes.xml#njs0.2.7) )
  
- Методы прототипа `Object` :
  - ES5.1: `hasOwnProperty` , `isPrototypeOf` ,
( [0.3.0](changes.xml#njs0.3.0) ), `propertyIsEnumerable` , `toString` , `valueOf`
  - ES6: `is` ( [0.3.8](changes.xml#njs0.3.8) ), `setPrototypeOf` ( [0.3.8](changes.xml#njs0.3.8) )
  
- Методы `Array` :
  - ES5.1: `isArray`
  - ES6: `of`
  - ES13: `from` ( [0.8.0](changes.xml#njs0.8.0) ),
  
- Методы прототипа `Array` :
  - ES5.1: `concat` , `every` , `filter` , `forEach` , `indexOf` , `join` , `lastIndexOf` , `map` , `pop` , `push` , `reduce` , `reduceRight` , `reverse` , `shift` , `slice` , `some` , `sort` , `splice` , `unshift`
  - ES6: `copyWithin` ( [0.3.7](changes.xml#njs0.3.7) ), `fill` , `find` , `findIndex`
  - ES7: `includes`
  - ES13: `toReversed` ( [0.8.0](changes.xml#njs0.8.0) ), `toSorted` ( [0.8.0](changes.xml#njs0.8.0) ), `toSpliced` ( [0.8.0](changes.xml#njs0.8.0) )
  
- Методы `ArrayBuffer` ( [0.3.8](changes.xml#njs0.3.8) ):
  - ES6: `isView`
  
- Методы прототипа `ArrayBuffer` ( [0.3.8](changes.xml#njs0.3.8) ):
  - ES6: `slice`
  
- Конструкторы `Typed-array` ( [0.3.8](changes.xml#njs0.3.8) ):
  - ES6: `Int8Array` , `Uint8Array` , `Uint8ClampedArray` , `Int16Array` , `Uint16Array` , `Int32Array` , `Uint32Array` , `Float32Array` , `Float64Array`
  
- Методы прототипа `Typed-array` ( [0.3.8](changes.xml#njs0.3.8) ):
  - ES6: `copyWithin` , `every` ( [0.4.4](changes.xml#njs0.4.4) ), `fill` , `filter` ( [0.4.4](changes.xml#njs0.4.4) ), `find` ( [0.4.4](changes.xml#njs0.4.4) ), `findIndex` ( [0.4.4](changes.xml#njs0.4.4) ), `forEach` ( [0.4.4](changes.xml#njs0.4.4) ), `includes` ( [0.4.4](changes.xml#njs0.4.4) ), `indexOf` ( [0.4.4](changes.xml#njs0.4.4) ), `join` , `lastIndexOf` ( [0.4.4](changes.xml#njs0.4.4) ), `map` ( [0.4.4](changes.xml#njs0.4.4) ), `reduce` ( [0.4.4](changes.xml#njs0.4.4) ), `reduceRight` ( [0.4.4](changes.xml#njs0.4.4) ), `reverse` ( [0.4.4](changes.xml#njs0.4.4) ), `set` , `slice` , `some` ( [0.4.4](changes.xml#njs0.4.4) ), `sort` ( [0.4.2](changes.xml#njs0.4.2) ), `subarray` , `toString`
  - ES13: `toReversed` ( [0.8.0](changes.xml#njs0.8.0) ) `toSorted` ( [0.8.0](changes.xml#njs0.8.0) )
  
- Методы `Buffer` ( [0.4.4](changes.xml#njs0.4.4) ):
  - [`alloc`](reference.xml#buffer_alloc) , [`allocUnsafe`](reference.xml#buffer_alloc_unsafe) , [`byteLength`](reference.xml#buffer_bytelength) , [`compare`](reference.xml#buffer_compare) , [`concat`](reference.xml#buffer_concat) , [`from`](reference.xml#buffer_from_array) , [`isBuffer`](reference.xml#buffer_is_buffer) , [`isEncoding`](reference.xml#buffer_is_encoding)
  
- Методы прототипа `Buffer` :
( [0.4.4](changes.xml#njs0.4.4) ):
  - [`compare`](reference.xml#buf_compare) , [`copy`](reference.xml#buf_copy) , [`equals`](reference.xml#buf_equals) , [`fill`](reference.xml#buf_fill) , [`includes`](reference.xml#buf_includes) , [`indexOf`](reference.xml#buf_indexof) , [`lastIndexOf`](reference.xml#buf_lastindexof) , [`readIntBE`](reference.xml#buf_readintbe) , `readInt8` , `readInt16BE` , `readInt32BE` , [`readIntLE`](reference.xml#buf_readintle) , `readInt8` , `readInt16LE` , `readInt32LE` , [`readUIntBE`](reference.xml#buf_readuintbe) , `readUInt8` , `readUInt16BE` , `readUInt32BE` , [`readUIntLE`](reference.xml#buf_readuintle) , `readUInt8` , `readUInt16LE` , `readUInt32LE` , [`readDoubleBE`](reference.xml#buf_readdobulebe) , [`readDoubleLE`](reference.xml#buf_readdobulele) , [`readFloatBE`](reference.xml#buf_readfloatbe) , [`readFloatLE`](reference.xml#buf_readfloatle) , [`subarray`](reference.xml#buf_subarray) , [`slice`](reference.xml#buf_slice) , [`swap16`](reference.xml#buf_swap16) , [`swap32`](reference.xml#buf_swap32) , [`swap64`](reference.xml#buf_swap64) , [`toJSON`](reference.xml#buf_tojson) , [`toString`](reference.xml#buf_tostring) , [`write`](reference.xml#buf_write) , [`writeIntBE`](reference.xml#buf_writeintbe) , `writeInt8` , `writeInt16BE` , `writeInt32BE` , [`writeIntLE`](reference.xml#buf_writeintle) , `writeInt8` , `writeInt16LE` , `writeInt32LE` , [`writeUIntBE`](reference.xml#buf_writeuintbe) , `writeUInt8` , `writeUInt16BE` , `writeUInt32BE` , [`writeUIntLE`](reference.xml#buf_writeuintle) , `writeUInt8` , `writeUInt16LE` , `writeUInt32LE` , [`writeDoubleBE`](reference.xml#buf_writedoublebe) , [`writeDoubleLE`](reference.xml#buf_writedoublele) , [`writeFloatBE`](reference.xml#buf_writefloatbe) , [`writeFloatLE`](reference.xml#buf_writefloatle)
  
- Методы `Promise` ( [0.3.8](changes.xml#njs0.3.8) ):
  - ES6: `any` ( [0.6.2](changes.xml#njs0.6.2) ), `all` ( [0.6.2](changes.xml#njs0.6.2) ), `allSettled` ( [0.6.2](changes.xml#njs0.6.2) ), `reject` , `resolve` , `race` ( [0.6.2](changes.xml#njs0.6.2) )
  
- Методы прототипа `Promise` ( [0.3.8](changes.xml#njs0.3.8) ):
  - ES6: `catch` , `finally` , `then`
  
- Методы прототипа `Function` :
  - ES5.1: `apply` , `bind` , `call`
  
- Свойства аксессоров прототипа `RegExp` :
  - `flags` ( [0.6.0](changes.xml#njs0.6.0) ), `global` , `ignoreCase` , `multiline` , `source` , `sticky` ( [0.6.0](changes.xml#njs0.6.0) )
  
- Методы прототипа `RegExp` :
  - `[@@replace]` ( [0.4.2](changes.xml#njs0.4.2) ), `[@@split]` ( [0.6.0](changes.xml#njs0.6.0) )
  - ES5.1: `exec` , `test` , `toString`
  
- Свойства экземпляра `RegExp` :
  - `lastIndex`
  
- `RegExp` ES9 именные группы записи ( [0.3.2](changes.xml#njs0.3.2) )
- Методы прототипа `DataView` ( [0.4.4](changes.xml#njs0.4.4) ):
  - ES6: `getFloat32` , `getFloat64` , `getInt16` , `getInt32` , `getInt8` , `getUint16` , `getUint32` , `getUint8` , `setFloat32` , `setFloat64` , `setInt16` , `setInt32` , `setInt8` , `setUint16` , `setUint32` , `setUint8`
  
- Методы `Date` :
  - ES5.1: `now` , `parse` , `UTC`
  
- Методы прототипа `Date` :
  - ES5.1: `getDate` , `getDay` , `getFullYear` , `getHours` , `getMilliseconds` , `getMinutes` , `getMonth` , `getSeconds` , `getTime` , `getTimezoneOffset` , `getUTCDate` , `getUTCDay` , `getUTCFullYear` , `getUTCHours` , `getUTCMilliseconds` , `getUTCMinutes` , `getUTCMonth` , `getUTCSeconds` , `toDateString` , `toISOString` , `toLocaleDateString` , `toLocaleString` , `toLocaleTimeString` , `toTimeString` , `toUTCString` , `setDate` , `setFullYear` , `setHours` , `setMinutes` , `setMilliseconds` , `setMonth` , `setSeconds` , `setTime` , `setUTCDate` , `setUTCFullYear` , `setUTCHours` , `setUTCMilliseconds` , `setUTCMinutes` , `setUTCMonth` , `setUTCSeconds`
  
- Методы `JSON` :
  - ES5.1: `parse` , `stringify`
  
- Методы `Symbol` ( [0.7.6](changes.xml#njs0.7.6) ):
  - `for` , `keyfor`
  
- ES5.1 объект `arguments` ( [0.2.5](changes.xml#njs0.2.5) )
- ES6 синтаксис rest параметров (без поддержки деструктуризации)
( [0.2.7](changes.xml#njs0.2.7) )
- ES5.1 global functions: `decodeURI` , `decodeURIComponent` , `encodeURI` , `encodeURIComponent` , `isFinite` , `isNaN` , `parseFloat` , `parseInt`
- Global functions ( [0.7.6](changes.xml#njs0.7.6) ): [`atob`](reference.xml#atob) , [`btoa`](reference.xml#btoa)
- Объекты `Error` : `Error` , `EvalError` , `InternalError` , `RangeError` , `ReferenceError` , `SyntaxError` , `TypeError` , `URIError`
- Функции [`clearTimeout`](reference.xml#cleartimeout) и [`setTimeout`](reference.xml#settimeout) ( [0.2.0](changes.xml#njs0.2.0) )
- Методы `File system` : [`fs.accessSync`](reference.xml#fs_accesssync) ( [0.3.9](changes.xml#njs0.3.9) ), [`fs.appendFileSync`](reference.xml#appendfilesync) , [`fs.closeSync`](reference.xml#fs_closesync) , [`fs.existsSync`](reference.xml#fs_existssync) ( [0.8.2](changes.xml#njs0.8.2) ), [`fs.FileHandle`](reference.xml#fs_filehandle) ( [0.7.7](changes.xml#njs0.7.7) ), [`fs.fstatSync`](reference.xml#fs_fstatsync) ( [0.7.7](changes.xml#njs0.7.7) ), [`fs.lstatSync`](reference.xml#fs_lstatsync) ( [0.7.1](changes.xml#njs0.7.7) ), [`fs.mkdirSync`](reference.xml#fs_mkdirsync) ( [0.4.2](changes.xml#njs0.4.2) ), [`fs.openSync`](reference.xml#fs_opensync) ( [0.7.7](changes.xml#njs0.7.7) ), [`fs.promises.open`](reference.xml#fs_promises_open) ( [0.7.7](changes.xml#njs0.7.7) ), [`fs.readdirSync`](reference.xml#fs_readdirsync) ( [0.4.2](changes.xml#njs0.4.2) ), [`fs.readFileSync`](reference.xml#readfilesync) , [`fs.readSync`](reference.xml#fs_readsync) ( [0.7.7](changes.xml#njs0.7.7) ), [`fs.realpathSync`](reference.xml#fs_realpathsync) ( [0.3.9](changes.xml#njs0.3.9) ), [`fs.renameSync`](reference.xml#fs_renamesync) ( [0.3.4](changes.xml#njs0.3.4) ), [`fs.rmdirSync`](reference.xml#fs_rmdirsync) ( [0.4.2](changes.xml#njs0.4.2) ), [`fs.symlinkSync`](reference.xml#fs_symlinksync) ( [0.3.9](changes.xml#njs0.3.9) ), [`fs.unlinkSync`](reference.xml#fs_unlinksync) ( [0.3.9](changes.xml#njs0.3.9) ), [`fs.writeFileSync`](reference.xml#fs_writefilesync) [`fs.writeSync`](reference.xml#fs_writesync_buf) ( [0.7.7](changes.xml#njs0.7.7) )
- `fs.promises` API ( [0.3.9](changes.xml#njs0.3.9) ),
асинхронная версия файловых методов file system.
- Методы `Crypto` ( [0.2.0](changes.xml#njs0.2.0) ): [`crypto.createHash`](reference.xml#crypto_createhash) , [`crypto.createHmac`](reference.xml#crypto_createhmac)
- Методы [`Query String`](reference.xml#querystring) ( [0.4.3](changes.xml#njs0.4.3) ): [`querystring.decode`](reference.xml#querystring_decode) , [`querystring.encode`](reference.xml#querystring_encode) , [`querystring.escape`](reference.xml#querystring_escape) , [`querystring.parse`](reference.xml#querystring_parse) , [`querystring.stringify`](reference.xml#querystring_stringify) , [`querystring.unescape`](reference.xml#querystring_unescape)
- Методы [`TextDecoder`](reference.xml#textdecoder) ( [0.4.3](changes.xml#njs0.4.3) ): [`encoding`](reference.xml#textdecoder_encoding) , [`fatal`](reference.xml#textdecoder_fatal) , [`ignoreBOM`](reference.xml#textdecoder_ignorebom) , [`decode`](reference.xml#textdecoder_ignorebom)
- Методы [`TextEncoder`](reference.xml#textencoder) ( [0.4.3](changes.xml#njs0.4.3) ): [`encode`](reference.xml#textencoder_encode) , [`encodeInto`](reference.xml#textencoder_encodeinto)
- Методы [`XML`](reference.xml#xml) ( [0.7.10](changes.xml#njs0.7.10) ): [`parse`](reference.xml#xml_parse) , [`xml.c14n`](reference.xml#xml_c14n) , [`xml.exclusiveC14n`](reference.xml#xml_exclusiveC14n)
- Методы [`zlib`](reference.xml#zlib) ( [0.7.12](changes.xml#njs0.7.12) ): [`deflateRawSync`](reference.xml#zlib_deflaterawsync) , [`deflateSync`](reference.xml#zlib_deflatesync) , [`inflateRawSync`](reference.xml#zlib_inflaterawsync) [`inflateSync`](reference.xml#zlib_inflatesync)
- ES6 поддержка модулей:
инструкции `export` по умолчанию и `import` по умолчанию
( [0.3.0](changes.xml#njs0.3.0) )
- ES6 поддержка стрелочных функций
( [0.3.1](changes.xml#njs0.3.1) )
- Шаблонные строки:
многострочные литералы, интерполяция выражений, вложенные шаблоны
( [0.3.2](changes.xml#njs0.3.2) )
- Глобальные объекты
( [0.3.3](changes.xml#njs0.3.3) ):
  - [`console`](reference.xml#console) ( [0.8.2](changes.xml#njs0.8.2) ): [`error`](reference.xml#console_error) , [`info`](reference.xml#console_info) , [`log`](reference.xml#console_log) , [`time`](reference.xml#console_time) , [`timeEnd`](reference.xml#console_time_end) , [`warn`](reference.xml#console_warn)
  - [`crypto`](reference.xml#builtin_crypto) ( [0.7.0](changes.xml#njs0.7.0) ): [`getRandomValues`](reference.xml#crypto_get_random_values) , [`subtle.encrypt`](reference.xml#crypto_subtle_encrypt) , [`subtle.decrypt`](reference.xml#crypto_subtle_decrypt) , [`subtle.deriveBits`](reference.xml#crypto_subtle_derive_bits) , [`subtle.deriveKey`](reference.xml#crypto_subtle_derive_key) , [`subtle.digest`](reference.xml#crypto_subtle_digest) [`subtle.exportKey`](reference.xml#crypto_subtle_export_key) ( [0.7.10](changes.xml#njs0.7.10) ), [`subtle.generateKey`](reference.xml#crypto_subtle_generate_key) ( [0.7.10](changes.xml#njs0.7.10) ), [`subtle.importKey`](reference.xml#crypto_subtle_import_key) , [`subtle.sign`](reference.xml#crypto_subtle_sign) , [`subtle.verify`](reference.xml#crypto_subtle_verify)
  - псевдоним `globalThis` ( [0.3.8](changes.xml#njs0.3.8) ),
  - [`njs`](reference.xml#njs) : [`version`](reference.xml#njs_version) , [`version_number`](reference.xml#njs_version_number) ( [0.7.4](changes.xml#njs0.7.4) ), [`dump`](reference.xml#njs_dump) , [`memoryStats`](reference.xml#njs_memory_stats) ( [0.7.8](changes.xml#njs0.7.8) ), [`on`](reference.xml#njs_on) ( [0.5.2](changes.xml#njs0.5.2) )
  - [`process`](reference.xml#process) : [`argv`](reference.xml#process_argv) , [`env`](reference.xml#process_env) , [`pid`](reference.xml#process_pid) , [`ppid`](reference.xml#process_ppid)
  
- Методы объекта nginx:
  - [`HTTP Request`](reference.xml#http) : [`r.done`](reference.xml#r_done) ( [0.5.2](changes.xml#njs0.5.2) ), [`r.error`](reference.xml#r_error) , [`r.finish`](reference.xml#r_finish) , [`r.internalRedirect`](reference.xml#r_internal_redirect) , [`r.log`](reference.xml#r_log) , [`r.return`](reference.xml#r_return) ( [0.5.0](changes.xml#njs0.5.0) ), [`r.send`](reference.xml#r_send) ( [0.5.0](changes.xml#njs0.5.0) ), [`r.sendBuffer`](reference.xml#r_sendbuffer) ( [0.5.2](changes.xml#njs0.5.2) ), [`r.sendHeader`](reference.xml#r_send_header) , [`r.setReturnValue`](reference.xml#r_set_return_value) ( [0.7.0](changes.xml#njs0.7.0) ), [`r.subrequest`](reference.xml#r_subrequest) , [`r.warn`](reference.xml#r_warn)
  - [`Stream Session`](reference.xml#stream) : [`s.allow`](reference.xml#s_allow) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.decline`](reference.xml#s_decline) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.deny`](reference.xml#s_deny) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.done`](reference.xml#s_done) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.error`](reference.xml#s_error) , [`s.log`](reference.xml#s_log) , [`s.off`](reference.xml#s_off) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.on`](reference.xml#s_on) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.send`](reference.xml#s_send) ( [0.2.4](changes.xml#njs0.2.4) ), [`s.sendDownstream`](reference.xml#s_send_downstream) ( [0.7.8](changes.xml#njs0.7.8) ), [`s.sendUpstream`](reference.xml#s_send_upstream) ( [0.7.8](changes.xml#njs0.7.8) ), [`s.setReturnValue`](reference.xml#s_set_return_value) ( [0.7.0](changes.xml#njs0.7.0) ), [`s.warn`](reference.xml#s_warn)
  - [`Headers`](reference.xml#headers) ( [0.5.1](changes.xml#njs0.5.1) ): [`append`](reference.xml#headers_append) , [`delete`](reference.xml#headers_delete) , [`get`](reference.xml#headers_get) , [`getAll`](reference.xml#headers_getall) , [`forEach`](reference.xml#headers_foreach) , [`has`](reference.xml#headers_has) , [`set`](reference.xml#headers_set)
  - [`Request`](reference.xml#request) ( [0.7.10](changes.xml#njs0.7.10) ): [`arrayBuffer`](reference.xml#request_arraybuffer) , [`headers`](reference.xml#request_headers) , [`json`](reference.xml#request_json) , [`text`](reference.xml#request_text)
  - [`Response`](reference.xml#response) ( [0.5.1](changes.xml#njs0.5.1) ): [`arrayBuffer`](reference.xml#response_arraybuffer) , [`headers`](reference.xml#response_headers) , [`json`](reference.xml#response_json) , [`text`](reference.xml#response_text)
  - [`ngx`](reference.xml#ngx) ( [0.5.0](changes.xml#njs0.5.0) ): [`fetch`](reference.xml#ngx_fetch) ( [0.5.1](changes.xml#njs0.5.1) ), [`log`](reference.xml#ngx_log)
  - [`ngx.shared`](reference.xml#ngx_shared) ( [0.8.0](changes.xml#njs0.8.0) ): [`add`](reference.xml#dict_add) , [`clear`](reference.xml#dict_clear) , [`delete`](reference.xml#dict_delete) , [`freeSpace`](reference.xml#dict_freespace) , [`get`](reference.xml#dict_get) , [`has`](reference.xml#dict_has) , [`incr`](reference.xml#dict_incr) , [`items`](reference.xml#dict_items) , [`keys`](reference.xml#dict_keys) , [`pop`](reference.xml#dict_pop) , [`replace`](reference.xml#dict_replace) , [`set`](reference.xml#dict_set) , [`size`](reference.xml#dict_size)
  
- Свойства объекта nginx:
  - [`HTTP Request`](reference.xml#http) : [`r.args`](reference.xml#r_args) , [`r.headersIn`](reference.xml#r_headers_in) , [`r.headersOut`](reference.xml#r_headers_out) , [`r.httpVersion`](reference.xml#r_http_version) , [`r.internal`](reference.xml#r_internal) , [`r.method`](reference.xml#r_method) , [`r.parent`](reference.xml#r_parent) , [`r.rawHeadersIn`](reference.xml#r_raw_headers_in) ( [0.4.1](changes.xml#njs0.4.1) ), [`r.rawHeadersOut`](reference.xml#r_raw_headers_out) ( [0.4.1](changes.xml#njs0.4.1) ), [`r.rawVariables`](reference.xml#r_raw_variables) ( [0.5.0](changes.xml#njs0.5.0) ), [`r.remoteAddress`](reference.xml#r_remote_address) , [`r.requestBuffer`](reference.xml#r_request_buffer) ( [0.5.0](changes.xml#njs0.5.0) ), [`r.requestText`](reference.xml#r_request_text) , [`r.responseBuffer`](reference.xml#r_response_buffer) ( [0.5.0](changes.xml#njs0.5.0) ), [`r.responseText`](reference.xml#r_response_text) ( [0.5.0](changes.xml#njs0.5.0) ), [`r.status`](reference.xml#r_status) , [`r.uri`](reference.xml#r_uri) , [`r.variables`](reference.xml#r_variables) ( [0.2.8](changes.xml#njs0.2.8) )
  - [`Stream Session`](reference.xml#stream) : [`s.remoteAddress`](reference.xml#s_remote_address) , [`s.rawVariables`](reference.xml#s_raw_variables) ( [0.5.0](changes.xml#njs0.5.0) ), [`s.status`](reference.xml#s_status) ( [0.5.2](changes.xml#njs0.5.2) ), [`s.variables`](reference.xml#s_variables) ( [0.2.8](changes.xml#njs0.2.8) )
  - [`Periodic Session`](reference.xml#periodic_session) ( [0.8.1](changes.xml#njs0.8.1) ): [`PeriodicSession.rawVariables`](reference.xml#periodic_session_raw_variables) , [`PeriodicSession.variables`](reference.xml#periodic_session_variables)
  - [`Request`](reference.xml#request) ( [0.7.10](changes.xml#njs0.7.10) ): [`bodyUsed`](reference.xml#request_bodyused) , [`cache`](reference.xml#request_cache) , [`credentials`](reference.xml#request_credentials) , [`method`](reference.xml#request_method) , [`mode`](reference.xml#request_mode) , [`url`](reference.xml#request_url)
  - [`Response`](reference.xml#response) ( [0.5.1](changes.xml#njs0.5.1) ): [`bodyUsed`](reference.xml#response_bodyused) , [`ok`](reference.xml#response_ok) , [`redirected`](reference.xml#response_redirect) , [`status`](reference.xml#response_status) , [`statusText`](reference.xml#response_statustext) , [`type`](reference.xml#response_type) , [`url`](reference.xml#response_url)
  - [`ngx`](reference.xml#ngx) ( [0.5.0](changes.xml#njs0.5.0) ): [`build`](reference.xml#ngx_build) ( [0.8.0](changes.xml#njs0.8.0) ), [`conf_file_path`](reference.xml#ngx_conf_file_path) ( [0.8.0](changes.xml#njs0.8.0) ), [`conf_prefix`](reference.xml#ngx_conf_prefix) ( [0.7.8](changes.xml#njs0.7.8) ), [`error_log_path`](reference.xml#ngx_error_log_path) ( [0.8.0](changes.xml#njs0.8.0) ), [`prefix`](reference.xml#ngx_prefix) ( [0.8.0](changes.xml#njs0.8.0) ), [`version`](reference.xml#ngx_version) ( [0.8.0](changes.xml#njs0.8.0) ), [`version_number`](reference.xml#ngx_version_number) ( [0.8.0](changes.xml#njs0.8.0) ), [`worker_id`](reference.xml#ngx_worker_id) ( [0.8.0](changes.xml#njs0.8.0) )
  - [`ngx.shared`](reference.xml#ngx_shared) ( [0.8.0](changes.xml#njs0.8.0) ): [`capacity`](reference.xml#dict_capacity) , [`name`](reference.xml#dict_name) , [`type`](reference.xml#dict_name)
  

