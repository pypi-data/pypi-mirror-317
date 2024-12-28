### Pioreactor Logs2Discord

This is a Pioreactor plugin to post a bioreactor's logs to a Discord channel.

### Installation

This is a two part installation.

#### 1. Setting up your Discord channel

1. You probably want a dedicated channel for incoming logs, as it can get chatty. So go ahead
and create a dedicated channel in your Discord channel. I've called mine `experiment_logs`.

2. Under your server's dropdown, find "Server Settings" -> "Integrations"

3. Click "Webhooks" -> "New webhook" to create your webhook. Give it a name like `PioreactorLogs`, and choose the channel from step 1. Here's an avatar icon you can use too:

   ![icon](https://github.com/Pioreactor/pioreactorui_frontend/blob/main/public/logo.png)

4. Copy the webhook URL to your clipboard. We'll need this in a moment.

#### 2. Installing this plugin

1. In your Pioreactor interface, click on "Plugins". Find `pioreactor-logs2discord`, and click "Install" beside it. **Or** you can run `pio plugins install pioreactor-logs2discord`. Either way, this plugin will be installed on your leader Pioreactor.

2. After installing (should take less than a minute), click on "Configuration". At the bottom of the page will be a section called `[logs2discord]`.

```
[logs2discord]
discord_webhook_url=
log_level=INFO
```

Add your webhook URL from step 4. here. Click "Save". You can also change the level of logs to report, see [Python logging levels](https://docs.python.org/3/library/logging.html#logging-levels).

3. Power-cycle (reboot) the Pioreactor leader, or ssh into the Pioreactor leader and run `sudo systemctl restart pioreactor_startup_run@logs2discord.service`

4. In your dedicated Discord channel, you should start to see logs arrive!
