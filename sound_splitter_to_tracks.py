# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 22:36:32 2021
@author: Vilmantas LIUBINAS
v.liubinas@gmail.com

"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
import subprocess
import sys
import os
import time


SIZE_LIMIT = 40000
OUTPUT_FORMAT = "mp3"

def seconds_to_human_readable_time(name_of_record, chunk_size_in_seconds):
    hours = int(chunk_size_in_seconds // 3600)
    minutes = int(((chunk_size_in_seconds / 3600 - chunk_size_in_seconds // 3600) * 60)//1)
    seconds = round(chunk_size_in_seconds - hours * 3600 - minutes * 60, 3)
    return ("  Length of " + name_of_record + " in seconds: " + str(chunk_size_in_seconds) + " (" + str(hours) + ":" + str(minutes) + ":" + str(seconds) + ") ")
    
def seconds_to_filename(chunk_size_in_seconds):
    hours = int(chunk_size_in_seconds // 3600)
    minutes = int(((chunk_size_in_seconds / 3600 - chunk_size_in_seconds // 3600) * 60)//1)
    seconds = round(chunk_size_in_seconds - hours * 3600 - minutes * 60, 3)
    return (str(hours) + "_h_" + str(minutes) + "_min_" + str(seconds) + "_sec")


def count_audio_tracks(filename):
    pos = 0
    output = str(subprocess.check_output("ffprobe -v error -show_entries stream=codec_type,index:stream_tags=language -i {}".format(r'"'+filename+r'"'))) #index,codec_name
    #output = r'  [STREAM]\r\nindex=012\r\ncodec_type=audio\r\n[/STREAM]\r\n[STREAM]\r\nindex=123\r\ncodec_type=audio\r\n[/STREAM]\r\n[STREAM]\r\nindex=22\r\ncodec_type=audio\r\n[/STREAM]\r\n'
    
    tracks = []
    languages = []
    total_tracks = output.count("nindex=")
    
    for track_no in range(0, total_tracks):
        pos = output.find("nindex=", pos) + 6
        audio_track_no = ""
        track_no_pos = 0
        for char in range(1, 4):
            for num in range(0, 10):
               track_no_pos = output.find(str(num), pos + char, pos + char + 1)
               if track_no_pos>0:
                   audio_track_no = str(audio_track_no) + output[track_no_pos]
        type_pos = output.find("ncodec_type=", pos) + 12
        m = output[type_pos:type_pos + 2]
        if output[type_pos:type_pos + 2]=="au":
            tracks.append(audio_track_no)
            language_pos = output.find("language=", type_pos, len(output)) 
            if language_pos>-1:
               language_pos = language_pos + 9
               language = output[language_pos:language_pos+2]
               languages.append(language)
            else:
               languages.append("xx")
    return tracks, languages

def split(sound):
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, 
        min_silence_len = 300,
        silence_thresh = dBFS-16,
        keep_silence = True
    )
    
    target_length = 5 * 1000 
    output_chunks = [chunks[0]]
    no_chunks = 0
    short_chunk_found = 0
    for chunk in chunks[1:]:
      
      if len(output_chunks[-1]) < target_length:
        output_chunks[-1] += chunk
        short_chunk_found = 1
      else:
        no_chunks = no_chunks + 1
        short_chunk_found = 0
        # if the last output chunk is longer than the target length,
        # we can start a new one
        output_chunks.append(chunk)
    if short_chunk_found == 1:
        no_chunks = no_chunks + 1
    if no_chunks<1:
        no_chunks = 1
        output_chunks.append(sound)
    return no_chunks, output_chunks

def save_song(song, filename):
    song.export(
        ".//{}".format(filename),
        bitrate = "16k",
        format = OUTPUT_FORMAT 
    )

#-------------------------------------------------------------------------
#------------- MAIN: extracts all audio tracks and saves them as mp3
#-------------------------------------------------------------------------

filename = sys.argv[-1]
#print(filename)
#os.chdir(os.path.split(sys.argv[0])[0])
#print (filename.find(".wav",len(filename)-5, len(filename)))
print ("'Sound Splitter' extracts all audio tracks from your audio or video files and saves them in mp3 format.")
print ("File '{}' is going to be deconstructeed into several audio tracks. \nBe patient, this process may take a couple of minutes, depending on the length of the audio/video file.\n".format(filename))

audio_tracks, languages = count_audio_tracks(os.path.normpath(filename))

#-- extractig filename from file path and removing the file extension ------------------------------------
full_filename = filename
#print(full_filename)
filename_ok = True
char = len(filename)-1
newname=""
while filename_ok and char>-1:
  if filename[char] == "/" or filename[char] == '\\':
     filename_ok = False
  else:
      newname = filename[char]+newname
  char -= 1
filename = newname[0:-4]
#-------------------------------------------------------------------------------------------------------------
#-- building the ffmpeg command to extract all audio tracks --------------------------------------------------
output = ""
for counter, track_no in enumerate(audio_tracks):
    output = output + str("-map 0:{0} -acodec libmp3lame {1}_track_{0}_{2}.mp3 ".format(track_no, filename.replace(" ","_"), languages[counter])) #index,codec_name
output = "ffmpeg -y -i {0} ".format(r'"' + full_filename + r'"') + output 
#print(output)

if counter == 0:
    print("Extracting {} audio track...".format(counter+1))
else:
    print("Extracting {} audio tracks...".format(counter+1))
res = subprocess.run(output, capture_output=True, text=True)
#print(res.stderr)
if str(res.stderr).find("size=") > -1:
    print("Audio tracks extracted.")
    
#time.sleep(5)