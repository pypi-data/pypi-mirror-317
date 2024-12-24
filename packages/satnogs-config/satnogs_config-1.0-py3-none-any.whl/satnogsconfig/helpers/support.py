"""SatNOGS support info module"""
import json
import platform
from datetime import datetime, timezone

import psutil

from satnogsconfig._version import get_versions

__version__ = get_versions()['version']

del get_versions


class Support():
    """Create support information to be used for reporting bugs"""

    def __init__(self, config, satnogs_setup):
        """Class constructor"""
        self._config = config
        self._satnogs_setup = satnogs_setup

    @property
    def info(self):
        """Support information

        :return: Support information dictionary
        :rtype: dict
        """
        config = self._config.config.copy()
        redacted_keys = ['satnogs_api_token', 'satnogs_artifacts_api_token']
        for key in redacted_keys:
            if config.get(key) is not None:
                config[key] = '[redacted]'
        data = {
            'versions':
                {
                    'satnogs-client': 'unknown',
                    'satnogs-ansible': 'unknown',
                    'satnogs-flowgraphs': 'unknown',
                    'gr-satnogs': 'unknown',
                    'gr-soapy': 'unknown',
                    'gnuradio': 'unknown',
                    'satnogs-config': __version__,
                },
            'state':
                {
                    'is-applied': self._satnogs_setup.is_applied,
                    'pending-tags': None,
                },
            'system':
                {
                    'date': datetime.now(timezone.utc).isoformat(),
                    'platform': dict(platform.uname()._asdict()),
                    'memory': dict(psutil.virtual_memory()._asdict()),
                    'disk': dict(psutil.disk_usage('/')._asdict()),
                },
            'configuration': config,
        }

        if tags := self._satnogs_setup.tags:
            data['state']['pending-tags'] = list(tags)

        return data

    def dump(self, *args, **kwargs):
        """Dump support information

        :return: JSON dump of support information
        :rtype: str
        """
        return json.dumps(self.info, *args, **kwargs)
