import json
import pandas as pd
import numpy as np
from datasets import DatasetDict, Dataset, load_dataset
from sklearn.model_selection import train_test_split
from itertools import combinations
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold
from typing import Union, List, Dict


def is_multilabel(df: pd.DataFrame, column: str) -> bool:
    """
    判断是否为多标签数据

    Args:
        df: 输入数据框
        column: 标签列名

    Returns:
        bool: 是否为多标签数据
    """
    try:
        if not len(df):
            return False
        first_valid_value = df[column].dropna().iloc[0]
        return isinstance(first_valid_value, (list, np.ndarray))
    except (KeyError, IndexError):
        return False


def get_label_matrix(labels: List, unique_labels: List) -> np.ndarray:
    """
    将标签列表转换为二值矩阵

    Args:
        labels: 标签列表
        unique_labels: 唯一标签列表

    Returns:
        np.ndarray: 二值矩阵
    """
    matrix = np.zeros(len(unique_labels))
    label_to_index = {label: idx for idx, label in enumerate(unique_labels)}
    for label in labels:
        if label in label_to_index:
            matrix[label_to_index[label]] = 1
    return matrix


def split_dataset(
    dataset: Union[Dataset, pd.DataFrame], test_size: float = 0.2, stratify: str = None
) -> DatasetDict:
    """
    Split the given dataset into train and test sets.
    Support both single-label and multi-label stratification.

    Args:
        dataset: 输入数据集
        test_size: 测试集比例
        stratify: 分层抽样的列名

    Returns:
        DatasetDict: 包含训练集和测试集的数据集字典

    Raises:
        ValueError: 当输入参数无效时抛出
    """
    try:
        # 输入验证
        if not 0 < test_size < 1:
            raise ValueError("test_size must be between 0 and 1")

        # 转换为DataFrame
        if isinstance(dataset, Dataset):
            df = pd.DataFrame(dataset)
        elif isinstance(dataset, pd.DataFrame):
            df = dataset.copy()
        else:
            raise ValueError("dataset must be either a Dataset or DataFrame")

        # 检查是否存在分层列
        if stratify and stratify not in df.columns:
            raise ValueError(f"Column {stratify} not found in dataset")

        if stratify is None:
            train_df, val_df = train_test_split(
                df, test_size=test_size, random_state=42
            )
        else:
            if is_multilabel(df, stratify):
                # 处理空值
                df = df.dropna(subset=[stratify])

                # 获取所有唯一的标签
                unique_labels = list(
                    set(
                        [
                            label
                            for labels in df[stratify]
                            if isinstance(labels, (list, np.ndarray))
                            for label in labels
                        ]
                    )
                )

                # 将标签列表转换为二值矩阵
                label_matrix = np.array(
                    [get_label_matrix(labels, unique_labels) for labels in df[stratify]]
                )

                # 使用MultilabelStratifiedKFold进行划分
                mskf = MultilabelStratifiedKFold(
                    n_splits=int(1 / test_size), shuffle=True, random_state=42
                )

                # 获取划分的索引
                try:
                    train_idx, test_idx = next(mskf.split(df, label_matrix))
                except StopIteration:
                    raise ValueError("Failed to split dataset with given parameters")

                # 使用索引划分数据
                train_df = df.iloc[train_idx]
                val_df = df.iloc[test_idx]

            else:
                train_df, val_df = train_test_split(
                    df, test_size=test_size, stratify=df[stratify], random_state=42
                )

        # 重置索引并删除索引列
        train_df = train_df.reset_index(drop=True)
        val_df = val_df.reset_index(drop=True)

        # 转换为字典格式，避免产生额外的索引列
        train_dict = {col: train_df[col].tolist() for col in train_df.columns}
        val_dict = {col: val_df[col].tolist() for col in val_df.columns}

        # 创建Dataset
        train_dataset = Dataset.from_dict(train_dict)
        val_dataset = Dataset.from_dict(val_dict)

        # 构建DatasetDict
        train_val_dataset = DatasetDict(
            {
                "train": train_dataset,
                "test": val_dataset,
            }
        )

        return train_val_dataset

    except Exception as e:
        raise ValueError(f"Error splitting dataset: {str(e)}")


