#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import discord
import subprocess
import discord.ext.commands
import mido
from mido import Message, MidiFile, MidiTrack
import time
import threading

ADMIN_ROLE = "BotyrAdmin"

TEXT_CHANNEL  = os.environ['TEXT_CHANNEL']
VOICE_CHANNEL = os.environ['VOICE_CHANNEL']

bot = discord.ext.commands.Bot(command_prefix='!') #discord.Client()

bot.midiserver = subprocess.Popen(['timidity', '-iA', '-Ow', '-o', '-'], stdout=subprocess.PIPE)
bot.midiclient = None

NOTES = [
    'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1',
    'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2',
    'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
    'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
    'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5',
    'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6',
    'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7',
    'C8', 'C#8', 'D8', 'D#8', 'E8', 'F8', 'F#8', 'G8', 'G#8', 'A8', 'A#8', 'B8',
    'C9', 'C#9', 'D9', 'D#9', 'E9', 'F9', 'F#9', 'G9', 'G#9', 'A9', 'A#9', 'B9',
]

def compose_masterpiece(pattern):
    mid = MidiFile()
    guitar1 = MidiTrack()
    # guitar2 = MidiTrack()
    bass    = MidiTrack()
    drums   = MidiTrack()

    mid.tracks.append(guitar1)
    # mid.tracks.append(guitar2)
    mid.tracks.append(bass)
    mid.tracks.append(drums)

    #          1                      2
    # C  D  E  F  G  A  B  | C  D  E  F  G  A  B  | C
    # 0  2  4  6  7  9  11 | 12 14 16 17 19 21 23 | 24
    #          3                      4
    # C  D  E  F  G  A  B  | C  D  E  F  G  A  B  | C
    # 24 26 28 29 31 33 35 | 36 38 40 41 43 45 47 | 48
    #          5                      6
    # C  D  E  F  G  A  B  | C  D  E  F  G  A  B  | C
    # 48 50 52 53 55 57 59 | 60 62 64 65 67 69 71 | 72
    vel = 64
    dur = 64

    # Set Distorsion Guitar istrument
    guitar1.append(Message('program_change', program=30, time=0))
    # Pan
    # guitar1.append(Message('control_change', control=10, value=32, time=0))

    for chord in pattern:
        # Power chord
        try:
            root = NOTES.index(chord.upper())
        except ValueError:
            root = 0

        fifth = root + 5
        octave = root + 12

        for i in range(4):
            guitar1.append(Message('note_on', note=root, velocity=vel, time=0))
            guitar1.append(Message('note_on', note=fifth, velocity=vel, time=0))
            guitar1.append(Message('note_on', note=octave, velocity=vel, time=0))
            guitar1.append(Message('note_off', note=root, velocity=127, time=32))
            guitar1.append(Message('note_off', note=fifth, velocity=127, time=32))
            guitar1.append(Message('note_off', note=octave, velocity=127, time=32))


    # Set Bass instrument
    bass.append(Message('program_change', program=34, channel=1, time=0))
    for chord in pattern:
        try:
            root = NOTES.index(chord.upper())
        except ValueError:
            root = 0

        for i in range(2):
            bass.append(Message('note_on', channel=1, note=root, velocity=vel, time=64))
            bass.append(Message('note_off', channel=1, note=root, velocity=127, time=127))

    # drums
    crash = 49
    bd = 36
    sd = 40
    hh = 46

    drums.append(Message('program_change', channel=9, program=0, time=0))
    drums.append(Message('note_on', note=crash, channel=9, velocity=vel, time=0))
    for i in range(8):
        drums.append(Message('note_on', note=bd, channel=9, velocity=vel, time=0))
        drums.append(Message('note_on', note=sd, channel=9, velocity=vel, time=0))
        drums.append(Message('note_on', note=hh, channel=9, velocity=vel, time=0))
        drums.append(Message('note_off', note=bd, channel=9, velocity=127, time=64))
        drums.append(Message('note_off', note=sd, channel=9, velocity=127, time=64))
        drums.append(Message('note_off', note=hh, channel=9, velocity=127, time=64))

    return mid

def play():
    t = threading.current_thread()
    output_names = [pn for pn in mido.get_output_names() if 'port 0' in pn]
    print(f'Available ports: {output_names}')
    outport = mido.open_output(output_names[0])

    t.mid = compose_masterpiece(getattr(t, "pattern"))

    while getattr(t, "do_run", True):
        if getattr(t, "do_break", False):
            time.sleep(.41)
            outport.send(Message('note_on', note=81, channel=9, velocity=100, time=64))
            time.sleep(.41)
            t.do_break = False

        for msg in t.mid.play():
            outport.send(msg)


@bot.event
async def on_ready():
    channel = bot.get_channel(int(TEXT_CHANNEL.strip()))
    voice_channel = bot.get_channel(int(VOICE_CHANNEL.strip()))
    print(f"Found channel: {channel.name}, {channel.id}")
    print(f"Found voice channel: {voice_channel.name}, {voice_channel.id}")
    await channel.send(f'Bonjour @everyone, je vais vous jouer ma dernière composition !\n'
                       f'Rendez-vous sur #{voice_channel.name} !')
    if channel is None or voice_channel is None:
        exit
    voice_client = await voice_channel.connect()
    src = discord.FFmpegPCMAudio(bot.midiserver.stdout, pipe=True)
    await bot.change_presence(activity=discord.Game('Composing!'))
    voice_client.play(src) # , after=self.after_play)

    time.sleep(1)

    bot.midiclient = threading.Thread(target=play, args=())
    bot.midiclient.daemon = True                            # Daemonize thread
    bot.midiclient.start()                                  # Start the execution
    bot.midiclient.pattern = ('E3', 'C3', 'C#3', 'C3')

@bot.command()
async def quit(context):
    print('Handle quit')
    if ADMIN_ROLE in list(map(lambda r: r.name, context.author.roles)):
        if bot.midiclient is not None:
            bot.midiclient.do_run = False
            bot.midiclient.join()

        if bot.midiserver is not None:
            bot.midiserver.terminate()
        await context.channel.send('Bye.')
        await bot.logout()
    else:
        print(f'Member {context.author.name} not allowed to run this command.')

@bot.command()
async def pattern(context, *args):
    print(f'Handle pattern: {args}')
    if len(args) == 0:
        currentPattern = ' '.join(bot.midiclient.pattern)
        await context.send(f'Current pattern is: `{currentPattern}`')
    else:
        if len(args) != 4:
            await context.send('Pattern must contains 4 chords.')
            return

        for chord in args:
            if chord.upper() not in NOTES:
                await context.send(f'Unknown chord: `{chord}`')
                return

        bot.midiclient.pattern = args
        bot.midiclient.mid = compose_masterpiece(args)

@bot.command(name='break')
async def do_break(context, *args):
    print(f'Handle do_break: {args}')
    bot.midiclient.do_break = True

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

bot.run(os.environ['BOTYR_TOKEN'])

