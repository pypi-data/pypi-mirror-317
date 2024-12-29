#!/usr/bin/env python3

import asyncio
import logging
import time

from prometheus_client import Gauge, start_http_server
from pyoverkiz.client import OverkizClient
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.enums import DataType, Server
from the_conf import TheConf

logger = logging.getLogger(__name__)
conf = TheConf(
    {
        "source_order": ["files"],
        "config_files": [
            "/etc/overkiz-exporter/overkiz_exporter.json",
            "~/.config/overkiz_exporter.json",
        ],
        "parameters": [
            {
                "type": "list",
                "credentials": [
                    {"username": {"type": str}},
                    {"password": {"type": str}},
                    {"servertype": {"type": str}},
                ],
            },
            {"loop": [{"interval": {"default": 60}}]},
            {"prometheus": [{"port": {"type": "int", "default": 8500}}]},
        ],
    }
)
_BASE_LABELS = ["device_id", "device_label", "metric_namespace", "metric_name"]
OVERKIZ_EXPORTER = Gauge("exporter", "", ["status"], namespace="overkiz")
OVERKIZ_MEASURABLE = Gauge("measurable", "", _BASE_LABELS, namespace="overkiz")
OVERKIZ_LABELS = Gauge(
    "labels", "", _BASE_LABELS + ["label"], namespace="overkiz"
)


async def update_metrics(username, password, server_type):
    server = SUPPORTED_SERVERS[Server[server_type]]
    async with OverkizClient(username, password, server=server) as client:
        try:
            await client.login()
        except Exception:  # pylint: disable=broad-except
            logger.error("%r/%r => couldn't connect", server, username)
            return

        devices = await client.get_devices()

        metric_count = metric_ignored = 0
        for device in devices:
            for state in device.states:
                if state.value and not isinstance(state.value, dict):
                    namespace, name = state.name.split(":")
                    lbl = [device.id, device.label, namespace, name]
                    if state.type in {DataType.FLOAT, DataType.INTEGER}:
                        OVERKIZ_MEASURABLE.labels(*lbl).set(state.value)
                    else:
                        OVERKIZ_LABELS.labels(*lbl, state.value).set(1)
                    metric_count += 1
                else:
                    metric_ignored += 1
        OVERKIZ_EXPORTER.labels(status="ok").inc()
        logger.debug(
            "%r/%r wrote %d metric, ignored %d",
            server,
            username,
            metric_count,
            metric_ignored,
        )


async def main() -> None:
    start_http_server(conf.prometheus.port)
    OVERKIZ_EXPORTER.labels(status="loop_interval").set(conf.loop.interval)
    OVERKIZ_EXPORTER.labels(status="credentials_count").set(
        len(conf.credentials)
    )
    while True:
        OVERKIZ_LABELS.clear()  # removing existing labels
        OVERKIZ_EXPORTER.labels(status="ok").set(0)
        OVERKIZ_EXPORTER.labels(status="nok").set(0)
        for credential in conf.credentials:
            try:
                await update_metrics(
                    credential.username,
                    credential.password,
                    credential.servertype,
                )
            except Exception:
                OVERKIZ_EXPORTER.labels(status="nok").inc()
                raise
        time.sleep(conf.loop.interval)


if __name__ == "__main__":
    asyncio.run(main())
