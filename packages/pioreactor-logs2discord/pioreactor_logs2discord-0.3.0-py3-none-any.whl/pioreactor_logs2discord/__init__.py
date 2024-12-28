# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from json import loads

import click
from pioreactor.background_jobs.base import LongRunningBackgroundJobContrib
from pioreactor.config import config
from pioreactor.mureq import post
from pioreactor.types import MQTTMessage
from pioreactor.whoami import get_unit_name
from pioreactor.whoami import UNIVERSAL_EXPERIMENT


class Logs2Discord(LongRunningBackgroundJobContrib):
    job_name = "logs2discord"
    colors = {
        "DEBUG": "65535",
        "INFO": "65280",
        "NOTICE": "65280",
        "WARNING": "16776960",
        "ERROR": "16711680",
        "CRITICAL": "16711680",
    }

    def __init__(self, unit: str, experiment: str) -> None:
        super(Logs2Discord, self).__init__(
            unit=unit, experiment=experiment, plugin_name="pioreactor_logs2discord"
        )
        self.discord_webhook_url = config.get("logs2discord", "discord_webhook_url")
        if not self.discord_webhook_url:
            self.logger.error(
                "[logs2discord] discord_webhook_url is not defined in your config.ini."
            )
            raise ValueError(
                "[logs2discord] discord_webhook_url is not defined in your config.ini."
            )

        self.log_level = config.get("logs2discord", "log_level", fallback="INFO")
        self.start_passive_listeners()

    def publish_to_discord(self, msg: MQTTMessage) -> None:
        payload = loads(msg.payload)
        topics = msg.topic.split("/")
        unit = topics[1]

        # check to see if we should allow the logs based on the level.
        if getattr(logging, self.log_level) > getattr(logging, payload["level"]):
            return
        elif payload["task"] == self.job_name:
            # avoid an infinite loop, https://github.com/Pioreactor/pioreactor-logs2discord/issues/2
            return

        level = payload["level"]
        color = self.colors[level]
        discord_msg = payload["message"]

        r = post(
            self.discord_webhook_url,
            json={
                "username": "Pioreactor",
                "embeds": [
                    {
                        "description": discord_msg,
                        "author": {
                            "name": unit,
                            "icon_url": f"https://api.dicebear.com/9.x/shapes/svg?seed={unit}",
                        },
                        "title": payload["task"],
                        "color": color,
                    }
                ],
            },
        )

        r.raise_for_status()

    def start_passive_listeners(self) -> None:
        self.subscribe_and_callback(self.publish_to_discord, "pioreactor/+/+/logs/#")


@click.command(name="logs2discord")
def click_logs2discord() -> None:
    """
    turn on logging to Discord
    """

    lg = Logs2Discord(unit=get_unit_name(), experiment=UNIVERSAL_EXPERIMENT)
    lg.block_until_disconnected()
