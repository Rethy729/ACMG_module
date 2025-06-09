import unittest
from unittest.mock import patch

from PM4_BP3 import pm4_bp3

class TestPM4BP3(unittest.TestCase):
    def setUp(self):
        self.header = ['Uploaded_variation', 'Location', 'Consequence']

    def test_stop_lost_pm4(self):
        variant_data = ['var', 'chr1:10000', 'stop_lost']
        variant_evidence = [False] * 12
        pm4_bp3(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 3:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[3])

    @patch('PM4_BP3.rmsk_dict_generator')
    def test_inframe_insertion_inside_rmsk_bp3(self, mock_rmsk):
        mock_rmsk.return_value = {'chr1':[(30, 500)]}
        variant_data = ['var', 'chr1:200-202', 'inframe_insertion']
        variant_evidence = [False] * 12
        pm4_bp3(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 7:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[7])

    @patch('PM4_BP3.rmsk_dict_generator')
    def test_inframe_insertion_outside_rmsk_pm4(self, mock_rmsk):
        mock_rmsk.return_value = {'chr1': [(30, 500)]}
        variant_data = ['var', 'chr1:498-503', 'inframe_insertion']
        variant_evidence = [False] * 12
        pm4_bp3(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 3:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[3])

    @patch('PM4_BP3.rmsk_dict_generator')
    def test_inframe_insertion_before_rmsk_pm4(self, mock_rmsk):
        mock_rmsk.return_value = {'chr1': [(30, 500)]}
        variant_data = ['var', 'chr1:2-7', 'inframe_insertion']
        variant_evidence = [False] * 12
        pm4_bp3(self.header, variant_data, variant_evidence)
        for i in range(12):
            if i != 3:
                self.assertFalse(variant_evidence[i])
            else:
                self.assertTrue(variant_evidence[3])
