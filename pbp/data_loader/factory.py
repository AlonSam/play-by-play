"""
``DataLoaderFactory`` can be used to create data loader objects from the ``data_loader`` module.
"""

from collections import defaultdict

import pbp.data_loader as data_loader


class DataLoaderFactory(object):
    """
    Class for factory of data loader classes. On initialization will load in all data loader classes in ``data_loader`` module
    """

    def __init__(self):
        self.loaders = defaultdict(lambda: defaultdict(lambda: []))
        self._load_data_loaders()

    def _load_data_loaders(self):
        """
        loads data loaders from data_loader package
        """
        loaders = dict(
            [
                (name, cls)
                for name, cls in data_loader.__dict__.items()
                if isinstance(cls, type)
            ]
        )
        for name, loader_cls in loaders.items():
            if hasattr(loader_cls, "resource"):
                file_source = loaders[name.replace("Loader", "DBLoader")]
                web_source = loaders[name.replace("Loader", "WebLoader")]
                loader = {
                    "loader": loader_cls,
                    "db_source": file_source,
                    "web_source": web_source,
                }
                self.loaders[loader_cls.resource][loader_cls.data_provider].append(loader)

    def get_data_loader(self, data_provider, resource):
        """
        Gets data loader classes for given data provider and resource.
        :param str data_provider: Which data provider should data be loaded from. Options are 'segev_sports', 'fiba', 'euroleague' or 'acb'
        :param str resource: Name of class from resources directory. Options are 'details', 'boxscore', 'pbp', 'enhancedpbp', 'possessions', 'schedule'
        :return: list of data loader classes
        :rtype: list
        """
        return self.loaders[resource][data_provider]