import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


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

    @staticmethod
    def perform_kmeans(self, agg_data: pd.DataFrame, columns: list, n_clusters: int):
        cluster_data = agg_data[columns]

        # Perform k-means clustering with specified number of clusters
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        agg_data['Cluster'] = kmeans.fit_predict(cluster_data)

        return agg_data[['MSISDN/Number', 'Cluster']]
