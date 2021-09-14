def get_topic(string):
  from ast import literal_eval

  try:
    aux = literal_eval(str(string))
    x = aux['categories'][0]['label']
    return x.split('/')[1]

  except:
    return '9999'