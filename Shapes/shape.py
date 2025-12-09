from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def find_itersection(ray):
        pass
