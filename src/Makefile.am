SUBDIRS = duck

bin_SCRIPTS = duck-launcher duck-settings duck-plugins
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = duck-launcher.in duck-settings.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
	-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
	-e 's,[@]VERSION[@],$(VERSION),g' \
	-e 's,[@]datadir[@],$(datadir),g'

duck-launcher: duck-launcher.in Makefile
	$(do_substitution) < $(srcdir)/duck-launcher.in > duck-launcher
	chmod +x duck-launcher
duck-settings: duck-settings.in Makefile
	$(do_substitution) < $(srcdir)/duck-settings.in > duck-settings
	chmod +x duck-settings
	
	
duck-plugins: duck-plugins.in Makefile
	$(do_substitution) < $(srcdir)/duck-plugins.in > duck-plugins
	chmod +x duck-settings