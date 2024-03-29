from abc import ABC, abstractmethod
from functools import reduce
from typing import TypeVar, Generic, AbstractSet, Optional, Tuple, Dict, Any, Sequence

StateType = TypeVar("StateType")
SymbolType = TypeVar("SymbolType")
GuardType = TypeVar("GuardType")
TransitionType = Tuple[StateType, GuardType, StateType]

