import unittest
from hcc_risk_models.common import agesexv2

class TestParseAgeSexVar(unittest.TestCase):
    """Test function parse_agesex_var."""

    def test_correct_input(self):
        """agesexv2 - test parse_agesex_var."""

        x = 'F0_34'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 0, 34), (sex, age_lo, age_hi))

        x = 'F35_44'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 35, 44), (sex, age_lo, age_hi))

        x = 'F95_GT'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 95, agesexv2.MAX_AGE), (sex, age_lo, age_hi))

        x = 'NEF0_34'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 0, 34), (sex, age_lo, age_hi))

        x = 'NEF35_44'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 35, 44), (sex, age_lo, age_hi))

        x = 'NEF65'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 65, 65), (sex, age_lo, age_hi))

        x = 'NEF95_GT'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((2, 95, agesexv2.MAX_AGE), (sex, age_lo, age_hi))


        x = 'M0_34'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 0, 34), (sex, age_lo, age_hi))

        x = 'M35_44'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 35, 44), (sex, age_lo, age_hi))

        x = 'M95_GT'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 95, agesexv2.MAX_AGE), (sex, age_lo, age_hi))

        x = 'NEM0_34'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 0, 34), (sex, age_lo, age_hi))

        x = 'NEM35_44'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 35, 44), (sex, age_lo, age_hi))

        x = 'NEM65'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 65, 65), (sex, age_lo, age_hi))

        x = 'NEM95_GT'
        sex, age_lo, age_hi = agesexv2._parse_agesex_var(x)
        self.assertEqual((1, 95, agesexv2.MAX_AGE), (sex, age_lo, age_hi))


class TestCreateDisabl(unittest.TestCase):
    """Test function create_disabl."""

    def test_correct_input(self):
        """agesexv2 - test create_disabl."""
        age = 64
        orecs = [0, 1, 2, 3, 4]
        disabl_arr = [agesexv2.create_disabl(age, orec) for orec in orecs]
        self.assertEqual([0, 1, 1, 1, 1], disabl_arr)

        age = 65
        orecs = [0, 1, 2, 3, 4]
        disabl_arr = [agesexv2.create_disabl(age, orec) for orec in orecs]
        self.assertEqual([0, 0, 0, 0, 0], disabl_arr)


class TestCreateOrigds(unittest.TestCase):
    """Test function create_origds."""

    def test_correct_input(self):
        """agesexv2 - test create_origds."""
        disabl = 0; orecs = [0, 1, 2, 3, 4]
        origds_arr = [agesexv2.create_origds(disabl, orec) for orec in orecs]
        self.assertEqual([0, 1, 0, 0, 0], origds_arr)

        disabl = 1; orecs = [0, 1, 2, 3, 4]
        origds_arr = [agesexv2.create_origds(disabl, orec) for orec in orecs]
        self.assertEqual([0, 0, 0, 0, 0], origds_arr)


class TestCreateCell(unittest.TestCase):
    """Test function create_cell."""

    def test_correct_input(self):
        """agesexv2 - test create_cell."""
        # check cell only key "M65_69" should be 1
        age = 67; sex = 1
        cell = agesexv2.create_cell(age, sex)
        for k, v in cell.items():
            if k == 'M65_69':
                expected = 1
            else:
                expected = 0
            self.assertEqual(expected, v)


class TestCreateNecell(unittest.TestCase):
    """Test function create_necell."""

    def test_correct_input(self):
        """agesexv2 - test create_necell."""
        # check necell only key "NEM67" should be 1
        age = 67; sex = 1
        necell = agesexv2.create_necell(age, sex)
        for k, v in necell.items():
            if k == 'NEM67':
                expected = 1
            else:
                expected = 0
            self.assertEqual(expected, v)



if __name__ == '__main__':
    unittest.main()
