SUBDIRS=launcher settings

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
	-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
	-e 's,[@]VERSION[@],$(VERSION),g' \
	-e 's,[@]datadir[@],$(datadir),g'

datadir.py: datadir.py.in Makefile
	$(do_substitution) < $(srcdir)/datadir.py.in > datadir.py

duckdir = $(pythondir)/duck

duck_PYTHON = \
	datadir.py \
	__init__.py 