#!/usr/bin/env python3

import sys
import EVMVerifier.certoraContextAttributes as Attrs
from certoraRun import run_certora, CertoraRunResult
from typing import List, Optional


def run_soroban_prover(args: List[str]) -> Optional[CertoraRunResult]:
    return run_certora(args, Attrs.SorobanProverAttributes)


if __name__ == '__main__':
    run_soroban_prover(sys.argv[1:])
