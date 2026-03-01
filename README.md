# Simple Python Bytecode Interpreter

This repository contains a minimal Python bytecode interpreter implemented in pure Python.  It can load and execute compiled `.pyc` files by interpreting Python's bytecode opcodes.

## Overview

The interpreter consists of a few core classes:

- `VirtualMachine` – drives execution, maintains a stack of `Frame` objects, and dispatches bytecode instructions.
- `Frame` – represents an execution frame holding local/global namespaces, the evaluation stack, and block stack for loops/exception handling.
- `Function` – wraps a code object so that user-defined functions can be called within the VM.

Opcode handlers are defined as methods on `VirtualMachine` with the prefix `byte_` (e.g. `byte_LOAD_CONST`).  The VM supports many of the standard bytecode operations including name lookups, arithmetic, jumps, loops, and function calls.  A simple block-stack mechanism handles `break`, `continue`, `try/except`, and `finally` behaviour.

### How it was made

This interpreter was built as an educational proof of concept.  It follows the structure of the official CPython interpreter but in a much-simplified manner:

1. **Parsing** – bytes are read from a code object's `co_code` property and converted into opcode names and arguments using Python's `dis` module to map numeric opcodes to names.
2. **Dispatch loop** – a tight loop in `VirtualMachine.run_frame` fetches the next instruction, dispatches it to the corresponding handler method, and manages control-flow changes and exceptions.
3. **Stack manipulation** – most operations push and pop values on a stack held per frame, imitating CPython's evaluation stack.
4. **Frames and calls** – each call creates a new `Frame`; returning or raising unwinds the frame stack.
5. **Function objects** – a lightweight `Function` class wraps a Python code object so that calling it pushes another frame.

The code uses the built‑in `marshal` module to read a compiled `.pyc` file when run as a script.  The VM is then instantiated and `run_code()` is invoked with the loaded code object.

## Usage

1. Compile a Python source file to bytecode (e.g. with `python -m py_compile myscript.py`).
2. Copy the resulting `.pyc` (usually in `__pycache__`) to the interpreter's directory or update the path in the `__main__` section of `Bytecode.py`.
3. Run the interpreter:
   ```sh
   python Bytecode.py
   ```
   This will load `testcode.pyc` by default and execute it inside the custom virtual machine.

You can also import the `VirtualMachine` class from other code and use `run_code(code_object)` directly.

Example:

```python
from Bytecode import VirtualMachine
import compileall, marshal

# compile a simple script and run it
compileall.compile_file('hello.py', force=True)
with open('__pycache__/hello.cpython-3xx.pyc','rb') as f:
    f.read(8)            # skip header
    code = marshal.load(f)

vm = VirtualMachine()
vm.run_code(code)
```

> ⚠️ **Limitations:**
> - No support for keyword arguments or varargs in function calls.
> - Only a subset of bytecodes are implemented.
> - Not suitable for running untrusted code; it is mainly a learning tool.

## Extending

To add support for additional opcodes, simply implement a new `byte_<OPNAME>` method on `VirtualMachine`, following the pattern used in the existing methods.  Consult the [`dis` module documentation](https://docs.python.org/3/library/dis.html) for opcode semantics.

Block handling and exception propagation can be enhanced by modifying `manage_block_stack` and related helper methods.

Contributions or experiments are welcome!
