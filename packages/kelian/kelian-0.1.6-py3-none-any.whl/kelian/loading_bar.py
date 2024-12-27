from types import NoneType

class ProgressBar():
    def __init__(self, total:int, current:int=0, length:int=50) -> None:
        self.total:int   = total
        self.current:int = current
        self.length:int  = length
        self.pattern:list[str, str, str, str, bool] = ["[", "=", ".", "]", True]

    def format(self, start_side:str=None, full:str=None, empty:str=None, end_side:str=None, percent:bool=None) -> None:
        assert isinstance(start_side, (str, NoneType)), "'start_side' is not of type string"
        assert isinstance(full, (str, NoneType)), "'full' is not of type string"
        assert isinstance(empty, (str, NoneType)), "'empty' is not of type string"
        assert isinstance(end_side, (str, NoneType)), "'end_side' is not of type string"
        assert isinstance(percent, (bool, NoneType)), "'percent' is not of type boolean"

        self.pattern = [
            start_side if start_side is not None else self.pattern[0], 
            full if full is not None else self.pattern[1], 
            empty if empty is not None else self.pattern[2], 
            end_side if end_side is not None else self.pattern[3], 
            percent if percent is not None else self.pattern[4]
        ]

    def display(self, update:bool=False) -> str:
        if update:
            self.current += 1

        full_bar_value = (self.length*self.current) // self.total

        result = self.pattern[0]
        result += self.pattern[1] * full_bar_value
        result += self.pattern[2] * (self.length - full_bar_value)
        result += self.pattern[3]

        if self.pattern[4]: # if percent
            result += " "
            percent_value = round((100*self.current)/self.total, 1)
            result += ' '*(5-len(str(percent_value)))
            result += str(percent_value)
            result += "%"

        return result

    def __str__(self) -> str:
        return self.display(True)
