from abc import ABC, abstractmethod
from typing import List
from .models import ConnectivityData

class ConnectivityRepository(ABC):
    @abstractmethod
    def get_connectivity_data(self, log_file_path: str) -> List[ConnectivityData]:
        """Retrieve connectivity data from a log file."""
        pass 