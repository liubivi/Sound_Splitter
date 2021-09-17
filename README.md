SOUND SPLITTER V.1.0

Description

“Sound splitter” is a free Windows application that splits large audio and video files (e.g. of public speeches, presentations), recorded in the most popular formats, such as wav, mp3, flv, mp4, wma, into smaller wav (or mp3) files of around 60 MB in size. It makes an attempt to cut the input file in a silent place, so that a word in a recorded speech is not split in the middle. It also contains the tool for splitting large video files to audio tracks in mp3 format.
Supported input file formats include as a minimum the following formats:

•	audio formats: wav, mp3, wma, ogg, aac, ...

•	video formats: mp4, avi, flv, ...

You can try other input file formats supported by FFMPEG.
The output files are 16 kHz 16 bit wav or mp3 files, depending on the application you are using: sound_splitter.exe outputs files in wav format, sound_splitter_mp3.exe outputs files in mp3 format.
The file splitting allows you a hassle-free upload of very large files to online services (e.g. Speech to text service). Among other things, when you submit many files to the online sound processing service, you can also expect a faster finishing time, because such tasks normally run in paralel.

The application consists of three files:

Sound_Splitter.exe - splits a larger file to smaller wav files

Sound_Splitter_mp3.exe - splits a larger file to smaller mp3 files

Sound_Splitter_to_tracks.exe - converts a multi-track video or audio file into several mp3 files, each of them containing a single audio track. The quality of the records is not degraded in this step: the bit-rate and the frequency of the record remains the same as in the original track. It means that the tool can be also used for the easy conversion of video/audio files to mp3 without any quality loss.

Usage

Always make a secure copy of the original file before doing any operations with Sound Splitter.
Using your mouse, drag and drop the audio or video file in question on the application sound_splitter.exe or sound_splitter_mp3.exe. The application should start processing the file immediately.

Requirements

Windows 10 (tested) or possibly other Windows versions.
FFMPEG application must be installed and included in the Windows PATH environmental variable before using Sound Splitter. Check the Sound Splitter tutorial on how to do it.

FFMPEG is available at the official website https://ffmpeg.org.
Windows version is available at https://ffmpeg.org/download.html#build-windows.
Direct download link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip.

License

Free
