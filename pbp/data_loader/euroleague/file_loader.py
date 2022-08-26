import json
from pathlib import Path

from pbp.data_loader.abs_data_loader import AbsDataLoader


class ELFileLoader(AbsDataLoader):
    """
    Base class for loading Euroleague files saved on disk.
    This class should not be instantiated directly.
    """
    def _load_data_from_file(self):
        data_file = Path(self.file_path)
        if not data_file.is_file():
            raise Exception(f'{self.file_path} does not exist')
        with open(self.file_path) as json_data:
            self.source_data = json.load(json_data)

    @property
    def data(self):
        return self.source_data