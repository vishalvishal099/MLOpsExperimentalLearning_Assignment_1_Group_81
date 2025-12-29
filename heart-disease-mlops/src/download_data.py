"""
Script to download and prepare the Heart Disease dataset from UCI ML Repository
"""
import os
import shutil
import pandas as pd
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Create directories
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_dataset():
    """
    Download heart disease dataset from local source
    
    The dataset is available at:
    - Local: raw_dataSet/heart+disease (within project directory)
    - Web: https://archive.ics.uci.edu/dataset/45/heart+disease
    """
    
    print("=" * 80)
    print("Heart Disease Dataset Download Script")
    print("=" * 80)
    
    # Source path (within project directory)
    source_path = BASE_DIR / "raw_dataSet" / "heart+disease"
    
    if source_path.exists():
        print(f"\n✓ Found local dataset at: {source_path}")
        
        # Copy relevant files
        files_to_copy = [
            "processed.cleveland.data",
            "cleveland.data",
            "heart-disease.names"
        ]
        
        for filename in files_to_copy:
            src = source_path / filename
            if src.exists():
                dst = RAW_DATA_DIR / filename
                shutil.copy2(src, dst)
                print(f"  ✓ Copied: {filename}")
        
        print("\n✓ Dataset files copied successfully!")
        
    else:
        print("\n⚠ Local dataset not found.")
        print("\nPlease download the dataset manually from:")
        print("https://archive.ics.uci.edu/dataset/45/heart+disease")
        print(f"\nAnd place the files in: {RAW_DATA_DIR}")
        return False
    
    return True

def load_and_prepare_data():
    """
    Load the Cleveland dataset (most commonly used) and prepare it
    """
    print("\n" + "=" * 80)
    print("Preparing Dataset")
    print("=" * 80)
    
    # Column names based on UCI documentation
    column_names = [
        'age',           # Age in years
        'sex',           # Sex (1 = male; 0 = female)
        'cp',            # Chest pain type (1-4)
        'trestbps',      # Resting blood pressure (mm Hg)
        'chol',          # Serum cholesterol (mg/dl)
        'fbs',           # Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
        'restecg',       # Resting ECG results (0-2)
        'thalach',       # Maximum heart rate achieved
        'exang',         # Exercise induced angina (1 = yes; 0 = no)
        'oldpeak',       # ST depression induced by exercise
        'slope',         # Slope of peak exercise ST segment (1-3)
        'ca',            # Number of major vessels colored by fluoroscopy (0-3)
        'thal',          # Thalassemia (3 = normal; 6 = fixed defect; 7 = reversible defect)
        'target'         # Heart disease diagnosis (0 = no disease, 1-4 = disease)
    ]
    
    # Load the processed Cleveland data
    data_file = RAW_DATA_DIR / "processed.cleveland.data"
    
    if not data_file.exists():
        print(f"\n✗ Error: {data_file} not found!")
        print("Please run the download step first.")
        return None
    
    # Read the data
    df = pd.read_csv(data_file, names=column_names, na_values='?')
    
    print(f"\n✓ Loaded dataset with {len(df)} records and {len(df.columns)} features")
    print(f"  - Shape: {df.shape}")
    print(f"  - Missing values: {df.isnull().sum().sum()}")
    
    # Convert target to binary (0 = no disease, 1 = disease present)
    df['target'] = (df['target'] > 0).astype(int)
    
    print(f"\n✓ Converted target to binary classification:")
    print(f"  - Class 0 (No disease): {(df['target'] == 0).sum()} samples")
    print(f"  - Class 1 (Disease): {(df['target'] == 1).sum()} samples")
    
    # Save processed data
    output_file = PROCESSED_DATA_DIR / "heart_disease.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved processed data to: {output_file}")
    
    # Create data dictionary
    data_dict = """
# Heart Disease Dataset - Data Dictionary

## Features (13 predictors + 1 target)

### Demographic Features:
- **age**: Age in years (continuous)
- **sex**: Sex (1 = male; 0 = female)

### Clinical Measurements:
- **trestbps**: Resting blood pressure in mm Hg (continuous)
- **chol**: Serum cholesterol in mg/dl (continuous)
- **fbs**: Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
- **thalach**: Maximum heart rate achieved (continuous)

### Chest Pain & Exercise:
- **cp**: Chest pain type (1-4)
  - 1: Typical angina
  - 2: Atypical angina
  - 3: Non-anginal pain
  - 4: Asymptomatic
- **exang**: Exercise induced angina (1 = yes; 0 = no)
- **oldpeak**: ST depression induced by exercise relative to rest (continuous)

### ECG Results:
- **restecg**: Resting electrocardiographic results (0-2)
  - 0: Normal
  - 1: ST-T wave abnormality
  - 2: Left ventricular hypertrophy
- **slope**: Slope of peak exercise ST segment (1-3)
  - 1: Upsloping
  - 2: Flat
  - 3: Downsloping

### Cardiac Tests:
- **ca**: Number of major vessels colored by fluoroscopy (0-3)
- **thal**: Thalassemia (3, 6, 7)
  - 3: Normal
  - 6: Fixed defect
  - 7: Reversible defect

### Target Variable:
- **target**: Heart disease diagnosis (binary)
  - 0: No disease (< 50% diameter narrowing)
  - 1: Disease present (> 50% diameter narrowing)

## Missing Values:
- Represented as '?' in raw data
- Primarily in 'ca' and 'thal' features

## Dataset Source:
- UCI Machine Learning Repository
- Cleveland Clinic Foundation database (most commonly used)
- 303 instances in Cleveland dataset
"""
    
    dict_file = DATA_DIR / "DATA_DICTIONARY.md"
    with open(dict_file, 'w') as f:
        f.write(data_dict)
    print(f"✓ Created data dictionary: {dict_file}")
    
    return df

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("HEART DISEASE DATASET PREPARATION")
    print("=" * 80)
    
    # Step 1: Download dataset
    if download_dataset():
        # Step 2: Prepare dataset
        df = load_and_prepare_data()
        
        if df is not None:
            print("\n" + "=" * 80)
            print("✓ DATASET PREPARATION COMPLETE!")
            print("=" * 80)
            print(f"\nProcessed data available at:")
            print(f"  {PROCESSED_DATA_DIR / 'heart_disease.csv'}")
            print(f"\nYou can now proceed with EDA and model training.")
            print("=" * 80 + "\n")
    else:
        print("\n✗ Dataset preparation failed!")

if __name__ == "__main__":
    main()
