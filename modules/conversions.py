import logging
import re

logger = logging.getLogger(__name__)

def convert_ins(variant, fasta_file):
    assert re.search("ins[A-Z]+$", variant), "This doesn\'t look like an insertion: {}".format(variant)

    # NC_000011.9:g.108190737_108190738insTT -> chr11 108190736   C   CTT
    chr = 'chr' + re.sub('NC_[0]+', '', variant.split('.')[0])
    start = int(variant.split(':')[1].split('.')[1].split('_')[0])
    new_start = start - 2
    ref = fasta_file[chr][new_start:start - 1].seq
    alt = ref + variant.split('ins')[1]
    return chr, start - 1, ref, alt


def convert_delins(variant, fasta_file):
    assert re.search("delins[0-9A-Z]+$", variant), "This doesn\'t look like an insdel: {}".format(variant)

    # NC_000011.9:g.108196200_108196219delinsCA -> chr11    108196199   ATGTATTAAGGACATTCTCAC   ACA
    # NC_000011.9:g.108122705_108122706delinsAT -> chr11    108122704   ATC AAT
    # NC_000017.10:g.41245354delinsTT ->           chr17    41245353    TC  TTT
    # NC_000013.10:g.32971146_32971147delinsCT ->  chr13    32971145    TGC TCT
    chr = 'chr' + re.sub('NC_[0]+', '', variant.split('.')[0])
    if '_' in variant.split(':')[1].split('.')[1]:
        start = int(variant.split(':')[1].split('.')[1].split('_')[0])
        stop = int(variant.split(':')[1].split('.')[1].split('_')[1].split('delins')[0])
        new_start = start - 1
    else:
        new_start = int(variant.split(':')[1].split('.')[1].split('delins')[0]) - 1
        stop = new_start + len(variant.split(':')[1].split('.')[1].split('delins')[1]) - 1

    ref = fasta_file[chr][new_start - 1:stop].seq
    alt = ref[:1] + variant.split('ins')[1]
    return chr, new_start, ref, alt


def convert_del(variant, fasta_file):
    assert re.search("del[0-9A-Z]+|del$", variant), "This doesn\'t look like a deletion: {}".format(variant)

    # NC_000002.11:g.215609822del ->                chr2  215609821   GA            G
    # NC_000002.11:g.215609822delA ->               chr2  215609821   GA            G
    # NC_000002.11:g.215609822del1 ->               chr2  215609821   GA            G
    # NC_000011.9:g.108216454_108216457delTATT ->   chr11 108216453   ATATT         A
    # NC_000017.10:g.41244410_41244419del10 ->      chr17  41244409   CTTCATTAATA   C

    chr = 'chr' + re.sub('NC_[0]+', '', variant.split('.')[0])

    # Check for a stop
    var = variant.split(':')[1].split('.')[1].split('del')[0]
    if '_' in var:
        # NC_000011.9:g.108216454_108216457delTATT
        start, stop = [int(x) for x in var.split('_')]
        start = start - 1
    else:
        pre_alt = variant.split(':')[1].split('.')[1].split('del')[1]
        start = int(var) - 1

        if pre_alt.isdigit():
            # NC_000002.11:g.215609822del1
            stop = start + int(pre_alt)
        else:
            if variant.endswith('del'):
                stop = start + 1
            else:
                # NC_000002.11:g.215609822delA
                stop = start + len(pre_alt)

    ref = fasta_file[chr][start - 1: stop].seq
    alt = fasta_file[chr][start - 1: start].seq
    return chr, start, ref, alt


def convert_dup(variant, fasta_file):
    assert re.search("dup[0-9A-Z]+|dup$", variant), "This doesn\'t look like a duplication: {}".format(variant)

    # NC_000011.9:g.108119733_108119736dupACAG ->   chr11  108119732   T   TACAG
    # NC_000017.10:g.41246724_41246733dup10 ->      chr17   41246723   G   GCCACATGGCT
    # NC_000011.9:g.108117842dupT ->                chr11  108117841   A   AT
    # NC_000011.9:g.108117842dup  ->                chr11  108117841   A   AT
    # NC_000011.9:g.108117842dup1  ->               chr11  108117841   A   AT

    chr = 'chr' + re.sub('NC_[0]+', '', variant.split('.')[0])

    # Check for a dup
    var = variant.split(':')[1].split('.')[1].split('dup')[0]
    if '_' in var:
        # NC_000011.9:g.108119733_108119736dupACAG
        start, stop = [int(x) for x in var.split('_')]
        start = start - 1
    else:
        # NC_000011.9:g.108117842dup
        start = int(var) - 1
        if variant.endswith('dup'):
            stop = start + 1
        else:
            if variant.split('dup')[1].isdigit():
                # NC_000011.9:g.108117842dup1
                stop = start + int(variant.split('dup')[1])
            else:
                # NC_000011.9:g.108117842dupT
                stop = start + len(variant.split('dup')[1])

    ref = fasta_file[chr][start - 1: start].seq
    alt = fasta_file[chr][start - 1: stop].seq
    return chr, start, ref, alt


def convert_snp(variant, fasta_file):
    assert re.search("[0-9][A-Z]>[A-Z]$", variant), "This doesn\'t look like a snp: {}".format(variant)
    # NC_000011.9:g.108186818C>T -> chr11   108186818   C   T
    # NC_000017.10:g.33434435A>G -> chr17   33434435    T   C   # Reverse strand
    chr = 'chr' + re.sub('NC_[0]+', '', variant.split('.')[0])

    var = variant.split(':')[1].split('.')[1]
    start = int(variant.split(':')[1].split('.')[1][:-3])

    ref = fasta_file[chr][start - 1: start].seq
    ref_1 = variant.split(':')[1].split('.')[1][-3:-2].strip()
    if ref != ref_1:
        logger.warning("{} Wrong reference base provided! Provided: {}, Actual: {}".format(variant, ref_1, ref))

    alt = variant.split(':')[1].split('.')[1][-1:]
    return chr, start, ref, alt