def analyze_label_distribution(dataset, label_column, top_k=None, min_freq=None):
    """
    分析数据集中标签的分布情况，支持单标签和多标签情况

    参数:
        dataset (list): 数据集
        label_column (str): 标签列的名称
        top_k (int, optional): 只返回前k个最常见的标签
        min_freq (int, optional): 最小频率阈值，低于该阈值的标签将被过滤

    返回:
        dict: 包含标签分布信息和统计摘要的字典
    """
    if not dataset:
        raise ValueError("Dataset is empty")

    all_labels = {}
    total_samples = len(dataset)
    samples_per_label = {}  # 记录每个标签包含的样本数
    label_lengths = []  # 记录每个样本的标签数量

    first_label = dataset[0][label_column]
    is_multi_label = isinstance(first_label, (list, tuple, set))

    # 统计标签分布
    for item in dataset:
        labels = item[label_column]
        if is_multi_label:
            label_lengths.append(len(labels))
            for label in labels:
                all_labels[label] = all_labels.get(label, 0) + 1
                if label not in samples_per_label:
                    samples_per_label[label] = set()
                samples_per_label[label].add(id(item))
        else:
            label_lengths.append(1)
            all_labels[labels] = all_labels.get(labels, 0) + 1
            if labels not in samples_per_label:
                samples_per_label[labels] = set()
            samples_per_label[labels].add(id(item))  # 使用 labels 而不是 label

    # 过滤标签，只保留频率高于 min_freq 的标签
    if min_freq is not None:
        all_labels = {k: v for k, v in all_labels.items() if v >= min_freq}

    # 计算标签分布
    label_dist = {}
    for label, count in all_labels.items():
        percentage = count / total_samples * 100
        label_dist[label] = {
            "count": count,
            "percentage": f"{percentage:.1f}%",
            "samples_count": len(samples_per_label[label]),
        }

    # 按频率排序
    label_dist = dict(
        sorted(label_dist.items(), key=lambda x: x[1]["count"], reverse=True)
    )

    # 只保留前 top_k 个标签
    if top_k is not None:
        label_dist = dict(list(label_dist.items())[:top_k])

    total_label_occurrences = sum(v["count"] for v in label_dist.values())

    # 获取最频繁和最不频繁的标签
    sorted_labels = sorted(all_labels.items(), key=lambda x: x[1], reverse=True)
    most_frequent = sorted_labels[:5]  # 最频繁的5个
    least_frequent = sorted_labels[-5:]  # 最不频繁的5个

    # 计算类别比例
    max_percentage = max(v["count"] / total_samples * 100 for v in label_dist.values())
    min_percentage = min(v["count"] / total_samples * 100 for v in label_dist.values())
    imbalance_ratio = (
        max_percentage / min_percentage if min_percentage > 0 else float("inf")
    )

    # 汇总统计信息
    summary = {
        "basic_stats": {
            "total_samples": total_samples,
            "unique_labels": len(label_dist),
            "avg_labels_per_sample": total_label_occurrences / total_samples,
            "is_multi_label": is_multi_label,
            "total_label_occurrences": total_label_occurrences,
        },
        "label_frequency": {
            "most_frequent": [
                {"label": label, "count": count} for label, count in most_frequent
            ],
            "least_frequent": [
                {"label": label, "count": count} for label, count in least_frequent
            ],
        },
        "distribution_stats": {
            "max_percentage": f"{max_percentage:.1f}%",
            "min_percentage": f"{min_percentage:.1f}%",
            "imbalance_ratio": f"{imbalance_ratio:.2f}",
        },
    }

    if is_multi_label:
        summary["multi_label_stats"] = {
            "max_labels_per_sample": max(label_lengths),
            "min_labels_per_sample": min(label_lengths),
            "median_labels_per_sample": sorted(label_lengths)[len(label_lengths) // 2],
            "samples_with_multiple_labels": sum(1 for x in label_lengths if x > 1),
            "samples_with_single_label": sum(1 for x in label_lengths if x == 1),
            "samples_with_no_labels": sum(1 for x in label_lengths if x == 0),
        }

    return {"distribution": label_dist, "summary": summary}


if __name__ == "__main__":
    # 测试单标签数据
    data = load_dataset("json", data_files="./testdata/data.jsonl", split="train")
    split = split_dataset(data, test_size=0.2, stratify="label")

    print("Single-label split result:", split)
    for split_type in ["train", "test"]:
        print(f"\nLabel distribution in {split_type} set:")
        print(
            json.dumps(
                analyze_label_distribution(split[split_type], "label"),
                indent=4,
                ensure_ascii=False,
            )
        )

    # 测试多标签数据
    multi_data = load_dataset(
        "json", data_files="./testdata/multilabel_data.jsonl", split="train"
    )
    split = split_dataset(multi_data, test_size=0.2, stratify="labels")

    print("\nMulti-label split result:", split)
    for split_type in ["train", "test"]:
        print(f"\nMulti-label distribution in {split_type} set:")
        print(
            json.dumps(
                analyze_label_distribution(split[split_type], "labels"),
                indent=4,
                ensure_ascii=False,
            )
        )
