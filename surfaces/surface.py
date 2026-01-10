from abc import ABC, abstractmethod


class Surface(ABC):
    
    def __init__(self, material_index):
        self.material_index = material_index

    @abstractmethod
    def find_intersection(self, ray, source):
        pass

    @abstractmethod
    def get_normal(self, point):
        # Assumes point is on surface
        pass
