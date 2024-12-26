import pandas as pd
from datasets import DatasetDict, Dataset,load_dataset
from sklearn.model_selection import train_test_split

def split_dataset(dataset, test_size=0.2, stratify=None):
    """
    Split the given dataset into train and test sets.

    Args:
        dataset (Dataset): A Hugging Face Dataset object.
        test_size (float): Proportion of the data to be used as the validation set.
        stratify (str): Column name for stratified sampling. If None, no stratification is applied.

    Returns:
        DatasetDict: Dictionary containing 'train' and 'test' splits.
    """
    # Convert to DataFrame
    df = pd.DataFrame(dataset)
    
    # Perform train-test split
    if stratify:
        train_df, val_df = train_test_split(df, test_size=test_size, stratify=df[stratify], random_state=42)
    else:
        train_df, val_df = train_test_split(df, test_size=test_size, random_state=42)
    
    # Convert DataFrames back to Hugging Face Dataset
    train_val_dataset = DatasetDict(
        {
            "train": Dataset.from_pandas(train_df),
            "test": Dataset.from_pandas(val_df),
        }
    )
    
    return train_val_dataset

if __name__=="__main__":
    DATA_FILE = "./testdata/data.jsonl"
    dataset = load_dataset("json", data_files=DATA_FILE, split="train")

    split_data = split_dataset(dataset, test_size=0.2, stratify="label")

    print(split_data)
