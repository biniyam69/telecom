import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class Helpers:
    @staticmethod
    def normalize(df, columns):
        scaler = StandardScaler()
        df_normalized = df.copy()
        df_normalized[columns] = scaler.fit_transform(df_normalized[columns])
        return df_normalized

    @staticmethod
    def reduce(df):
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        numerical_columns = numerical_columns.drop('MSISDN/Number', axis=1)
        numerical_data = df[numerical_columns]
        numerical_data = numerical_data.dropna()

        scaler = StandardScaler()
        numerical_data = scaler.fit_transform(numerical_data)

        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(numerical_data)
        pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
        final_df = pd.concat([df, pca_df], axis=1)
        return final_df


