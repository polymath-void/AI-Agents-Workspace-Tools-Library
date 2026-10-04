from wasmtime import Engine, Store, Module
import sys

engine = Engine()
module = Module.from_file(engine, "/data/data/com.termux/files/home/Projects/python_agent/agent_core.wasm")
for export in module.exports:
    print(export.name, export.type)
