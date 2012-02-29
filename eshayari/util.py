def gst_available():
	"""Return ``True`` if :mod:`gst` module is available."""
	try:
		print "Checking for Python Gstreamer Bindings.......\n "
		import gst
		print "Found...."
		return True
	except Exception:
		print "Python Gstreamer bindings are not found !\n\n"
		return False
		
def pocketsphinx_available():
	"""Return ``True`` if `pocketsphinx` gstreamer plugin is available."""
	try:
		print "Checking for Gstreamer Pocketsphinx plugins......\n"
		import gst
		print "Found !!!"
		return gst.plugin_load_by_name("pocketsphinx") is not None    
	except Exception:
		print "Gstreamer Pocketsphinx plugins not found !!! \n\n\n"
		return False