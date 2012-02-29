import gst
class Application():
	
	def __init__(self, mediafile, subtitlesfile):
		self._pipeline = None
		self.init_gst()
		self.mediafile = mediafile
		self.subtitlesfile= subtitlesfile
	
	def speech_recognition(self):
		print "Inside Speech Recognition"
		print self.mediafile
		print self.subtitlesfile
	
	def init_gst(self):
		self._pipeline = gst.parse_launch(self._get_pipeline_definition())
		
	def _get_pipeline_definition(self):
		"""Return pipeline definition for :func:`gst.parse_launch`."""
		return (self._get_filesrc_definition()
		                + "! decodebin2 "
		                + "! audioconvert "
		                + "! audioresample "
		                + self._get_vader_definition()
		                + self._get_pocketsphinx_definition()
		                + "! fakesink"
		                )
	
	def _get_filesrc_definition(self):
		"""Return ``filesrc`` definition for :func:`gst.parse_launch`."""
		return 'filesrc location=some.avi '
	
		
	def init_gst_bkp(self):
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
		
	def asr_result(self, asr, text, uttid):
		"""Forward result signals on the bus to the main thread."""
		struct = gst.Structure('result')
		struct.set_value('hyp', text)
		struct.set_value('uttid', uttid)
		asr.post_message(gst.message_new_application(asr, struct))
		
	def application_message(self, bus, msg):
		"""Receive application messages from the bus."""
		msgtype = msg.structure.get_name()
		if msgtype == 'partial_result':
			self.partial_result(msg.structure['hyp'], msg.structure['uttid'])
		elif msgtype == 'result':
			self.final_result(msg.structure['hyp'], msg.structure['uttid'])
			self.pipeline.set_state(gst.STATE_PAUSED)