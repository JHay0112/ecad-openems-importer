"""
This file contains an abstract class that defines an interface for accessing a PCB design. It is
expected that an implementation of this interface will be given for each method of accessing a PCB
design.

Author: J. L. Hay
"""


from abc import ABC, abstractmethod 

import os

from src.ecad_intf.layer import Layer
from src.ecad_intf.zone import Zone
from src.ecad_intf.track import Track
from src.ecad_intf.via import Via



class Board(ABC):
    """
    The definition of the interface for accesing any board.
    """


    @classmethod
    @abstractmethod
    def get_filename_extension(_) -> str:
        """
        Returns the expected filename extension.

        Returns
        -------

        str
        """
        ...


    @classmethod
    @abstractmethod
    def load_from_file(_, filename: str) -> "Board":
        """
        Loads a board from the given filename.

        Parameters
        ----------

        filename: str
            The filename containing the board.

        Returns
        -------

        Board
        """
        ...


    @abstractmethod
    def get_thickness(self) -> float:
        """
        Gets the thickness of the PCB in millimetres.

        Returns
        -------

        float
        """
        ...

    
    @abstractmethod
    def get_bounding_box(self) -> list[tuple[float, float, float]]:
        """
        Returns the bounding box around the PCB.

        Returns
        -------

        list[tuple[float, float]]
        """
        ...


    @abstractmethod
    def get_layers(self) -> list[Layer]:
        """
        Returns a list of layers.

        Returns
        -------

        list[str]
        """
        ...


    @abstractmethod
    def get_zones(self) -> list[Zone]:
        """
        Returns a list of zones.

        Returns
        -------

        list[Zone]
        """
        ...

    
    @abstractmethod
    def get_tracks(self) -> list[Track]:
        """
        Returns a list of copper tracks on the board.

        Returns
        -------

        list[Track]
        """
        ...


    @abstractmethod
    def get_vias(self) -> list[Via]:
        """
        Returns a list of vias on the board.

        Returns
        -------

        list[Via]
        """
        ...


    @classmethod
    def is_valid_file(cls, filename: str) -> bool:
        """
        Checks if the passed file is a valid.

        Parameters
        ----------

        filename: str
            The name of the file to validate.

        Returns
        -------

        bool
        """
        if not os.path.exists(filename):
            return False 
        
        _, extension = os.path.splitext(filename)
        if extension != "." + cls.get_filename_extension():
            return False 
        
        return True