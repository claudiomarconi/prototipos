import re
import unittest
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "ConsumoApiAgilleControl"
    / "MainForm.pas"
)


def read_source():
    return SOURCE.read_text(encoding="cp1252")


def extract_routine(source, name):
    pattern = re.compile(
        rf"(?:procedure|function)\s+TfrmMain\.{name}\b.*?"
        rf"(?=\n(?:procedure|function)\s+TfrmMain\.|\ninitialization\b)",
        re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise AssertionError(f"Routine {name} not found")
    return match.group(0)


class ClientInitializationSourceTests(unittest.TestCase):
    def test_connection_helper_initializes_and_authenticates_client(self):
        routine = extract_routine(read_source(), "EnsureClientAuthenticated")

        self.assertIn("if not Assigned(FClient) then", routine)
        self.assertIn(
            "FClient := TRestHttpClient.Create('notei5', '8888', FModel);",
            routine,
        )
        self.assertIn(
            "if not FClient.SetUser('cmarcony', 'synopse') then",
            routine,
        )
        self.assertIn("raise Exception.Create", routine)

    def test_product_and_sales_actions_ensure_authenticated_client(self):
        source = read_source()

        for name in ("Button1Click", "Button2Click", "Button3Click"):
            with self.subTest(name=name):
                routine = extract_routine(source, name)
                self.assertIn("EnsureClientAuthenticated;", routine)


if __name__ == "__main__":
    unittest.main()
