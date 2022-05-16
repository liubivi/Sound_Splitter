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
#------------- MAIN: splits large mp3, wav files to smaller parts
#------------- so that they can be easier uploaded in the browser applications
#-------------------------------------------------------------------------

filename = sys.argv[-1]
#print (filename.find(".wav",len(filename)-5, len(filename)))
print ("'Sound Splitter' splits your audio (wav, mp3, wma, ogg, aac, ...) or video (mp4, avi, flv, ...) files into small 16 bit 16 kHz wav (mp3) sound files, so that you can use them for other purposes.")
print ("File {} is going to be split into several separate files. \nBe patient, this process may take a couple of minutes, depending on the length of the audio/video file.\n".format(filename))
print("Opening file {} ...".format(filename))
if filename.find(".wav",len(filename)-5, len(filename))>0:
    song = AudioSegment.from_wav(filename) 
elif filename.find(".mp3",len(filename)-5, len(filename))>0:
    song = AudioSegment.from_mp3(filename)
elif filename.find(".ogg",len(filename)-5, len(filename))>0:
    song = AudioSegment.from_ogg(filename) 
elif filename.find(".flv",len(filename)-5, len(filename))>0:
    song = AudioSegment.from_flv(filename)
elif filename.find(".mp4",len(filename)-5, len(filename))>0:
    song = AudioSegment.from_file(filename, "mp4")
else:
    song = AudioSegment.from_file(filename) 

#-- extractig filename from file path and removing the the file extension ------------------------------------
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


print ("Total channels:", song.channels)

#no_channels = song.channels
#for channel in range(no_channels):
#    song = song_channels[channel].set_sample_width(2).set_frame_rate(16000)
    
song = song.set_channels(1).set_sample_width(2).set_frame_rate(16000)
originalsong = song
hours = int(song.duration_seconds // 3600)
minutes = int(((song.duration_seconds / 3600 - song.duration_seconds // 3600) * 60)//1)
seconds = song.duration_seconds - hours * 3600 - minutes * 60
print ("Total record length in seconds:", round(song.duration_seconds, 3), hours, "hours", minutes, "minutes", round(seconds, 3), "seconds")
remaining_chunk = song
i = 1

size_check = 0

while (remaining_chunk.duration_seconds > SIZE_LIMIT):    
    chunk_count = (remaining_chunk.duration_seconds // SIZE_LIMIT) + 1
    chunk_size = (1000 * remaining_chunk.duration_seconds) // chunk_count #takes away the number part after comma
    interval = 2 * 60 * 1000
    soft_cut = chunk_size - interval
    first_chunk = remaining_chunk [:soft_cut]
    medium_chunk = remaining_chunk [soft_cut:chunk_size]
    
    no_chunks, output_chunks = split (medium_chunk) 
    for j in range(no_chunks-1):
        first_chunk = first_chunk + output_chunks[j]
    print(seconds_to_human_readable_time("chunk {}".format(i), len(first_chunk) / 1000))
    remaining_chunk = remaining_chunk [len(first_chunk):]
    #save_song(first_chunk, "{0}_channel_{1}_chunk_{2}_{3}.{4}".format(filename, channel, i, seconds_to_filename(len(first_chunk)/1000), OUTPUT_FORMAT))
    save_song(first_chunk, "{0}_chunk_{1}_{2}.{3}".format(filename.replace(" ","_"), i, seconds_to_filename(len(first_chunk)/1000), OUTPUT_FORMAT))
    size_check = size_check + len(first_chunk)/1000
    i += 1
save_song(remaining_chunk, "{0}_chunk_{1}_{2}.{3}".format(filename.replace(" ","_"), i, seconds_to_filename(len(remaining_chunk)/1000), OUTPUT_FORMAT)) 
#save_song(remaining_chunk, "{0}_channel_{1}_chunk_{2}_{3}.{4}".format(filename, channel, i, seconds_to_filename(len(remaining_chunk)/1000), OUTPUT_FORMAT))
print(seconds_to_human_readable_time("chunk {}".format(i), len(remaining_chunk) / 1000))
size_check = size_check + len(remaining_chunk)/1000
print ("  Length of all saved chunks:", round(size_check, 3))    
save_song(originalsong, "{0}_{1}.{2}".format(filename.replace(" ","_") + "_original", seconds_to_filename(len(originalsong)/1000), OUTPUT_FORMAT))
print(seconds_to_human_readable_time("original song in compact format", len(originalsong) / 1000))
print("Splitting completed.")