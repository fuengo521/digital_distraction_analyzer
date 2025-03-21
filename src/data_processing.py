import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(filepath):
    # Loads the data from the CSV and performs initial cleaning
    
    df = pd.read_csv(filepath)
    df = df.drop_duplicates()
    
    # Standardize
    df['Gender'] = df['Gender'].str.strip().str.title()
    df['Location'] = df['Location'].str.strip().str.title()
    df['Profession'] = df['Profession'].str.strip().str.title()
    df['Demographics'] = df['Demographics'].str.strip().str.title()
    df['Platform'] = df['Platform'].str.strip().str.title()
    df['Video Category'] = df['Video Category'].str.strip().str.title()
    df['Frequency'] = df['Frequency'].str.strip().str.title()
    df['Watch Reason'] = df['Watch Reason'].str.strip().str.title()
    df['DeviceType'] = df['DeviceType'].str.strip().str.title()
    df['OS'] = df['OS'].str.strip().str.title()
    df['CurrentActivity'] = df['CurrentActivity'].str.strip().str.title()
    df['ConnectionType'] = df['ConnectionType'].str.strip().str.title()
    
    # Fix typo: replace "Barzil" with "Brazil" in Location
    df['Location'] = df['Location'].str.replace("Barzil", "Brazil", case=False)
    
    # Convert booleans to integers
    df['Debt'] = df['Debt'].astype(int)
    df['Owns Property'] = df['Owns Property'].astype(int)
    
    # Convert Watch Time to datetime
    df['Watch Time'] = pd.to_datetime(df['Watch Time'], format='%I:%M %p', errors='coerce')
    df['Watch Hour'] = df['Watch Time'].dt.hour
    df['Watch Time'] = df['Watch Time'].dt.time
    
    # Feature Engineering
    df['Time per Session'] = (df['Total Time Spent'] / df['Number of Sessions']).round(2)
    df['Engagement Efficiency'] = (df['Engagement'] / df['Total Time Spent']).round(3)
    df['Videos per Session'] = (df['Number of Videos Watched'] / df['Number of Sessions']).round(2)
    df['Video Consumption Ratio'] = (df['Time Spent On Video'] / df['Total Time Spent']).round(3)
    
    # Categorize Watch Hour into parts of day
    def categorize_hour(hour):
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    df['Time of Day'] = df['Watch Hour'].apply(categorize_hour)
    
    return df

def scale_features(df, features_to_scale):
    # Standardizes some features
    
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[features_to_scale] = scaler.fit_transform(df[features_to_scale])
    return df_scaled

def transform_skewed_features(df, skewed_features):
    # log tranformations to reduce skew
    # small constant to avoid log(0)
    
    for col in skewed_features:
        df[f'{col}_log'] = np.log(df[col] + 1)
    return df

def export_data(df_clean, df_scaled, processed_dir):
    # Export cleaned and scaled data
    
    os.makedirs(processed_dir, exist_ok=True)
    clean_path = os.path.join(processed_dir, "data_clean.csv")
    scaled_path = os.path.join(processed_dir, "data_scaled.csv")
    
    df_clean.to_csv(clean_path, index=False)
    df_scaled.to_csv(scaled_path, index=False)
    
    print(f"Exported clean data to: {clean_path}")
    print(f"Exported scaled data to: {scaled_path}")

def main():
    # Assuming the script is run from the 'src' directory, 
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_data_path = os.path.join(project_root, 'data', 'raw', 'Time-Wasters on Social Media.csv')
    processed_dir = os.path.join(project_root, 'data', 'processed')
    
    print("Project root:", project_root)
    print("Raw data path:", raw_data_path)
    print("Processed directory:", processed_dir)
    
    df = load_and_clean_data(raw_data_path)
    print("Data loaded and cleaned. Shape:", df.shape)
    
    features_to_scale = [
        'Age', 
        'Income', 
        'Total Time Spent', 
        'Time per Session', 
        'Engagement Efficiency', 
        'Videos per Session', 
        'Video Consumption Ratio'
    ]
    df_scaled = scale_features(df, features_to_scale)
    print("Summary statistics for scaled features:")
    print(df_scaled[features_to_scale].describe())

    skewed_features = [
        'Time per Session',
        'Engagement Efficiency',
        'Videos per Session',
        'Video Consumption Ratio'
    ]
    df_scaled = transform_skewed_features(df_scaled, skewed_features)
    
    export_data(df, df_scaled, processed_dir)

if __name__ == "__main__":
    main()
