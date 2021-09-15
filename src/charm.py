#!/usr/bin/env python3
# Copyright 2021 charmjuju
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import datetime
import logging
import os
from ipaddress import IPv4Address
from pathlib import Path
from subprocess import check_output
from typing import Optional

from cryptography import x509
from kubernetes import kubernetes
from ops.charm import CharmBase, InstallEvent, RemoveEvent
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus
from ops.pebble import ConnectionError

import resource

logger = logging.getLogger(__name__)

# Reduce the log output from the Kubernetes library
logging.getLogger("kubernetes").setLevel(logging.INFO)

class MmeCharm(CharmBase):
    """Charm the service."""

    _authed = False
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.mme_pebble_ready, self._on_mme_pebble_ready)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.remove, self._on_remove)

    def _update_mme_and_run(self):
        self.unit.status = MaintenanceStatus('Configuring mme-app')

        # Define an initial Pebble layer configuration
        pebble_layer = {
            "summary": "mme-app layer",
            "description": "pebble config layer for mme-app",
            "services": {
                "mme": {
                    "override": "replace",
                    "summary": "mme",
                    "command": """/bin/bash -c "while true; do echo 'Running mme-app'; sleep 10; done" """,
                    "startup": "enabled",
                    "environment": {"thing": self.model.config["thing"]},
                }
            },
        }

        container = self.unit.get_container("mme")

        self._push_file_to_container(container, "src/files/scripts/*.*", scriptPath, 0o755)
        self._push_file_to_container(container, "src/files/config/*.*", configPath, 0o644)
        # Add intial Pebble config layer using the Pebble API
        container.add_layer("mme", pebble_layer, combine=True)

        if container.get_service("mme").is_running():
            container.stop("mme")
        container.start("mme")

        self.unit.status = ActiveStatus()

    def _on_mme_pebble_ready(self, event):
        self._update_mme_and_run()

    def _on_config_changed(self, _):
        """Just an example to show how to deal with changed configuration.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle config, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the config.py file.

        Learn more about config at https://juju.is/docs/sdk/config
        """
        current = self.config["thing"]
        if current not in self._stored.things:
            logger.debug("found a new thing: %r", current)
            self._stored.things.append(current)

    def _on_fortune_action(self, event):
        """Just an example to show how to receive actions.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle actions, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the actions.py file.

        Learn more about actions at https://juju.is/docs/sdk/actions
        """
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"fortune": "A bug in the code is worth two in the documentation."})


if __name__ == "__main__":
    main(MmeCharm)
