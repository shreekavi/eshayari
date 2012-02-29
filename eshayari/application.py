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
		asr = self.pipeline.get_by_name('asr')
		asr.connect('partial_result', self.asr_partial_result)
		asr.connect('result', self.asr_result)
		asr.set_property('configured', True)

		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect('message::application', self.application_message)

		self.pipeline.set_state(gst.STATE_PAUSED)
		
	def asr_partial_result(self, asr, text, uttid):
		"""Forward partial result signals on the bus to the main thread."""
		struct = gst.Structure('partial_result')
		struct.set_value('hyp', text)
		struct.set_value('uttid', uttid)
		asr.post_message(gst.message_new_application(asr, struct))