#!/usr/bin/env python3

import sys
from pathlib import Path

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

import EVMVerifier.certoraContextAttributes as Attrs
from certoraRun import run_certora, CertoraRunResult
from typing import List, Optional


def run_evm_prover(args: List[str]) -> Optional[CertoraRunResult]:
    return run_certora(args, Attrs.EvmProverAttributes)

def entry_point() -> None:
    run_evm_prover(sys.argv[1:])

if __name__ == '__main__':
    entry_point()
