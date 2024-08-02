#!/usr/bin/env python3
import re
import sys
from utils import *
from pathlib import Path
from icecream import ic

# GENOMES_DIR = Path(sys.argv[1])
QUERIES_DIR = Path("queries")
OUT_FILE = Path(sys.argv[1])
OUT_FH = open(OUT_FILE, "ab")
VERBOSE = False

GENOMES = sys.argv[2:]

GENOME_REGEX = re.compile(r"(GCF_\d+\.\d)\.faa$")


def get_hmms(queries_path):
    queries_path = Path(queries_path)
    hmms_files = HMMFiles(*queries_path.iterdir())
    return hmms_files


def run_genome(genome_path, hmms_files):
    with SequenceFile(genome_path, digital=True) as genome_file:
        genome = genome_file.read_block()
    hits = hmmsearch(hmms_files, genome)
    # del genome
    return hits


def parse_genome(genome_path):
    genome_path = str(genome_path)
    genome = re.search(GENOME_REGEX, genome_path).group(1)
    return genome


if __name__ == "__main__":
    hmms_files = get_hmms(QUERIES_DIR)

    for idx, genome in enumerate(GENOMES):
        idx += 1
        if VERBOSE:
            print(f".{idx}", end="", flush=True)

        genome_id = parse_genome(genome)
        hits = run_genome(genome, hmms_files)

        for hit in hits:
            if len(hit) > 0:
                OUT_FH.write(f"{genome_id}\t".encode("utf-8"))
                hit.write(OUT_FH, header=False)

        del hits
