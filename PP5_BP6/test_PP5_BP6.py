import unittest
from PP5_BP6 import pp5_bp6

class TestPP5BP6(unittest.TestCase):
    def setUp(self):
        self.header = ['header1', 'Consequence', 'header2', 'ClinVar_CLNSIG', 'ClinVar_CLNREVSTAT']

    def test_BP6(self):
        for clnrevstat in ['practice_guideline',
                           'reviewed_by_expert_panel',
                           'criteria_provided,_multiple_submitters,_no_conflicts',
                           'criteria_provided,_single_submitter']:
            with self.subTest(clnrevstat = clnrevstat):
                variant_data = ['data1', 'all_variant', 'data2', 'Benign', clnrevstat]
                variant_evidence = [False] * 12
                pp5_bp6(self.header, variant_data, variant_evidence)
                for i in range(12):
                    if i != 9:
                        self.assertFalse(variant_evidence[i])
                    else:
                        self.assertTrue(variant_evidence[9])
    def test_PP5(self):
        for clnrevstat in ['practice_guideline',
                           'reviewed_by_expert_panel',
                           'criteria_provided,_multiple_submitters,_no_conflicts',
                           'criteria_provided,_single_submitter']:
            with self.subTest(clnrevstat = clnrevstat):
                variant_data = ['data1', 'not_missense_variant', 'data2', 'Pathogenic', clnrevstat]
                variant_evidence = [False] * 12
                pp5_bp6(self.header, variant_data, variant_evidence)
                for i in range(12):
                    if i != 6:
                        self.assertFalse(variant_evidence[i])
                    else:
                        self.assertTrue(variant_evidence[6])

    def test_missense(self):
        for clnrevstat in ['practice_guideline',
                           'reviewed_by_expert_panel',
                           'criteria_provided,_multiple_submitters,_no_conflicts',
                           'criteria_provided,_single_submitter']:
            with self.subTest(clnrevstat = clnrevstat):
                variant_data = ['data1', 'missense_variant', 'data2', 'Pathogenic', clnrevstat]
                variant_evidence = [False] * 12
                pp5_bp6(self.header, variant_data, variant_evidence)
                self.assertFalse(all(b for b in variant_evidence))

    def test_both_no_data(self):
        variant_data = ['data1', 'all_variant', 'data2', '-', '-']
        variant_evidence = [False] * 12
        pp5_bp6(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_sig_no_data(self):
        variant_data = ['data1', 'all_variant','data2', '-', 'status']
        variant_evidence = [False] * 12
        pp5_bp6(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))

    def test_stat_no_data(self):
        variant_data = ['data1', 'all_variant', 'data2', 'sig', '-']
        variant_evidence = [False] * 12
        pp5_bp6(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))