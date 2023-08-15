class Singleton:
    __instanse = None

    def __new__(cls, *args, **kwargs):
        if cls.__instanse is None:
            cls.__instanse = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instanse