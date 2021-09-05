# Copiado de limpieza uber.ipynb (ubicado en collab)

def change_types(df):
    # Pasamos a str las que creemos convenientes
    df["text"] = str(df["text"])
    df["user_name"] = str(df["user_name"])
    df["user_location"] = str(df["user_location"])
    df["source_device"] = str(df["source_device"])
    # Pasamos a factor las variables binarias
    df['retweeted'] = df['retweeted'].astype('category')
    df['finished_tweet'] = df['finished_tweet'].astype('category')
    return df

# Outliers
def outliers_treatment(df, col):
    mean = df[col].mean()
    std = df[col].std()
    outlier = mean + (std* 1.5)
    df[col] = df.user_friends.apply(lambda x: 9999999 if x>=outlier else x)
    return df


def outliers_full_treatment(df, cols):
    cols_to_remove_outliers = ["user_friends", "user_followers", "hastags_in_tweet", "status_count", 
                               "mentions_in_tweet", "favorite_count", "retweet_count"]
    for col in cols_to_remove_outliers:
        df = outliers_treatment(df, col)
    return df

# Tratamiento variables categóricas
