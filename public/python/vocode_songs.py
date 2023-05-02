#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Uses Audacity pipe to automatically vocode two audio files.
Audacity needs to be running first and have mod-script-pipe enabled
before running this script.
Requires Python 2.7 or higher
"""

import os
import sys


if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")

print("Read from \"" + FROMNAME +"\"")

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

# Sends commands to audacity to vocode two songs, then export the result
# The songs are parameters of the program
def vocode_songs():
    filePath1 = os.getcwd().replace('\\', '/') + "/public/audio/temp1_vocals.mp3"
    filePath2 = os.getcwd().replace('\\', '/') + "/public/audio/temp2_accompaniment.mp3"

    do_command('Import2: FileName={}'.format(filePath1))
    do_command('Import2: FileName={}'.format(filePath2))

    do_command('SelectAll:')
    do_command('Duplicate:')
    do_command('SelectTracks: Mode="Set" Track="0.5" TrackCount="0.5"')
    do_command('Silence: Use_Preset="<Factory Defaults>"')
    do_command('SelectTracks: Mode="Set" Track="0" TrackCount="1"')
    do_command('Stereo to Mono:')
    do_command('Amplify: Ratio="2.0"')
    do_command('SelectTracks: Mode="Set" Track="1" TrackCount="0.5"')
    do_command('Silence: Use_Preset="<Factory Defaults>"')
    do_command('SelectTracks: Mode="Set" Track="1" TrackCount="1"')
    do_command('Stereo to Mono:')
    do_command('Amplify: Ratio="2.0"')

    do_command('LastTrack:')
    do_command('TrackClose:')

    do_command('LastTrack:')
    do_command('TrackClose:')

    do_command('FirstTrack:')
    do_command('TruncateSilence:')

    do_command('LastTrack:')
    do_command('TruncateSilence:')

    do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
    do_command('PanLeft:')
    do_command('SelectTracks:Mode="Set" Track="1" TrackCount="1"')
    do_command('PanRight:')
    do_command('SelectAll:')
    do_command('MixAndRender:')
    
    do_command('SelectAll:')

    do_command('Vocoder: dst="1" bands="100" track-vl="100"')

    do_command('Export2: Filename={} NumChannels="2"'.format(os.getcwd().replace('\\', '/') + "/public/vocoded/output1.mp3"))

    do_command('SelectAll:')
    do_command('RemoveTracks:')

    filePath1 = os.getcwd().replace('\\', '/') + "/public/audio/temp2_vocals.mp3"
    filePath2 = os.getcwd().replace('\\', '/') + "/public/audio/temp1_accompaniment.mp3"

    do_command('Import2: FileName={}'.format(filePath1))
    do_command('Import2: FileName={}'.format(filePath2))

    do_command('SelectAll:')
    do_command('Duplicate:')
    do_command('SelectTracks: Mode="Set" Track="0.5" TrackCount="0.5"')
    do_command('Silence: Use_Preset="<Factory Defaults>"')
    do_command('SelectTracks: Mode="Set" Track="0" TrackCount="1"')
    do_command('Stereo to Mono:')
    do_command('Amplify: Ratio="2.0"')
    do_command('SelectTracks: Mode="Set" Track="1" TrackCount="0.5"')
    do_command('Silence: Use_Preset="<Factory Defaults>"')
    do_command('SelectTracks: Mode="Set" Track="1" TrackCount="1"')
    do_command('Stereo to Mono:')
    do_command('Amplify: Ratio="2.0"')

    do_command('LastTrack:')
    do_command('TrackClose:')

    do_command('LastTrack:')
    do_command('TrackClose:')

    do_command('FirstTrack:')
    do_command('TruncateSilence:')

    do_command('LastTrack:')
    do_command('TruncateSilence:')

    do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
    do_command('PanLeft:')
    do_command('SelectTracks:Mode="Set" Track="1" TrackCount="1"')
    do_command('PanRight:')
    do_command('SelectAll:')
    do_command('MixAndRender:')
    
    do_command('SelectAll:')

    do_command('Vocoder: dst="1" bands="100" track-vl="100"')

    do_command('Export2: Filename={} NumChannels="2"'.format(os.getcwd().replace('\\', '/') + "/public/vocoded/output2.mp3"))

    do_command('SelectAll:')
    do_command('RemoveTracks:')


vocode_songs()