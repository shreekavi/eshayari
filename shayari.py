#
# Shayari is a command line Python program to auto transcript a video file into subtitles
# Shayari is loosely based on Gaupol.
# Uses Pocketsphinx and gstreamer-pocketsphinx plugin for speech to text transcription.
#
# Read a video file
# Output subtitles file
# 	if 
#		subtitles files is not specified
#	then
#		use the input file name and append .srt
from optparse import OptionParser
import process_files
import util

parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")
parser.add_option("-m", "--mediafile", dest="media_filename", help="Input video/audio file for transcript", metavar="FILE")
parser.add_option("-s", "--subfile", dest="subtitles_filename", help="Output subtitles file", metavar="FILE", action="store", type="string")

(options, args) = parser.parse_args()

#print options.media_filename
#print options.subtitles_filename
assert util.gst_available()
assert util.pocketsphinx_available()
if(options.media_filename && options.subtitles_filename)
	process_files.process_files(options.media_filename, options.subtitles_filename)
else
	print "Usage"


