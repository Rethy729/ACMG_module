import unittest
from BA1_BS1_PM2 import ba1_bs1_pm2

class TestBA1BS1PM2(unittest.TestCase):

    def setUp(self):
        self.header = ['header1', 'gnomADg_AF', 'header2']

    def test_ba1(self):
        for af_value in ['0.1', '0.05']:
            with self.subTest(af_value = af_value):
                variant_data = ['data1', af_value, 'data2']
                variant_evidence = [False] * 12
                ba1_bs1_pm2(self.header, variant_data, variant_evidence)
                for i in range(12):
                    if i != 11:
                        self.assertFalse(variant_evidence[i])
                    else:
                        self.assertTrue(variant_evidence[11])

    def test_bs1(self):
        for af_value in ['0.01', '0.049']:
            with self.subTest(af_value = af_value):
                variant_data = ['data1', af_value, 'data2']
                variant_evidence = [False] * 12
                ba1_bs1_pm2(self.header, variant_data, variant_evidence)
                for i in range(12):
                    if i != 10:
                        self.assertFalse(variant_evidence[i])
                    else:
                        self.assertTrue(variant_evidence[10])

    def test_pm2(self):
        for af_value in ['0.00001', '0.0000001', '0']:
            with self.subTest(af_value = af_value):
                variant_data = ['data1', af_value, 'data2']
                variant_evidence = [False] * 12
                ba1_bs1_pm2(self.header, variant_data, variant_evidence)
                for i in range(12):
                    if i != 2:
                        self.assertFalse(variant_evidence[i])
                    else:
                        self.assertTrue(variant_evidence[2])

    def test_no_af_data(self):
        variant_data = ['data1', '-', 'data2']
        variant_evidence = [False] * 12
        ba1_bs1_pm2(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_no_matching_criteria(self):
        variant_data = ['data1', '0.00005', 'data2']
        variant_evidence = [False] * 12
        ba1_bs1_pm2(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

if __name__ == '__main__':
    unittest.main()