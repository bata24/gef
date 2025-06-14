// d8 --allow-natives-syntax test.js

// ---- basic objects ----
let obj = { a: 1, b: 2 };
let arr = [1, 2, 3];
let str = "hello";
let num = 42;
let bool = true;
let date = new Date();
let map = new Map([[1, 'one'], [2, 'two']]);
let set = new Set([1, 2, 3]);

// other
let weakMap = new WeakMap();
let weakSet = new WeakSet();
let tempObj = {};
weakMap.set(tempObj, 'value');
weakSet.add(tempObj);

let promise = Promise.resolve(123);
let symbol = Symbol("mysymbol");
let bigInt = 1234567890123456789012345678901234567890n;

// ---- buffer ----
let buffer = new ArrayBuffer(0x1000);
let view = new DataView(buffer);
let typedArray = new Uint8Array(buffer);

// ---- functions ----
function normalFunc(x) { return x + 1; }
let arrowFunc = (x) => x * 2;
let closureFunc = (function(y) {
  return function(x) { return x + y; };
})(10);
class MyClass {
  constructor(value) { this.value = value; }
  method() { return this.value; }
}
let classInstance = new MyClass(123);

// ---- Wasm Module ----
let wasmCode = new Uint8Array([
  0x00,0x61,0x73,0x6D, // magic "\0asm"
  0x01,0x00,0x00,0x00, // version 1
  // minimal empty wasm module
]);
let wasmModule = new WebAssembly.Module(wasmCode);
let wasmInstance = new WebAssembly.Instance(wasmModule);

// ---- Proxy ----
let target = { foo: "bar" };
let handler = {
  get: function(obj, prop) {
    return prop in obj ? obj[prop] : "default";
  }
};
let proxy = new Proxy(target, handler);

// ---- Generator ----
function* genFunc() {
  yield 1;
  yield 2;
  return 3;
}
let generator = genFunc();

// ---- AsyncFunction ----
async function asyncFunc() {
  return 42;
}

// ---- AsyncGenerator ----
async function* asyncGenFunc() {
  yield 1;
  yield 2;
}
let asyncGenerator = asyncGenFunc();

// ---- Reflect ----
let reflectObj = Reflect;

// ---- Intl ----
let intlCollator = new Intl.Collator();
let intlNumberFormat = new Intl.NumberFormat();
let intlDateTimeFormat = new Intl.DateTimeFormat();

// ---- SharedArrayBuffer ----
let sharedArrayBuffer = new SharedArrayBuffer(1024);

// ---- Atomics ----
let sharedInt32Array = new Int32Array(sharedArrayBuffer);
Atomics.store(sharedInt32Array, 0, 42);

// ---- Error ----
let error = new Error("test error");
let typeError = new TypeError("test type error");

// ---- RegExp ----
let re = /abc/;

// ---- FinalizationRegistry / WeakRef ----
let registry = new FinalizationRegistry(() => {});
let weakRef = new WeakRef({});

// ---------------------------------------------------

// ---- dump ----
function debug(name, obj) {
  print(`=== ${name} ===`);
  %DebugPrint(obj);
}

debug("Object", obj);
debug("Array", arr);
debug("String", str);
debug("Number", num);
debug("Boolean", bool);
debug("Date", date);
debug("Map", map);
debug("Set", set);
debug("WeakMap", weakMap);
debug("WeakSet", weakSet);
debug("Promise", promise);
debug("Symbol", symbol);
debug("BigInt", bigInt);

debug("ArrayBuffer", buffer);
debug("DataView", view);
debug("TypedArray", typedArray);

debug("Normal Function", normalFunc);
debug("Arrow Function", arrowFunc);
debug("Closure Function", closureFunc);
debug("Class", MyClass);
debug("Class Instance", classInstance);

debug("Wasm Module", wasmModule);
debug("Wasm Instance", wasmInstance);

debug("Proxy", proxy);
debug("Generator", generator);
debug("AsyncFunction", asyncFunc);

debug("AsyncGenerator", asyncGenerator);
debug("Reflect", reflectObj);
debug("Intl.Collator", intlCollator);
debug("Intl.NumberFormat", intlNumberFormat);
debug("Intl.DateTimeFormat", intlDateTimeFormat);

debug("SharedArrayBuffer", sharedArrayBuffer);
debug("Shared Int32Array (Atomics target)", sharedInt32Array);

debug("Error", error);
debug("TypeError", typeError);

debug("RegExp", re);

debug("FinalizationRegistry", registry);
debug("WeakRef", weakRef);

debug("Math", Math);
debug("JSON", JSON);

while (1) {}
