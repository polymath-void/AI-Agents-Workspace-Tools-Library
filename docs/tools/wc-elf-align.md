# `wc-elf-align`

## Overview
`wc-elf-align` is an Android 15 & Android 16 (API 36) 16KB memory page-alignment ELF binary validator. It directly parses 32-bit and 64-bit ELF program headers (`PT_LOAD` segments), verifies that `p_align >= 0x4000` (16384 bytes), detects legacy 4KB unaligned `.so` libraries, and provides exact compiler and linker flag solutions for CMake, NDK, and Gradle.

## Category & Classification
- **Category**: `04_system_runtime` (Android & Termux System)
- **Runtime**: Pure Python 3 & Struct Binary Unpacker
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-elf-align <inspect|flags> [target]
```

### Subcommands
- `inspect <binary_or_dir>`: Inspects ELF headers and checks PT_LOAD alignments. Returns JSON with architecture, alignment, and compatibility verdict.
- `flags`: Displays recommended linker flags for CMake (`-Wl,-z,max-page-size=16384`), NDK build, Gradle, and Rust Cargo.

## Associated Skills
- `piuu-c-native-core`
- `termux-environment`
- `android-kernel-build`

## Example Agent Invocation
```bash
wc-elf-align inspect ~/repo/Piuu-Unified-Launcher-Android/app/src/main/jniLibs/arm64-v8a/libpiuu_core.so
```
