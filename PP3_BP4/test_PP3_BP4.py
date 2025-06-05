import unittest
from PP3_BP4 import pp3_bp4

class TestPP3BP4(unittest.TestCase):

    def setUp(self):
        self.header = ['header1', 'SIFT', 'PolyPhen', 'header2']

    def test_PP3(self):
        variant_data = ['data1','deleterious(score)', 'probably_damaging(score)', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 5:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[5])

    def test_BP4(self):
        variant_data = ['data1', 'tolerated(score)', 'benign(score)', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 8:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[8])

    def test_conflict_1(self):
        variant_data = ['data1', 'tolerated(score)', 'probably_damaging(score)', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_conflict_2(self):
        variant_data = ['data1', 'deleterious(score)', 'benign(score)', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_both_no_data(self):
        variant_data = ['data1', '-', '-', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_sift_no_data(self):
        variant_data = ['data1', '-', 'benign(score)', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_polyphen_no_data(self):
        variant_data = ['data1', 'deleterious(score)', '-', 'data2']
        variant_evidence = [False] * 12
        pp3_bp4(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

if __name__ == '__main__':
    unittest.main()