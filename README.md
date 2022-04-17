# Discord Bot: Anchor.fm Analytics

Let everyone on Discord regularly see how your podcast is performing.

# Installation & Usage

Discord bots are run on a personal computer of your choice with internet access. An inexpensive ARM computer with Linux is recommended.

## Get the Code

1. [Download & unzip](https://github.com/RobbyCBennett/DiscordBotAnchorAnalytics/archive/refs/heads/master.zip) or [clone](https://github.com/RobbyCBennett/DiscordBotAnchorAnalytics) this repository.

2. Inside of this folder, copy the `.env.example` and name it `.env`

## Install Dependencies

3. Install [python](https://www.python.org/downloads/)

4. Install [pip](https://pip.pypa.io/en/stable/installation/)

5. In the command line inside of this folder, type in one of the following commands.

```
make install
```

```
sudo pip install python-dotenv aiohttp discord
```

## Make a Bot & Add to Channel

6. Make an app then a bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   * See [this guide](https://discord.com/developers/docs/getting-started) for help with this process.
   * Don't name the app or the bot with the word "discord" in it.

7. Get a new token with Bot > Build-A-Bot > Reset Token. Copy the token. In the `.env` file, this should be saved as `DISCORD_BOT_TOKEN`

8. Get a link to add your bot to the channel with OAuth2 > URL Generator.
   * Under `SCOPES` select `bot`.
   * Under `BOT PERMISSIONS` select `Send Messages`.

9. Send this link to someone in the Discord server who has permissions to add bots.

10. [Copy the Discord channel ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). In the `.env` file, this should be saved as `DISCORD_CHANNEL_ID`

## Anchor Credentials

11. In the `.env` file, add your Anchor.fm email & password as `ANCHOR_EMAIL` and `ANCHOR_PASSWORD`.

## Run the Bot

12. Run the bot in the background by typing in one of the following commands.


```
make foreground
```

```
python bot.py
```

You can alternatively run the bot in the foreground with one of the following commands.

```
make background
```

```
nohup python bot.py </dev/null >/dev/null 2>&1 &
```
