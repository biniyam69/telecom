from sklearn.preprocessing import StandardScaler


class Helpers:
    @staticmethod
    def normalize(df, columns):
        scaler = StandardScaler()
        df_normalized = df.copy()
        df_normalized[columns] = scaler.fit_transform(df_normalized[columns])
        return df_normalized

#%%
