from typing import Mapping, Optional, Sequence

__all__ = [
    "full_version",
    "compiler_version",
    "compiler_git_short_hash",
    "compile",
    "CompiledGraph",
]

__version__: str = ...
__full_version__: str = ...
__git_short_hash__: str = ...
__build_timestamp__: str = ...

class CompiledGraph:
    def is_edf(self) -> bool: ...
    def serialize(self) -> bytes: ...
    @staticmethod
    def deserialize(b: bytes, tag: str) -> "CompiledGraph": ...

def full_version() -> str: ...
def compiler_version() -> str: ...
def compiler_git_short_hash() -> str: ...
def compile(
    model,
    input_args: Sequence,
    target_npu: str = "renegade",
    *,
    input_kwargs: Optional[Mapping] = None,
    target_ir: str = "edf",
    config: Optional[Mapping] = None,
    verbose: bool = False,
    enable_cache: bool = True,
    ignore_compile_error=False,
    skip_trace=False,
    skip_preprocess=False,
    print_fx_graph=False,
    only_cpu_tasks=False,
    experimental_lower_only_einsum_by_dpe=None,
    dump_tag: Optional[str] = None,
    dump_path: Optional[str] = None,
    dump_lir: bool = True,
    **kwargs,
) -> CompiledGraph: ...
def compile_from_path(
    model_path: str,
    target_npu: str = "renegade",
    target_ir: str = "edf",
    *,
    config: Optional[Mapping] = None,
    verbose: bool = False,
    enable_cache: bool = True,
    only_cpu_tasks=False,
    experimental_lower_only_einsum_by_dpe=None,
    dump_tag: Optional[str] = None,
    dump_path: Optional[str] = None,
    dump_lir: bool = True,
) -> CompiledGraph: ...
def check_furiosa_ir(model, ir_kind: str) -> bool: ...
