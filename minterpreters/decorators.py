def function_details(func):
    def show_name(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return show_name