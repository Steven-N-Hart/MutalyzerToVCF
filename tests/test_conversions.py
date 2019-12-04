import os
import sys
import unittest

sys.path.insert(0, '..')
from pyfaidx import Fasta
from modules.conversions import *

fasta_file = Fasta(os.path.join('..', 'refs', 'allchr.fa'))


class TestConversions(unittest.TestCase):

    def test_insertion(self):
        variant = 'NC_000011.9:g.108190737_108190738insTT'
        expected = ('chr11', 108190736, 'C', 'CTT')
        observed = convert_ins(variant, fasta_file)
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

    def test_delins(self):
        variant = 'NC_000011.9:g.108196200_108196219delinsCA'
        expected = ('chr11', 108196199, 'ATGTATTAAGGACATTCTCAC', 'ACA')
        observed = convert_delins(variant, fasta_file)
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

    def test_convert_del(self):
        VARIANTS = ['NC_000002.11:g.215609822del', 'NC_000002.11:g.215609822delA', 'NC_000002.11:g.215609822del1']
        expected = ('chr2', 215609821, 'GA', 'G')
        for variant in VARIANTS:
            observed = convert_del(variant, fasta_file)
            self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

        variant = 'NC_000011.9:g.108216454_108216457delTATT'
        observed = convert_del(variant, fasta_file)
        expected = ('chr11', 108216453, 'ATATT', 'A')
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

        variant = 'NC_000017.10:g.41244410_41244419del10'
        observed = convert_del(variant, fasta_file)
        expected = ('chr17', 41244409, 'CTTCATTAATA', 'C')
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

    def test_dup(self):
        VARIANTS = ['NC_000011.9:g.108117842dupT', 'NC_000011.9:g.108117842dup', 'NC_000011.9:g.108117842dup1']
        expected = ('chr11', 108117841, 'A', 'AT')
        for variant in VARIANTS:
            observed = convert_dup(variant, fasta_file)
            self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

        variant = 'NC_000011.9:g.108119733_108119736dupACAG'
        observed = convert_dup(variant, fasta_file)
        expected = ('chr11', 108119732, 'T', 'TACAG')
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

        variant = 'NC_000017.10:g.41246724_41246733dup10'
        observed = convert_dup(variant, fasta_file)
        expected = ('chr17', 41246723, 'G', 'GCCACATGGCT')
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))

    def test_snp(self):
        variant = 'NC_000011.9:g.108186818C>T'
        observed = convert_snp(variant, fasta_file)
        expected = ('chr11', 108186818, 'C', 'T')
        self.assertTupleEqual(expected, observed, "Expected: {}, but Observed: {}".format(expected, observed))


if __name__ == '__main__':
    unittest.main()
