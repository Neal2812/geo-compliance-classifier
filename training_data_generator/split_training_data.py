#!/usr/bin/env python3
"""
Automated Training/Testing/Validation Split for Geo-Compliance Classifier
Processes the corrections.json data and creates ML-ready datasets.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DatasetSplitter:
    """Handles splitting corrections data into train/test/validation sets."""

    def __init__(self, corrections_file: str = "active_learning_data/corrections.json"):
        self.corrections_file = corrections_file
        self.data = None
        self.splits = {}

    def load_corrections(self) -> pd.DataFrame:
        """Load and process corrections data."""
        logger.info(f"Loading corrections from {self.corrections_file}")

        with open(self.corrections_file, "r") as f:
            corrections = json.load(f)

        # Convert to DataFrame for easier processing
        processed_data = []
        for correction in corrections:
            record = {
                "case_id": correction["case_id"],
                "timestamp": correction["timestamp"],
                "original_prediction": correction["original_prediction"],
                "corrected_label": correction["corrected_label"],
                "reviewer_reasoning": correction["reviewer_reasoning"],
                "confidence_score": correction["confidence_score"],
                "model_used": correction["model_used"],
                "correction_type": correction["correction_type"],
                "impact_score": correction["impact_score"],
                # Extract geographic features
                "state": correction["feature_characteristics"]["geographic"].get(
                    "state", "Unknown"
                ),
                "country": correction["feature_characteristics"]["geographic"].get(
                    "country", "Unknown"
                ),
                "region": correction["feature_characteristics"]["geographic"].get(
                    "region", "Unknown"
                ),
                # Extract demographic features
                "age_min": correction["feature_characteristics"]["demographic"].get(
                    "age_min", 0
                ),
                "age_max": correction["feature_characteristics"]["demographic"].get(
                    "age_max", 100
                ),
                # Extract regulation info
                "regulation_type": correction["feature_characteristics"].get(
                    "regulation_type", "Unknown"
                ),
                "feature_type": correction["feature_characteristics"].get(
                    "feature_type", "Unknown"
                ),
            }
            processed_data.append(record)

        self.data = pd.DataFrame(processed_data)
        logger.info(f"Processed {len(self.data)} correction records")

        return self.data

    def analyze_data_distribution(self) -> Dict[str, Any]:
        """Analyze the distribution of corrections data."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_corrections() first.")

        analysis = {
            "total_records": len(self.data),
            "correction_types": self.data["correction_type"].value_counts().to_dict(),
            "models_used": self.data["model_used"].value_counts().to_dict(),
            "original_predictions": self.data["original_prediction"]
            .value_counts()
            .to_dict(),
            "corrected_labels": self.data["corrected_label"].value_counts().to_dict(),
            "regulation_types": self.data["regulation_type"].value_counts().to_dict(),
            "geographic_distribution": {
                "states": self.data["state"].value_counts().to_dict(),
                "countries": self.data["country"].value_counts().to_dict(),
                "regions": self.data["region"].value_counts().to_dict(),
            },
            "confidence_stats": {
                "mean": float(self.data["confidence_score"].mean()),
                "std": float(self.data["confidence_score"].std()),
                "min": float(self.data["confidence_score"].min()),
                "max": float(self.data["confidence_score"].max()),
            },
        }

        return analysis

    def create_splits(
        self,
        train_ratio: float = 0.7,
        test_ratio: float = 0.2,
        val_ratio: float = 0.1,
        stratify_column: str = "corrected_label",
        random_state: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        """Create stratified train/test/validation splits."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_corrections() first.")

        if not abs(train_ratio + test_ratio + val_ratio - 1.0) < 1e-6:
            raise ValueError("Train, test, and validation ratios must sum to 1.0")

        logger.info(
            f"Creating splits: {train_ratio:.1%} train, {test_ratio:.1%} test, {val_ratio:.1%} validation"
        )

        # Check if we have enough data for stratified splitting
        label_counts = self.data[stratify_column].value_counts()
        min_class_size = label_counts.min()

        if min_class_size < 2 or len(self.data) < 10:
            logger.warning(
                "Dataset too small for stratified splitting. Using random split."
            )
            # Use simple random split for small datasets
            train_data, temp_data = train_test_split(
                self.data, test_size=(test_ratio + val_ratio), random_state=random_state
            )

            # Second split: separate test from val
            relative_test_size = test_ratio / (test_ratio + val_ratio)
            test_data, val_data = train_test_split(
                temp_data, test_size=(1 - relative_test_size), random_state=random_state
            )
        else:
            # Use stratified split for larger datasets
            # First split: separate train from test+val
            train_data, temp_data = train_test_split(
                self.data,
                test_size=(test_ratio + val_ratio),
                stratify=self.data[stratify_column],
                random_state=random_state,
            )

            # Second split: separate test from val
            relative_test_size = test_ratio / (test_ratio + val_ratio)
            test_data, val_data = train_test_split(
                temp_data,
                test_size=(1 - relative_test_size),
                stratify=temp_data[stratify_column],
                random_state=random_state,
            )

        self.splits = {"train": train_data, "test": test_data, "validation": val_data}

        # Log split statistics
        for split_name, split_data in self.splits.items():
            logger.info(f"{split_name.capitalize()} set: {len(split_data)} records")
            label_dist = split_data[stratify_column].value_counts()
            logger.info(f"  Label distribution: {label_dist.to_dict()}")

        return self.splits

    def save_splits(self, output_dir: str = "active_learning_data/splits"):
        """Save the train/test/validation splits to separate files."""
        if not self.splits:
            raise ValueError("Splits not created. Call create_splits() first.")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for split_name, split_data in self.splits.items():
            # Save as JSON (preserves structure)
            json_file = output_path / f"{split_name}.json"
            split_data.to_json(json_file, orient="records", indent=2)

            # Save as CSV (easier for analysis)
            csv_file = output_path / f"{split_name}.csv"
            split_data.to_csv(csv_file, index=False)

            logger.info(f"Saved {split_name} set to {json_file} and {csv_file}")

    def generate_training_features(self) -> Dict[str, pd.DataFrame]:
        """Generate ML-ready feature matrices for training."""
        if not self.splits:
            raise ValueError("Splits not created. Call create_splits() first.")

        feature_sets = {}

        for split_name, split_data in self.splits.items():
            # Create feature matrix
            features = pd.DataFrame(
                {
                    # Categorical features (will need encoding)
                    "original_prediction": split_data["original_prediction"],
                    "model_used": split_data["model_used"],
                    "state": split_data["state"],
                    "country": split_data["country"],
                    "region": split_data["region"],
                    "regulation_type": split_data["regulation_type"],
                    "feature_type": split_data["feature_type"],
                    # Numerical features
                    "confidence_score": split_data["confidence_score"],
                    "impact_score": split_data["impact_score"],
                    "age_min": split_data["age_min"],
                    "age_max": split_data["age_max"],
                    "age_range": split_data["age_max"] - split_data["age_min"],
                    # Target variable
                    "target": split_data["corrected_label"],
                }
            )

            feature_sets[split_name] = features

        return feature_sets

    def generate_report(self) -> str:
        """Generate a comprehensive analysis report."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_corrections() first.")

        analysis = self.analyze_data_distribution()

        report = f"""# Geo-Compliance Classifier Dataset Analysis Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview

- **Total Records**: {analysis['total_records']}
- **Unique Cases**: {self.data['case_id'].nunique()}
- **Date Range**: {self.data['timestamp'].min()} to {self.data['timestamp'].max()}

## Correction Type Distribution

{pd.Series(analysis['correction_types']).to_string()}

## Model Performance Analysis

### Models Generating Corrections
{pd.Series(analysis['models_used']).to_string()}

### Original vs Corrected Predictions
- **Original Predictions**: {analysis['original_predictions']}
- **Corrected Labels**: {analysis['corrected_labels']}

## Regulation Type Analysis

{pd.Series(analysis['regulation_types']).to_string()}

## Geographic Distribution

### By State
{pd.Series(analysis['geographic_distribution']['states']).to_string()}

### By Country  
{pd.Series(analysis['geographic_distribution']['countries']).to_string()}

### By Region
{pd.Series(analysis['geographic_distribution']['regions']).to_string()}

## Confidence Score Statistics

- **Mean**: {analysis['confidence_stats']['mean']:.3f}
- **Standard Deviation**: {analysis['confidence_stats']['std']:.3f}
- **Range**: {analysis['confidence_stats']['min']:.3f} - {analysis['confidence_stats']['max']:.3f}

## Split Information

"""
        if self.splits:
            for split_name, split_data in self.splits.items():
                report += f"### {split_name.capitalize()} Set\n"
                report += f"- **Size**: {len(split_data)} records ({len(split_data)/len(self.data):.1%})\n"
                label_dist = split_data["corrected_label"].value_counts()
                report += f"- **Label Distribution**: {label_dist.to_dict()}\n\n"

        return report


