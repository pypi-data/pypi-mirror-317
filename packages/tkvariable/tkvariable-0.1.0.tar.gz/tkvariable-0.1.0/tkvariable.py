from __future__ import annotations

import tkinter as tk
from typing import Any, ClassVar, Callable, Literal


class TkVar:
    _instance: ClassVar[TkVar | None] = None
    
    def __new__(cls) -> TkVar:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self._master: tk.Tk | None = None
        self._variables: dict[str, tk.Variable] = {}
    
    def __getitem__(self, name: str) -> tk.Variable:
        self.__name_exists(name)
        return self._variables[name]
    
    def __setitem__(self, name: str, value: Any) -> None:
        if self._master is None:
            raise TypeError("Cannot create new variables without initializing master")
        if name not in self._variables:
            x = (self._master, value, name)
            match type(value).__name__:
                case "str":
                    self._variables[name] = tk.StringVar(*x)
                case "int":
                    self._variables[name] = tk.IntVar(*x)
                case "float":
                    self._variables[name] = tk.DoubleVar(*x)
                case "bool":
                    self._variables[name] = tk.BooleanVar(*x)
                case _:
                    raise TypeError(f"Variables only support (str, int, float and boolean) types not {type(value).__name__}")
        else:
            self._variables[name].set(value=value)
    
    @property
    def variables(self) -> dict[str, Any]:
        return {k: v.get() for k, v in self._variables.items()}
        
    def init(self, master: tk.Tk) -> TkVar:
        """"""
        self._master = master
        return self
    
    def get(self, name: str) -> tk.Variable:
        """"""
        return self[name]
    
    def set(self, name: str, value: Any) -> None:
        """"""
        self[name] = value
    
    def map(
        self,
        name: str,
        callback: Callable[[str, str, str], object],
        mode: Literal["array", "read", "write", "unset"]) -> str:
        """"""
        self.__name_exists(name)
        return self._variables[name].trace_add(mode=mode, callback=callback)
    
    def unmap(self, name: str, mode: Literal["array", "read", "write", "unset"]) -> None:
        """"""
        self.__name_exists(name)
        self._variables[name].trace_remove(mode, name)
    
    def __name_exists(self, name: str) -> None:
        """"""
        if name not in self._variables:
            raise ValueError(f"Variable {name} bot found")


variable: TkVar = TkVar()
