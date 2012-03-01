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
		vader = self._pipeline.get_by_name("vader")
		vader.connect("vader-start", self._on_vader_start)
		vader.connect("vader-stop", self._on_vader_stop)
		sphinx = self._pipeline.get_by_name("pocketsphinx")
		sphinx.connect("result", self._on_pocketsphinx_result)
		sphinx.set_property("configured", True)
		bus = self._pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect("message::application", self._on_bus_message_application)
		bus.connect("message::eos", self._on_bus_message_eos)
		self._prepare_page()
		self._pipeline.set_state(gst.STATE_PLAYING)
	
	
	def _on_vader_start(self, vader, pos):
		"""Send start position as a message on the bus."""
		import gst
		struct = gst.Structure("start")
		pos = pos / 1000000000 # ns to s
		struct.set_value("start", pos)
		vader.post_message(gst.message_new_application(vader, struct))

	def _on_vader_stop(self, vader, pos):
		"""Send stop position as a message on the bus."""
		import gst
		struct = gst.Structure("stop")
		pos = pos / 1000000000 # ns to s
		struct.set_value("stop", pos)
		vader.post_message(gst.message_new_application(vader, struct))
		
	def _on_pocketsphinx_result(self, sphinx, text, uttid):
		"""Send recognized text as a message on the bus."""
		import gst
		struct = gst.Structure("text")
		struct.set_value("text", text)
		struct.set_value("uttid", uttid)
		sphinx.post_message(gst.message_new_application(sphinx, struct))
	
		
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
		return 'filesrc location=some.avi'
		
	def _get_vader_definition(self):
		"""Return ``vader`` definition for :func:`gst.parse_launch`."""
		# Convert noise level from spin button range [0,32768] to gstreamer
		# element's range [0,1]. Likewise, convert silence from spin button's
		# milliseconds to gstreamer element's nanoseconds.
		noise = 256 / 32768
		silence = 300 * 1000000
		return ("! vader "
		                + "name=vader "
		                + "auto-threshold=false "
		                + "threshold=%.9f " % noise
		                + "run-length=%d " % silence
		                )
	
	def _get_pocketsphinx_definition(self):
		"""Return ``pocketsphinx`` definition for :func:`gst.parse_launch`."""
		definition = "! pocketsphinx name=pocketsphinx "
		acoustic_model_file = "/usr/share/pocketsphinx/model/hmm/wsj1"
		language_file= "/usr/share/pocketsphinx/model/lm/wsj/wlist5o.3e-7.vp.tg.lm.DMP"
		dictionary_file = "/usr/share/pocketsphinx/model/lm/wsj/wlist5o.dic"
		#return definition
		return definition + 'hmm="%s" dict="%s" lm="%s" ' % (
						            acoustic_model_file,
						            dictionary_file,
						            language_file)
	
	def _on_bus_message_application(self, bus, message):
		"""Process application messages from the bus."""
		import gst
		name = message.structure.get_name()
		print "Inside Bus message Application"
		
	def _on_bus_message_eos(self, bus, message):
		"""Flush remaining subtitles to page."""
		
	def _prepare_output(self):
		"""Prepare the output in SubRip format"""