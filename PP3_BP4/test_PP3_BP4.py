import unittest
from PP3_BP4 import pp3_bp4

class TestPP3BP4(unittest.TestCase):

    def setUp(self):
        self.header = ['SIFT', 'PolyPhen']

    def test_PP3(self):
        variant_data = ['deleterious(score)', 'probably_damaging(score)']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 5:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[5])

    def test_BP4(self):
        variant_data = ['tolerated(score)', 'benign(score)']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 8:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[8])

    def test_conflict_1(self):
        variant_data = ['tolerated(score)', 'probably_damaging(score)']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_conflict_2(self):
        variant_data = ['deleterious(score)', 'benign(score)']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_both_no_data(self):
        variant_data = ['-', '-']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_sift_no_data(self):
        variant_data = ['-', 'benign(score)']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_polyphen_no_data(self):
        variant_data = ['deleterious(score)', '-']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))