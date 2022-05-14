# Discord Bot: Anchor.fm Analytics

Let everyone on Discord regularly see how your podcast is performing.

# Installation & Usage

Discord bots are run on a personal computer of your choice with internet access. An inexpensive ARM computer with Linux is recommended. The commands given work on Ubuntu.

## Get the Code

1. [Download & unzip](https://github.com/RobbyCBennett/DiscordBotAnchorAnalytics/archive/refs/heads/master.zip) or clone [this repository](https://github.com/RobbyCBennett/DiscordBotAnchorAnalytics).
```bash
git clone git@github.com:RobbyCBennett/DiscordBotAnchorAnalytics.git
```

2. Inside of this folder, copy the `.env.example` and name it `.env`
```bash
cd DiscordBotAnchorAnalytics && cp .env.example .env
```

## Install Python

3. Install [python](https://www.python.org/downloads/)

```bash
sudo apt install python
```

4. Install [pip](https://pip.pypa.io/en/stable/installation/)

```bash
wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm get-pip.py
```

## Make a Bot & Add to Channel

5. Make an app then a bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   * See [this guide](https://discord.com/developers/docs/getting-started) for help with this process.
   * Don't name the app or the bot with the word "discord" in it.

6. Get the application id with General Information > Application ID. Copy the id. In the `.env` file, this should be saved as `DISCORD_BOT_ID`

7. Get a new token with Bot > Build-A-Bot > Reset Token. Copy the token. In the `.env` file, this should be saved as `DISCORD_BOT_TOKEN`

8. Get a link to add your bot to the channel with OAuth2 > URL Generator.
   * Under `SCOPES` select `bot`.
   * Under `BOT PERMISSIONS` select `Send Messages`.

9. Send this link to someone in the Discord server who has permissions to add bots.

10. [Copy the Discord channel ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). In the `.env` file, this should be saved as `DISCORD_CHANNEL_ID`

## Anchor Credentials

11. In the `.env` file, add your Anchor.fm email & password as `ANCHOR_EMAIL` and `ANCHOR_PASSWORD`.

## Pick a Time

12. In the `.env` file, choose a weekly time for the analytics to be retrieved and sent to Discord, and save it as `WEEKLY_TIME`.

## Install & Run the Bot

13. Install python dependencies, install in `/usr/local/src/discord-bot-anchor-analytics`, and make service

```
make install
```
