import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


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
    def perform_kmeans(agg_data: pd.DataFrame, columns: list, n_clusters: int):
        cluster_data = agg_data[columns]

        # Perform k-means clustering with specified number of clusters
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        agg_data['Cluster'] = kmeans.fit_predict(cluster_data)

        return agg_data[['MSISDN/Number', 'Cluster']]

    @staticmethod
    def plot_clusters(data, x_column, y_column, cluster_column):
        plt.figure(figsize=(8, 6))
        clusters = data[cluster_column].unique()
        
        for cluster in clusters:
            cluster_data = data[data[cluster_column] == cluster]
            plt.scatter(cluster_data[x_column], cluster_data[y_column], label=f'Cluster {cluster}')
        
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'Clusters based on {x_column} vs {y_column}')
        plt.legend()
        plt.show()
