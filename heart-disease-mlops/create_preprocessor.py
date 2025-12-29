"""Create preprocessor for the API"""
from src.preprocessing import HeartDiseasePreprocessor
from sklearn.model_selection import train_test_split
import joblib

# Create and fit preprocessor
preprocessor = HeartDiseasePreprocessor()
data = preprocessor.load_data('data/processed/heart_disease.csv')

# Split data
X = data.drop('target', axis=1)
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit preprocessor
X_train_processed = preprocessor.fit_transform(X_train)

# Save preprocessor
joblib.dump(preprocessor, 'models/preprocessor.pkl')
print('✓ Preprocessor saved to models/preprocessor.pkl')
