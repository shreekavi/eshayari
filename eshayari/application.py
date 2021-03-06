import gobject
import pygst
gobject.threads_init()
import gst
import logging

class Application():
	
	def __init__(self, mediafile, subtitlesfile):
		self._pipeline = None
		self._starts = []
		self._stops = []
		self._text = None
		self._texts = []
		self.init_gst()
		self.mediafile = mediafile
		self.subtitlesfile= subtitlesfile
		logger = logging.getLogger("eshayari")
		logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		logger.addHandler(ch)
	
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
		print "Initializing Bus -------->"
		bus = self._pipeline.get_bus()
		bus.add_signal_watch()
		print "Sending Message to Bus ---------->"
		bus.connect("message::application", self._on_bus_message_application)
		print "After Message to Bus ----------->"
		bus.connect("message::eos", self._on_bus_message_eos)
		self._prepare_output()
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
		logger.info( "Inside Bus Message Application")
		FILE = open("debug.txt","w")

		#this block has to get inputs from gstreamer-pocketsphinx
		#subtitle number
		FILE.writelines(name)
		if name == "start":
			start = message.structure["start"]
			self._starts.append(start)
			if self._text is not None:
				# Store previous text.
				self._texts[-1] = self._text
				self._text = None
			self._stops.append(None)
			self._texts.append(None)
			duration = self._pipeline.query_duration(gst.FORMAT_TIME, None)[0]
			duration = duration / 1000000000 # ns to s
			fraction = start / duration
			if len(self._starts) > 1:
				# Append previous subtitle to page.
				self._append_subtitle(-2)
		if name == "stop":
			stop = message.structure["stop"]
			self._stops[-1] = stop
		if name == "text":
			text = message.structure["text"]
			if not isinstance(text, unicode):
				text = unicode(text, errors="replace")
			self._text = text
		FILE.close()
		
	def _on_bus_message_eos(self, bus, message):
		"""Flush remaining subtitles to page."""
		if self._text is not None:
			# Store previous text.
			self._texts[-1] = self._text
			self._text = None
		if self._starts and self._stops[-1] is not None:
			self._append_subtitle(-1)
			self._stop_speech_recognition()
		
	def _prepare_output(self):
		"""Prepare the output in SubRip format"""
		import process_files
		process_files.create_subtitles("gatesspeech.srt")