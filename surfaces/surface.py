from abc import ABC, abstractmethod


class Surface(ABC):
    @abstractmethod
    def find_intersection(self, ray):
        pass

    @abstractmethod
    def normal(self, point):
        pass
