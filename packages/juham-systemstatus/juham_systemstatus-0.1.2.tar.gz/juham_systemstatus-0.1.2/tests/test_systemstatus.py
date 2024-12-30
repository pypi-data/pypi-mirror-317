import unittest

from juham_systemstatus.systemstatus import SystemStatus


class TestSystemstatus(unittest.TestCase):
    """Unit tests for `Systemstatus` weather forecast masterpiece."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = Systemstatus.get_class_id()
        self.assertEqual("Systemstatus", classid)


if __name__ == "__main__":
    unittest.main()
