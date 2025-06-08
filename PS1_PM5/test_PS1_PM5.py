import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict

from PS1_PM5 import ps1_pm5

class TestPS1PM5(unittest.TestCase):
    def setUp(self):
        self.header = [
            'Location', 'Consequence', 'HGVSc', 'HGVSp',
            'ClinVar_CLNSIG', 'ClinVar_CLNREVSTAT']

    def test_missense_pathogenic_ps1(self):
        for clnrevstat in ['practice_guideline',
                           'reviewed_by_expert_panel',
                           'criteria_provided,_multiple_submitters,_no_conflicts',
                           'criteria_provided,_single_submitter']:
            with self.subTest(clnrevstat = clnrevstat):
                variant_data = [
                    'chr1:12345', 'missense_variant',
                    'NM_000000.0:c.111A>G', 'NP_000000.0:p.Gly11Arg',
                    'Pathogenic', clnrevstat
                    ]
                variant_evidence = [False] * 12
                ps1_pm5(self.header, variant_data, variant_evidence)
                for i in range(12):
                    if i != 0:
                        self.assertFalse(variant_evidence[i])
                    else:
                        self.assertTrue(variant_evidence[0])

    @patch('PS1_PM5.clinvar_dict_generator', return_value={})
    def test_missense_not_pathogenic(self, mock_dict_gen):
        variant_data = [
            'chr1:12345', 'missense_variant',
            'NM_000000.0:c.111A>G', 'NP_000000.0:p.Gly11Arg',
            'Something_else', 'no_assertion'
        ]
        variant_evidence = [False] * 12
        ps1_pm5(self.header, variant_data, variant_evidence)
        self.assertFalse(all(b for b in variant_evidence))


    @patch('PS1_PM5.clinvar_dict_generator')
    def test_diff_hgvsc_same_hgvsp_ps1(self, mock_dict_gen):
        mock_dict = {'1:12345':[['NM_000000.0:c.111A>G', 'NP_000000.0:p.Gly11Arg']]}
        mock_dict_gen.return_value = mock_dict

        variant_data = [
                    'chr1:12345', 'missense_variant',
                    'NM_000000.0:c.111A>T', 'NP_000000.0:p.Gly11Arg',
                    'Something_else', 'no_assertion'
                    ]
        variant_evidence = [False] * 12
        ps1_pm5(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 0:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[0])

    @patch('PS1_PM5.clinvar_dict_generator')
    def test_diff_hgvsc_diff_hgvsp_pm5(self, mock_dict_gen):
        mock_dict = {'1:12345':[['NM_000000.0:c.111A>G', 'NP_000000.0:p.Gly11Arg']]}
        mock_dict_gen.return_value = mock_dict

        variant_data = [
                    'chr1:12345', 'missense_variant',
                    'NM_000000.0:c.111A>T', 'NP_000000.0:p.Gly11His',
                    'Something_else', 'no_assertion'
                    ]
        variant_evidence = [False] * 12
        ps1_pm5(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 4:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[4])