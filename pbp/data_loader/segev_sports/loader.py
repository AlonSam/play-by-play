import requests

from pbp.data_loader.abs_data_loader import AbsDataLoader


class SegevLoader(AbsDataLoader):
    """
    Base class for loading data from segev_sports API
    This class should not be instantiated directly.
    """
    def _load_request_data(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            self.source_data = response.json()
            return self.source_data
        else:
            response.raise_for_status()

    @property
    def data(self):
        return self.source_data