def estandarizar(numero,lista):
  min = lista.min()
  max = lista.max()
  result = (numero - min) / (max - min)
  return round(result,4)


def estandarizar_emojis(sent_emoji_pos):
  if sent_emoji_pos > 1:
    return 1
  else:
    return sent_emoji_pos


def standarize(df):
    df = df.loc[df['possitivity_ibm']!='9999']
    df['ibm_norm'] = df['possitivity_ibm'].progress_apply(lambda x: estandarizar(x, df['possitivity_ibm']))
    df['textblob_norm'] = df['possitivity_textblob'].progress_apply(lambda x: estandarizar(x, df['possitivity_textblob']))
    df['vader_norm'] = df['possitivity_vader'].progress_apply(lambda x: estandarizar(x, df['possitivity_vader']))
    df['emoji_norm'] = df['sent_emoji_pos'].progress_apply(lambda x: estandarizar_emojis(x))
    return df

    # Función que hace la media ponderada

def calc_media(textblob,vader,ibm,emojis):

  if emojis != 0:
      x_emojis = 0.44
      x_ibm = 0.25
      x_vader = 0.175
      x_textblob = 0.125

  else:
    x_emojis = 0
    x_ibm = 0.46
    x_vader = 0.31
    x_textblob = 0.23

  m = x_textblob*float(textblob) + x_ibm*float(ibm) + x_vader*float(vader) + x_emojis*float(emojis)

  return m