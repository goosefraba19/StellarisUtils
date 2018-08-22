def getitem_or_default(dict,key,default):
    if key in dict:
        return dict[key]
    else:
        return default
