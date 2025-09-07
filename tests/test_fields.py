import unittest
from django_bsdatetime import BikramSambatDateField

class TestDjangoBikramSambat(unittest.TestCase):
    def test_field_description(self):
        """Test field has correct description."""
        field = BikramSambatDateField()
        self.assertEqual(field.description, "Bikram Sambat date")

    def test_aliases(self):
        """Test field aliases work."""
        from django_bsdatetime import BSDateField, NepaliDateField
        
        # These should be the same class
        self.assertEqual(BSDateField, BikramSambatDateField)
        self.assertEqual(NepaliDateField, BikramSambatDateField)

if __name__ == "__main__":
    unittest.main()
