import os
import sys
import struct
from pathlib import Path
from typing import Dict, Any, List, Optional

PAGE_SIZE_16KB = 16384  # 0x4000
PAGE_SIZE_4KB = 4096    # 0x1000

ELF_MAGIC = b"\x7fELF"
PT_LOAD = 1

class ELFAlignAnalyzer:
    """Android 15 & 16 (API 36) 16KB memory page-alignment ELF binary analyzer & validator."""

    @classmethod
    def inspect_binary(cls, file_path: Path) -> Dict[str, Any]:
        """Parses ELF binary program headers and inspects PT_LOAD segment alignment."""
        if not file_path.exists() or not file_path.is_file():
            return {"status": "ERROR", "message": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                header = f.read(64)
                if len(header) < 52 or not header.startswith(ELF_MAGIC):
                    return {"status": "SKIPPED", "reason": "Not a valid ELF binary", "path": str(file_path)}

                ei_class = header[4]  # 1 = 32-bit, 2 = 64-bit
                is_64 = ei_class == 2

                ei_data = header[5]   # 1 = Little Endian, 2 = Big Endian
                endian = "<" if ei_data == 1 else ">"

                if is_64:
                    e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack(
                        f"{endian}HHIQQQIHHHHHH", header[16:64]
                    )
                else:
                    e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack(
                        f"{endian}HHIIIIIHHHHHH", header[16:52]
                    )


                if e_phoff == 0 or e_phnum == 0:
                    return {"status": "WARN", "message": "No program headers found", "path": str(file_path)}

                f.seek(e_phoff)
                pt_load_segments = []
                max_align = 0
                is_16kb_aligned = True

                for i in range(e_phnum):
                    ph_data = f.read(e_phentsize)
                    if len(ph_data) < e_phentsize:
                        break

                    if is_64:
                        p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack(
                            f"{endian}IIQQQQQQ", ph_data[:56]
                        )
                    else:
                        p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = struct.unpack(
                            f"{endian}IIIIIIII", ph_data[:32]
                        )

                    if p_type == PT_LOAD:
                        max_align = max(max_align, p_align)
                        aligned_16k = (p_align >= PAGE_SIZE_16KB)
                        if not aligned_16k:
                            is_16kb_aligned = False

                        pt_load_segments.append({
                            "segment_index": i,
                            "offset": hex(p_offset),
                            "vaddr": hex(p_vaddr),
                            "filesz": p_filesz,
                            "memsz": p_memsz,
                            "p_align": p_align,
                            "p_align_hex": hex(p_align),
                            "is_16kb_aligned": aligned_16k
                        })

                machine_map = {
                    183: "AArch64 (arm64-v8a)",
                    40: "ARM (armeabi-v7a)",
                    62: "x86_64",
                    3: "x86",
                    243: "RISC-V 64"
                }
                arch_name = machine_map.get(e_machine, f"Unknown ({e_machine})")

                return {
                    "status": "SUCCESS",
                    "path": str(file_path),
                    "file_size_bytes": file_path.stat().st_size,
                    "architecture": arch_name,
                    "is_64_bit": is_64,
                    "pt_load_count": len(pt_load_segments),
                    "max_page_align": max_align,
                    "max_page_align_hex": hex(max_align),
                    "is_16kb_aligned": is_16kb_aligned,
                    "android_16_ready": is_16kb_aligned or not is_64,
                    "pt_load_segments": pt_load_segments
                }

        except Exception as e:
            return {"status": "ERROR", "message": str(e), "path": str(file_path)}

    @classmethod
    def scan_directory(cls, dir_path: Path) -> Dict[str, Any]:
        """Recursively checks all .so and ELF shared objects inside a folder or APK extract."""
        if not dir_path.exists():
            return {"status": "ERROR", "message": f"Directory not found: {dir_path}"}

        binaries = []
        compliant_count = 0
        non_compliant_count = 0

        for p in dir_path.rglob("*"):
            if p.is_file() and (p.suffix == ".so" or not p.suffix):
                res = cls.inspect_binary(p)
                if res.get("status") == "SUCCESS":
                    binaries.append(res)
                    if res.get("is_16kb_aligned"):
                        compliant_count += 1
                    else:
                        non_compliant_count += 1

        return {
            "scanned_directory": str(dir_path),
            "total_elf_binaries": len(binaries),
            "compliant_16kb_count": compliant_count,
            "non_compliant_count": non_compliant_count,
            "all_compliant": non_compliant_count == 0,
            "binaries": binaries
        }

    @staticmethod
    def get_linker_flag_recommendation() -> Dict[str, str]:
        return {
            "cmake": 'set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-z,max-page-size=16384")',
            "ndk_build": "LOCAL_LDFLAGS += -Wl,-z,max-page-size=16384",
            "gradle_cmake": 'externalNativeBuild.cmake.cFlags "-Wl,-z,max-page-size=16384"',
            "rust_cargo": 'rustflags = ["-C", "link-arg=-Wl,-z,max-page-size=16384"]'
        }
