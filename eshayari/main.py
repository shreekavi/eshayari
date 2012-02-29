from optparse import OptionParser

def _parse_args(args):
	parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")
	parser.add_option("-m", "--mediafile", dest="media_filename", help="Input video/audio file for transcript", metavar="FILE")
	parser.add_option("-s", "--subfile", dest="subtitles_filename", help="Output subtitles file", metavar="FILE", action="store", type="string")
	return parser.parse_args(args)
	

def main(args):
	print "Inside main"
	(options, args) = _parse_args(args)
	
	import util
	assert util.gst_available()
	assert util.pocketsphinx_available()
	
	if options.media_filename and options.subtitles_filename:
		import process_files
		process_files._process_files(options.media_filename, options.subtitles_filename)
	else:
		print "Usage: shayari.py -m MEDIAFILE -s SUBTITLEFILE"
	