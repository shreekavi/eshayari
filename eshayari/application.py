import gst
class Application():
	
	def __init__(self):
		self._pipeline = None
		self.init_gst()
	
	def speech_recognition(self,mediafile, subtitlesfile):
		print "Inside Speech Recognition"
		print mediafile
		print subtitlesfile
		
	def init_gst(self):
		self.pipeline = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
		                                         + '! vader name=vad auto-threshold=true '
		                                         + '! pocketsphinx name=asr ! fakesink')