def main():
    """Main execution function."""
    logger.info("Starting dataset splitting process")

    # Initialize splitter
    splitter = DatasetSplitter()

    # Load and analyze data
    data = splitter.load_corrections()
    analysis = splitter.analyze_data_distribution()

    logger.info("Dataset Analysis:")
    logger.info(f"  Total records: {analysis['total_records']}")
    logger.info(f"  Regulation types: {list(analysis['regulation_types'].keys())}")
    logger.info(
        f"  Geographic coverage: {len(analysis['geographic_distribution']['countries'])} countries"
    )

    # Create splits
    splits = splitter.create_splits(
        train_ratio=0.7,
        test_ratio=0.2,
        val_ratio=0.1,
        stratify_column="corrected_label",
    )

    # Save splits
    splitter.save_splits()

    # Generate feature matrices
    feature_sets = splitter.generate_training_features()

    # Save feature matrices
    feature_dir = Path("active_learning_data/features")
    feature_dir.mkdir(parents=True, exist_ok=True)

    for split_name, features in feature_sets.items():
        feature_file = feature_dir / f"{split_name}_features.csv"
        features.to_csv(feature_file, index=False)
        logger.info(f"Saved {split_name} features to {feature_file}")

    # Generate and save report
    report = splitter.generate_report()
    report_file = Path("active_learning_data") / "dataset_analysis_report.md"

    with open(report_file, "w") as f:
        f.write(report)

    logger.info(f"Generated analysis report: {report_file}")
    logger.info("Dataset splitting process completed successfully!")

    return splitter, splits, feature_sets


if __name__ == "__main__":
    splitter, splits, feature_sets = main()
