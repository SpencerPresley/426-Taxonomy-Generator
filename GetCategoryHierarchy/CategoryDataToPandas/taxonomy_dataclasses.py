from dataclasses import dataclass
from typing import List

@dataclass
class DetailedCategory:
    name: str
    
    def to_dict(self):
        return self.name  # Return just the name as a string

@dataclass
class MajorCategory:
    name: str
    detailed_categories: List[DetailedCategory]
    
    def to_dict(self):
        return {
            self.name: [detailed.to_dict() for detailed in self.detailed_categories]
        }

@dataclass
class BroadCategory:
    name: str
    inner_categories: List[MajorCategory]
    
    def to_dict(self):
        return {
            self.name: {major.name: major.to_dict()[major.name] for major in self.inner_categories}
        }

@dataclass
class AreaCategory:
    name: str
    broad_categories: List[BroadCategory]
    
    def to_dict(self):
        return {
            self.name: {broad.name: broad.to_dict()[broad.name] for broad in self.broad_categories}
        }

@dataclass
class CategoryHierarchy:
    area_categories: List[AreaCategory]
    
    def to_dict(self):
        return {area.name: area.to_dict()[area.name] for area in self.area_categories}
    