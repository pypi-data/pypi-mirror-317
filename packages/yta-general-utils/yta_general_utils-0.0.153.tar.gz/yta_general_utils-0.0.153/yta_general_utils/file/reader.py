from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.parameter_validator import PythonValidator

import json


class FileReader:
    """
    Class to simplify and encapsulate the functionality related
    with reading files.
    """
    @staticmethod
    def read_json(filename: str):
        """
        Reads the provided 'filename' and returns the information 
        as a json (if possible).

        Parameters
        ----------
        filename : str
            File path from which we want to read the information.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.file_exists(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        with open(filename, encoding = 'utf-8') as json_file:
            return json.load(json_file)
        
    @staticmethod
    def read_lines(filename: str):
        """
        Read the content of the provided 'filename'
        if valid and return it as it decomposed in
        lines.

        Parameters
        ----------
        filename : str
            File path from which we want to read the information.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.file_exists(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        with open(filename, 'r', encoding = 'utf-8') as file:
            return file.readlines()
        
    @staticmethod
    def read(filename: str):
        """
        Read the content of the provided 'filename'
        if valid and return it as it is.

        Parameters
        ----------
        filename : str
            File path from which we want to read the information.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.file_exists(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        with open(filename, 'r', encoding = 'utf-8') as file:
            return file.read()
