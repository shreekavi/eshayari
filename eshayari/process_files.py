from application import Application

def _process_files(mediafile, subtitlesfile):
	print "Processing the files now .." 
	print "Media File --> " + mediafile
	print "Subtitles File -->"  + subtitlesfile
	
	application = Application(mediafile, subtitlesfile)
	application.speech_recognition()
	#method to call and create subtitles
	#create_subtitles(subtitlesfile)



def create_subtitles(file_name):
	FILE = open(file_name,"w")

	#this block has to get inputs from gstreamer-pocketsphinx
	#subtitle number
	FILE.writelines("1\n")

	#starttime --> end time
	FILE.writelines("00:00:13,800 --> 00:00:16,700\n")

	#Subtitle text
	FILE.writelines("Altocumulus clouds occur between six thousand\n")

	#A blank line
	FILE.writelines("\n")

	#subtitle number
	FILE.writelines("2\n")
	FILE.writelines("00:00:18,600 --> 00:00:20,800\n")
	FILE.writelines("Altocumulus clouds occur between six thousand\n")
	FILE.writelines("\n")

	FILE.close()
	print "Output created in " + file_name

