import unittest
from unittest.mock import patch

from PS2 import ps2

class TestPS2(unittest.TestCase):

    def setUp(self):
        self.header = ['Uploaded_variation', 'Allele']

    @patch('PS2.de_novo_variant_set_generator')
    def test_snv_match_ps2(self, mock_denovo_set):
        mock_denovo_set.return_value = {
            ('chr1', '10000', 'A', 'G')
        }
        variant_data = ['chr1_10000_A/G', 'G']
        variant_evidence = [False] * 12
        ps2(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 1:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[1])

    @patch('PS2.de_novo_variant_set_generator')
    def test_insertion_match_ps2(self, mock_denovo_set):
        mock_denovo_set.return_value = {
            ('chr1', '20000', '-', 'AC')
        }
        variant_data = ['chr1_20000_-/AC', 'AC']
        variant_evidence = [False] * 12
        ps2(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 1:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[1])

    @patch('PS2.de_novo_variant_set_generator')
    def test_deletion_match_ps2(self, mock_denovo_set):
        mock_denovo_set.return_value = {
            ('chr1', '30000', 'TC', '-')
        }
        variant_data = ['chr1_30000_TC/-', '-']
        variant_evidence = [False] * 12
        ps2(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 1:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[1])

    @patch('PS2.de_novo_variant_set_generator')
    def test_nomatch(self, mock_denovo_set):
        mock_denovo_set.return_value = {
            ('chr1', '40000', 'A', 'T'),
            ('chr1', '50000', '-', 'AC'),
            ('chr1', '60000', 'AC', '-')
        }
        for v_d in [
            ['chr1_40000_A/C', 'C'], ['chr1_40001_A/T', 'T'], ['chr2_40000_A/T', 'T'],
            ['chr1_50000_-/ACC', 'ACC'], ['chr1_50001_-/AC', 'AC'], ['chr2_50000_-/AC', 'AC'],
            ['chr1_60000_ACC/-', '-'], ['chr1_60001_AC/-', '-'], ['chr2_60000_AC/-', '-']
        ]:
            with self.subTest(v_d = v_d):
                variant_data = v_d
                variant_evidence = [False] * 12
                ps2(self.header, variant_data, variant_evidence)
                self.assertFalse(all(b for b in variant_evidence))