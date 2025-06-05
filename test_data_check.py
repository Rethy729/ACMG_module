import unittest
from unittest.mock import patch
from io import StringIO

from data_check import data_check

class TestDataCheck(unittest.TestCase):

    def setUp(self):
        self.required_fields = [
            'Uploaded_variation', 'Allele', 'Location', 'Consequence',
            'gnomADg_AF', 'SIFT', 'PolyPhen', 'HGVSc', 'HGVSp',
            'ClinVar_CLNSIG', 'ClinVar_CLNREVSTAT']

    def test_all_headers_present(self):
        header = self.required_fields
        self.assertTrue(data_check(header))

    @patch('sys.stdout', new_callable=StringIO)
    def test_some_headers_missing(self, mock_stdout):
        header = self.required_fields.copy()
        header.remove('SIFT')
        header.remove('HGVSp')

        result = data_check(header)
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn('please annotate sift, hgvsp', output.lower())

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_headers_missing(self, mock_stdout):
        header = []
        result = data_check(header)
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("please annotate", output.lower())
        for field in self.required_fields:
            self.assertIn(field.lower(), output.lower())