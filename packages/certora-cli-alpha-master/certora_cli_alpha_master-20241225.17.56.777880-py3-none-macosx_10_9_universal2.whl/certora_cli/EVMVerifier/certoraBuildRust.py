import glob
import shutil
from pathlib import Path
from typing import Set

from EVMVerifier.certoraBuild import build_source_tree
from EVMVerifier.certoraContextClass import CertoraContext
from EVMVerifier.certoraParseBuildScript import run_script_and_parse_json
from Shared import certoraUtils as Util


def build_rust_app(context: CertoraContext) -> None:
    if context.build_script:
        run_script_and_parse_json(context)
        if not context.rust_executables:
            raise Util.CertoraUserInputError("failed to get target executable")

        sources: Set[Path] = set()
        root_directory = Path(context.rust_project_directory)
        collect_files_from_rust_sources(context, sources, root_directory)

        try:
            # Create generators
            build_source_tree(sources, context)

            copy_files_to_build_dir(context, root_directory)

        except Exception as e:
            raise Util.CertoraUserInputError(f"Collecting build files failed with the exception: {e}")
    else:
        if not context.files:
            raise Util.CertoraUserInputError("'files' or 'build_script' must be set for Rust projects")
        if len(context.files) > 1:
            raise Util.CertoraUserInputError("Rust projects must specify exactly one executable in 'files'.")
        context.rust_executables = context.files[0]


def collect_files_from_rust_sources(context: CertoraContext, sources: Set[Path], root_directory: Path) -> None:
    patterns = ["*.rs", "*.so", "*.wasm", "Cargo.toml", "Cargo.lock", "justfile"]
    exclude_dirs = [".certora_internal"]

    if not root_directory.is_dir():
        raise ValueError(f"The given directory {root_directory} is not valid.")

    for source in context.rust_sources:
        for file in glob.glob(f'{root_directory.joinpath(source)}', recursive=True):
            file_path = Path(file)
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
            if file_path.is_file() and any(file_path.match(pattern) for pattern in patterns):
                sources.add(file_path)

    if Path(context.build_script).exists():
        sources.add(Path(context.build_script).resolve())
    if context.conf_file and Path(context.conf_file).exists():
        sources.add(Path(context.conf_file).absolute())


def copy_files_to_build_dir(context: CertoraContext, root_directory: Path) -> None:
    rust_executable = root_directory / context.rust_executables
    shutil.copyfile(rust_executable, Util.get_build_dir() / rust_executable.name)

    if hasattr(context, 'solana_inlining') and context.solana_inlining:
        solana_inlining = Path(context.solana_inlining).resolve()
        shutil.copy(solana_inlining, Util.get_build_dir() / solana_inlining.name)

    if hasattr(context, 'solana_summaries') and context.solana_summaries:
        solana_summaries = Path(context.solana_summaries).resolve()
        shutil.copy(solana_summaries, Util.get_build_dir() / solana_summaries.name)
