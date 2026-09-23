import unittest

from config.settings import load_settings
from security.policy import PermissionLevel, evaluate_permission


class TestFoundation(unittest.TestCase):

    def test_settings_load(self):
        settings = load_settings()
        self.assertEqual(settings.app_name, "ANNA AI")

    def test_read_only_permission(self):
        result = evaluate_permission(PermissionLevel.READ_ONLY)
        self.assertTrue(result.allowed)
        self.assertFalse(result.requires_confirmation)

    def test_high_impact_requires_confirmation(self):
        result = evaluate_permission(PermissionLevel.HIGH_IMPACT)
        self.assertFalse(result.allowed)
        self.assertTrue(result.requires_confirmation)

    def test_high_impact_with_confirmation(self):
        result = evaluate_permission(
            PermissionLevel.HIGH_IMPACT,
            confirmed=True,
        )
        self.assertTrue(result.allowed)
        self.assertTrue(result.requires_confirmation)


if __name__ == "__main__":
    unittest.main()
