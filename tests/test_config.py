import os
from unittest import TestCase, main
from unittest.mock import patch

import config


class TCFromEnv(TestCase):
    def test_empty_env(self):
        with self.assertRaises(RuntimeError):
            config.read_config_from_env()

    def test_empty_cmd(self):
        with self.assertRaises(RuntimeError):
            config.read_config_from_cmd()

    def test_valid_path(self):
        with patch.dict(os.environ, {'CONFIG_PATH': 'config/dev.json'}):
            config.read_config_from_env()


if __name__ == "__main__":
    main()
