def singleton(cls):
    """
    Decorator to create a singleton instance of a class.
    """
    instances = {}
    print(f"Creating singleton instance of {cls.__name__}")
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance
