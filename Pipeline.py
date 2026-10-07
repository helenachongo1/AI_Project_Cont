import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib  

# Data_Sample
data = {
    "Name": ["Jenny", "Elisabeth", "Erick", "Paul", "Johanna", "John", "Harry", "Litho"],
    "Age": [23, 34, 25, None, 35, 36, None, 22],
    "Gender": ["F", "F", "M", "M", "F", "M", "M", "M"],
    "Job": ["Writer", "Programmer", "Doctor", "Programmer", "Teacher", "Cook", "Dentist", "Engineer"]
}

df = pd.DataFrame(data)

# Define columns to process
numerical_cols = ['Age']
categorical_cols = ['Gender', 'Job']

# Numerical pipeline
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
cat_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combine into full pipeline
full_pipeline = ColumnTransformer(transformers=[
    ('num', num_pipeline, numerical_cols),
    ('cat', cat_pipeline, categorical_cols)
])

# Fit-transform the DataFrame (corrected line)
transformed_data = full_pipeline.fit_transform(df)

# Save transformed output
pd.DataFrame(
    transformed_data.toarray() if hasattr(transformed_data, 'toarray') else transformed_data
).to_csv('transformed_data.csv', index=False)

# Save the pipeline
joblib.dump(full_pipeline, 'preprocessing_pipeline.pkl')

print("ETL process completed and data saved.")
