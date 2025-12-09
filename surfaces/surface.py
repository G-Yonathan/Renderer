from abc import ABC, abstractmethod


class Surface(ABC):
    @abstractmethod
    def find_intersection(self, ray, source):
        pass

    @abstractmethod
    def get_normal(self, point):
        # Assumes point is on surface
        pass
