from typing import List, Tuple
from Mongy import MongoDB
from check_point import is_point_inside


class MAP:
    def __init__(self):
        """
        Initialize the MAP object, which keeps track of affected and unaffected regions.
        """
        self.affected_regions = []  
        self.db_object = MongoDB("EMS", "MAP")

    def check_in_region(self, location: Tuple[int,int]):
        """
        Check if a given location is inside an affected region.
        :param location: Tuple (latitude, longitude).
        :return: "Affected" if inside, "Unaffected" otherwise.
        """
        if location in self.affected_regions:  
            return 1
        return 0
        
    def _load_affected_regions(self):
        """
        Load affected regions from MongoDB at initialization.
        """
        data = self.db_object.find({})
        self.affected_regions = data.get("affected_regions", []) if data else []

    def add_affected_region(self, region: Tuple[Tuple[int, int], Tuple[int, int]]):
        """
        Add a new affected region defined by boundary coordinates.
        :param region: A tuple containing two points (top-left, bottom-right) defining a rectangular region.
        """
        self.affected_regions.append(region)
        self.db_object.update_one({}, {"$set": {"affected_regions": self.affected_regions}}, upsert=True)
    
    def remove_affected_region(self, region: Tuple[Tuple[int, int], Tuple[int, int]]):
        """
        Remove an affected region.
        """
        if region in self.affected_regions:
            self.affected_regions.remove(region)
            self.db_object.update_one({}, {"$set": {"affected_regions": self.affected_regions}}, upsert=True)
    
    def check_in_region(self, location: Tuple[int, int]) -> str:
        """
        Check if a given location lies inside any affected region.
        :param location: A tuple (latitude, longitude) to check.
        :return: "Affected" if inside a region, else "Unaffected".
        """
        x, y = location
        for region in self.affected_regions:
            (x1, y1), (x2, y2) = region  
            if x1 <= x <= x2 and y1 <= y <= y2:
                return "Affected"
        return "Unaffected"
    
    def get_affected_regions(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Return a list of all affected regions.
        """
        return self.affected_regions
    
    def __repr__(self):
        return f"MAP(Affected Regions={self.affected_regions})"
