import unittest
import config


class TestConfig(unittest.TestCase):
    def test_token_exists(self):
        self.assertIsNotNone(config.TOKEN)
        self.assertIsInstance(config.TOKEN, str)

    def test_db_path_is_string(self):
        self.assertIsInstance(config.DB_PATH, str)
        self.assertTrue(config.DB_PATH.endswith("database.db"))

    def test_log_dir_is_string(self):
        self.assertIsInstance(config.LOG_DIR, str)
        self.assertTrue(config.LOG_DIR.endswith("logs"))

    def test_category_name(self):
        self.assertIsInstance(config.TICKETS_CATEGORY_NAME, str)
        self.assertTrue(len(config.TICKETS_CATEGORY_NAME) > 0)

    def test_roles_are_strings(self):
        roles = [
            config.ROLE_APPLIED,
            config.ROLE_RECRUITER,
            config.ROLE_OWNER,
            config.ROLE_DEP_OWNER,
            config.ROLE_ADMIN,
            config.ROLE_SUPPORT,
        ]
        for role in roles:
            self.assertIsInstance(role, str)
            self.assertTrue(len(role) > 0)

    def test_channel_names(self):
        self.assertIsInstance(config.LOG_CHANNEL_NAME, str)
        self.assertIsInstance(config.VOICE_CHANNELS, list)
        self.assertEqual(len(config.VOICE_CHANNELS), 3)
        for ch in config.VOICE_CHANNELS:
            self.assertIsInstance(ch, str)

    def test_commands(self):
        self.assertEqual(config.CMD_PREFIX, "!")
        self.assertEqual(config.CMD_REGENT, "regent")
        self.assertEqual(config.CMD_STATS, "stats")
        self.assertEqual(config.CMD_HISTORY, "history")

    def test_dm_message(self):
        self.assertIsInstance(config.DM_MESSAGE, str)
        self.assertIn("Regent", config.DM_MESSAGE)

    def test_ticket_titles(self):
        self.assertIsInstance(config.TICKET_RP_TITLE, str)
        self.assertIsInstance(config.TICKET_CAPT_TITLE, str)
        self.assertTrue(len(config.TICKET_RP_TITLE) > 0)
        self.assertTrue(len(config.TICKET_CAPT_TITLE) > 0)

    def test_regent_embed(self):
        self.assertIsInstance(config.REGENT_EMBED_TITLE, str)
        self.assertIsInstance(config.REGENT_EMBED_DESCRIPTION, str)
        self.assertIn("Regent", config.REGENT_EMBED_TITLE)

    def test_rp_fields_is_list(self):
        self.assertIsInstance(config.RP_FIELDS, list)
        self.assertEqual(len(config.RP_FIELDS), 5)
        for field in config.RP_FIELDS:
            self.assertEqual(len(field), 4)
            label, placeholder, required, max_length = field
            self.assertIsInstance(label, str)
            self.assertIsInstance(placeholder, str)
            self.assertIsInstance(required, bool)
            self.assertIsInstance(max_length, int)

    def test_capt_fields_is_list(self):
        self.assertIsInstance(config.CAPT_FIELDS, list)
        self.assertEqual(len(config.CAPT_FIELDS), 5)

    def test_error_messages(self):
        self.assertIsInstance(config.ERROR_GENERIC, str)
        self.assertIsInstance(config.ERROR_TICKET_CREATE, str)


if __name__ == "__main__":
    unittest.main()
