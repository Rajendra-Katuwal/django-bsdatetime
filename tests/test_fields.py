import unittest
from django_bsdatetime.fields import BSDateField

class TestDjangoBSDateTime(unittest.TestCase):
    def test_field_description(self):
        """Test field has correct description."""
        field = BSDateField()
        self.assertEqual(field.description, "Bikram Sambat date")

    def test_aliases(self):
        """Test that top-level imports are the same classes as django_bsdatetime.fields,
        and that the two field classes remain distinct from each other."""
        from django_bsdatetime import BSDateField as TopBSDateField, BSDateTimeField as TopBSDateTimeField
        from django_bsdatetime.fields import BSDateField as FieldsBSDateField, BSDateTimeField as FieldsBSDateTimeField

        self.assertIs(TopBSDateField, FieldsBSDateField)
        self.assertIs(TopBSDateTimeField, FieldsBSDateTimeField)
        self.assertIsNot(TopBSDateField, TopBSDateTimeField)

if __name__ == "__main__":
    unittest.main()
