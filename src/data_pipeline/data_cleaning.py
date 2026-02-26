import pandas as pd
import numpy as np 

def clean_salary(salary_text):
    salary_text = salary_text.split('(')[0].replace('$', '').replace('K', '').replace(' ', '')
    try:
        if '-' in salary_text:
            low, high = salary_text.split('-')
            return (int(low) + int(high)) / 2
        return int(salary_text)
    except:
        return None

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # On filtre : on ne garde que ce qui est entre les bornes
    df_outliers_removed = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df_outliers_removed

def clean_data(df_raw):
    df = df_raw.drop(columns = ["index"]).copy()
    
    df['avg_salary'] = df['Salary Estimate'].apply(clean_salary)
    #  Remplacer les -1 par NaN 
    cols_with_minus_one = ['Rating', 'Founded', 'Size', 'Revenue', 'Sector', 'Industry','Type of ownership','Competitors']
    for col in cols_with_minus_one:
        df[col] = df[col].replace(['-1', -1], np.nan)
        if df[col].dtype == 'float64' or df[col].dtype == 'int64':
           # Si la colonne est numérique -> Médiane
           df[col] = df[col].fillna(df[col].median())
        
        
        else:
           # Sinon (si c'est un objet/string) -> Unknown
          df[col] = df[col].fillna('Unknown')
          df[col] = df[col].replace(['Unknown / Non-Applicable'], 'Unknown')
          
    df_cleaned = remove_outliers(df, 'avg_salary')
    
    return df_cleaned


if __name__ == "__main__":
    df = pd.read_csv("./data/raw/jobs.csv")
    df = clean_data(df)
    print(df.head())

    