import time

class Review:
    def __init__(self, rating: int, comment: str) -> None:
        self.__rating = rating
        self.__comment = comment
        self.__time = time.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def rating(self) -> int:
        return self.__rating
    
    @property
    def comment(self) -> str:
        return self.__comment
    
    @property
    def time(self) -> str:
        return self.__time
