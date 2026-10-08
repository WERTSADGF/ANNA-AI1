import pandas as pd
from sklearn.model_selection import train_test_split


def preprocess_data(
    dataset_path: str,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42,
):
    df = pd.read_csv(dataset_path)

    df = df.copy()
    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:
        df[numeric_columns] = df[numeric_columns].fillna(
            df[numeric_columns].mean()
        )

    if target_column not in df.columns:
        raise ValueError(
            f"Target column not found: {target_column}"
        )

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )
