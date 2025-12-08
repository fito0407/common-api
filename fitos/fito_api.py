def static_init(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls

def get_nullable_value(data,key, default):
    answer=default
    value = data.get(key)
    if value is not None:
        answer = value
    return answer

def get_nullable_value_no_default(data,key):
    answer=get_nullable_value(data,key,None)
    return answer