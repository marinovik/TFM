# Copiado de limpieza uber.ipynb (ubicado en collab)

def drop_unnamed(df):
    try:
        df = df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1)
    except:
        pass
    return df

def drop_cols_wo_value(df, cols=['user_ verified','user_withheld_in_countries','finished_tweet', 'created_at_time']):
    df = df.drop(cols, axis=1)
    return df

def num_cols_treatment(df, num_cols):
    # Limpio todas las variables salvo created_at_hour eliminando outliers
    for variable in num_cols:
        if variable != 'user_id':

            mean = df[variable].mean()
            std = df[variable].std()
            outlier = mean + (std * 1.5)

            aux = df[variable].loc[df[variable] >= outlier].count()
            pctg = (aux/df.shape[0])*100
            pctg = round(pctg,2)

            # Recategorizo
            df[variable] = df[variable].apply(lambda x: mean if x >= outlier else x)
    return df
    

# Modifico is_reply de forma simple
def is_reply_treat(df):
    cond1 = df['is_reply'].isin(['No','Uber_Support','Uber'])
    df['is_reply'] = df['is_reply'].where(cond1,'Si')
    cond2 = df['is_reply'].isin(['Si','No','Uber'])
    df['is_reply'] = df['is_reply'].where(cond2,'Uber')
    return df

# tratamos source_device
def source_device_treat(df):
    df.loc[df['source_device'] == 'Twitter for iPhone', 'source_device'] = 'Apple'
    df.loc[df['source_device'] == 'Twitter for iPad', 'source_device'] = 'Apple' 
    df.loc[df['source_device'] == 'Twitter Web App', 'source_device'] = 'Web_app' 
    df.loc[df['source_device'] == 'TweetDeck', 'source_device'] = 'Web_app' 
    df.loc[df['source_device'] == 'Twitter for Android', 'source_device'] = 'Android'
    cond3 = df['source_device'].isin(['Apple','Web_app','Android','Sprinklr'])
    df['source_device'] = df['source_device'].where(cond3,'Otro')
    return df

