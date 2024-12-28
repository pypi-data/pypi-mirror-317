import os
import sysconfig
from typing import Optional

__all__ = [
    "get_libpython",
    "get_jcpy_path",
    "get_jcpy_loader",
    "get_jcpy_engine",
]


def get_jcpy_loader() -> str:
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, "libs", "jcpy_loader.so")


def get_jcpy_path() -> str:
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, "jcpy")


def get_jcpy_engine() -> str:
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, "libs", "jcpy_engine.so")


def get_libpython() -> Optional[str]:
    lib_dir = sysconfig.get_config_var("LIBDIR")
    ld_lib = sysconfig.get_config_var("LDLIBRARY")
    multi_arch = sysconfig.get_config_var("MULTIARCH")

    if not (lib_dir and ld_lib):
        return None

    potential_paths = [os.path.join(lib_dir, ld_lib)]
    if multi_arch:
        potential_paths.append(os.path.join(lib_dir, multi_arch, ld_lib))

    if ld_lib.endswith(".a"):
        ld_share = ld_lib[:-1] + "so"
        potential_paths.extend(
            [
                os.path.join(lib_dir, ld_share),
                os.path.join(lib_dir, multi_arch, ld_share) if multi_arch else None,
            ]
        )

    for path in potential_paths:
        if path is not None and os.path.exists(path):
            return os.path.realpath(path)

    return None
