def gst_available():
	"""Return ``True`` if :mod:`gst` module is available."""
	try:
		import gst
		return True
	except Exception:
		return False
		
def pocketsphinx_available():
	"""Return ``True`` if `pocketsphinx` gstreamer plugin is available."""
	try:
		import gst
		return gst.plugin_load_by_name("pocketsphinx") is not None    
	except Exception:
		return False