import unittest
from django_bsdatetime.fields import BSDateField

class TestDjangoBikramSambat(unittest.TestCase):
    def test_field_description(self):
        """Test field has correct description."""
        field = BSDateField()
        self.assertEqual(field.description, "Bikram Sambat date")

    def test_aliases(self):
        """Test field aliases work."""
        from django_bsdatetime import BSDateField, BSDateTimeField
        
        # These should be the same class
        self.assertEqual(BSDateField, BSDateField)
        self.assertEqual(BSDateTimeField, BSDateField)

if __name__ == "__main__":
    unittest.main()
