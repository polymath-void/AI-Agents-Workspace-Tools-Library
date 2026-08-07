# `wc-kernel-builder`

## Overview
`wc-kernel-builder` is an automated toolchain and build manager for Android GKI Linux Kernels. It audits compiler environments (Clang, LLVM, GNU cross-tools), verifies defconfig options (KPROBES, BPF, GKI compliance), validates binary ARM64 Image headers, and compiles flashable AnyKernel3 zip archives.

## Category & Classification
- **Category**: `04_system_runtime` (Android & Termux System)
- **Runtime**: Pure Python 3 & ZipFile Packager
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-kernel-builder <check-env|audit-config|verify-image|anykernel-pack> [args]
```

### Subcommands
- `check-env`: Audits host system for LLVM/Clang toolchain and cross-compilation prerequisites.
- `audit-config <defconfig_path>`: Scans defconfig against GKI requirements.
- `verify-image <Image_path>`: Inspects ARM64 kernel Image magic header (`0x644d5241`) and entry points.
- `anykernel-pack <Image_path> [-o output.zip] [-d device_name]`: Generates a recovery-flashable AnyKernel3 zip package.

## Associated Skills
- `android-kernel-build`
- `termux-environment`

## Example Agent Invocation
```bash
wc-kernel-builder anykernel-pack out/arch/arm64/boot/Image -o Custom-GKI-Kernel.zip -d "Pixel 7"
```
