"""satnogs-setup module"""
from pathlib import Path

from satnogsconfig import settings


class SatnogsSetup():
    """Interract with satnogs-setup"""

    def __init__(self):
        """Class constructor"""
        self._satnogs_stamp_dir = settings.SATNOGS_SETUP_STAMP_DIR

    @property
    def is_applied(self):
        """Check whether configuration has been applied

        :return: Whether configuration has been applied
        :rtype: bool
        """
        install_stamp_path = Path(self._satnogs_stamp_dir).joinpath(
            settings.SATNOGS_SETUP_INSTALL_STAMP
        )
        if install_stamp_path.exists():
            with install_stamp_path.open(mode='r', encoding='utf-8') as file:
                if file.read():
                    return False
            return True
        return False

    @is_applied.setter
    def is_applied(self, install):
        """Mark that configuration has been applied

        :param install: Configuration has been installed
        :type install: bool
        """
        install_stamp_path = Path(self._satnogs_stamp_dir).joinpath(
            settings.SATNOGS_SETUP_INSTALL_STAMP
        )
        if install:
            with install_stamp_path.open(mode='w', encoding='utf-8'):
                pass
        else:
            try:
                install_stamp_path.unlink()
            except FileNotFoundError:
                pass

    @property
    def tags(self):
        """Get satnogs-setup tags

        :return: Set of tags
        :rtype: set
        """
        tags_path = Path(self._satnogs_stamp_dir
                         ).joinpath(settings.SATNOGS_SETUP_INSTALL_STAMP)
        if tags_path.exists():
            with tags_path.open(mode='r', encoding='utf-8') as file:
                if contents := file.read():
                    return set(contents.split(','))
        return None

    @tags.setter
    def tags(self, tags):
        """Set satnogs-setup tags

        :param tags: List of tags
        :type tags: list
        """
        new_tags = self.tags.copy() if self.tags else set()
        new_tags.update(tags)
        tags_path = Path(self._satnogs_stamp_dir
                         ).joinpath(settings.SATNOGS_SETUP_INSTALL_STAMP)
        if tags_path.exists():
            with tags_path.open(mode='w', encoding='utf-8') as file:
                file.write(','.join(new_tags))
