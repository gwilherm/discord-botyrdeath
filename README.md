# discord-botyrdeath

A Discord bot that plays brutal midi on voice channel.

## Creating a Bot Account

To see the instructions for creating a bot on [discordpy documentation](https://discordpy.readthedocs.io/en/stable/discord.html).

In Bot menu generate a copy the token. Paste it into the `botyrdeath.sh` script.

### Create invite link

In OAuth2 > URL Generator menu

#### Scopes

- [x] bot

#### Bot permissions

- [x] Read Messages/View Channels
- [x] Send Messages
- [x] Speak

Vistit the generated link to invite the bot to your discord server.

## Prepare the Discord server

Create a text channel and a voice channel (you can keep the default 'general' channels).

With right-click, copy the channels id and paste it into the `botyrdeath.sh` script.

## Instal dependencies

### Software and libraries

For apt (Ubuntu, Debian...)

```
sudo apt-get install python3 python3-dev libjack-dev timidity
```

### Python libraries

```
pip install -r requirements.txt
```

## Controlling the bot

In the text channel use the following commands to control the bot :

### Changing the chords pattern

```
!pattern <chord1> <chord2> <chord3> <chord4>
```

Chords from C1 to B9.

### Instert a bell-break

```
!break
```

### Shutdown the bot (only available for users in BotryAdmin role)

```
!quit
```