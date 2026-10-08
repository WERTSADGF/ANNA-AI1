import pandas as pd
import tempfile
from pathlib import Path
import importlib
import unittest


class TestDataPreprocessingImport(unittest.TestCase):

    def test_module_import_has_no_dataset_side_effect(self):
        module = importlib.import_module("data_preprocessing")
        self.assertIsNotNone(module)


    def test_preprocess_data_splits_and_fills_numeric_values(self):
        from data_preprocessing import preprocess_data

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "dataset.csv"

            frame = pd.DataFrame(
                {
                    "feature": [1.0, None, 3.0, 4.0, 5.0],
                    "target": [0, 1, 0, 1, 0],
                }
            )
            frame.to_csv(path, index=False)

            X_train, X_test, y_train, y_test = preprocess_data(
                str(path),
                "target",
                test_size=0.4,
                random_state=42,
            )

            self.assertEqual(len(X_train), 3)
            self.assertEqual(len(X_test), 2)
            self.assertEqual(len(y_train), 3)
            self.assertEqual(len(y_test), 2)
            self.assertNotIn("target", X_train.columns)
            self.assertFalse(X_train["feature"].isna().any())
            self.assertFalse(X_test["feature"].isna().any())

if __name__ == "__main__":
    unittest.main()
