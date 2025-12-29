
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
