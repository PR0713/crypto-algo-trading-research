import pandas as pd
import os

RAW_DIR = "raw"
PROCESSED_DIR = "processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


def preprocess_file(path):
    df = pd.read_csv(path)
    df.dropna(inplace=True)
    df.sort_values("timestamp", inplace=True)
    return df


if __name__ == "__main__":
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            raw_path = os.path.join(RAW_DIR, file)
            df = preprocess_file(raw_path)
            out_path = os.path.join(PROCESSED_DIR, file)
            df.to_csv(out_path, index=False)
            print(f"Processed {file}")
