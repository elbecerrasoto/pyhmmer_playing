#!/usr/bin/env python3
import os
from typing import Iterable, Union

from pyhmmer import hmmsearch
from pyhmmer.easel import SequenceFile, Alphabet
from pyhmmer.plan7 import Background, HMMFile, HMM


class HMMFiles(Iterable[HMM]):
    def __init__(self, *files: Union[str, bytes, os.PathLike]):
        self.files = files

    def __iter__(self):
        for file in self.files:
            with HMMFile(file) as hmm_file:
                yield from hmm_file


alphabet = Alphabet.amino()
background = Background(alphabet)
