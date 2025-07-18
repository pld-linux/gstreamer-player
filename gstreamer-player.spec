#
# Conditional build:
%bcond_with	nautilus	# build GStreamer nautilus view
#
%define		gstname 	gst-player
Summary:	GStreamer Multimedia Player
Summary(pl.UTF-8):	Odtwarzacz multimedialny GStreamer
Name:		gstreamer-player
Version:	0.8.0
Release:	8
License:	GPL
Epoch:		1
Group:		X11/Applications/Multimedia
Source0:	http://gstreamer.freedesktop.org/src/gst-player/%{gstname}-%{version}.tar.bz2
# Source0-md5:	4b67afde07fdcf2bde0e3d9b6699465c
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-locale_names.patch
URL:		http://gstreamer.net/
BuildRequires:	automake
BuildRequires:	gstreamer-plugins-devel >= 0.8.0
BuildRequires:	gstreamer08x-GConf-devel >= 0.8.0
BuildRequires:	libgnomeui-devel >= 2.4.0.1
BuildRequires:	rpm-build >= 4.1-10
%{?with_nautilus:BuildRequires:	nautilus-devel >= 2.4.0}
Requires:	gstreamer-plugins
Requires:	gstreamer08x >= 0.8.0
Requires:	gstreamer08x-GConf
Requires:	gstreamer08x-audio-effects
Requires:	gstreamer08x-colorspace >= 0.8.0
Requires:	gstreamer08x-gnomevfs
Requires:	gstreamer08x-mad
Requires:	gstreamer08x-mpeg
Requires:	gstreamer08x-vorbis
Requires:	gstreamer08x-videosink
Requires:	gstreamer08x-audiosink
Requires:	gstreamer08x-video-effects
Requires(post):	/sbin/ldconfig
Requires(post):	%{_bindir}/gconftool-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GStreamer Multimedia Player.

%description -l pl.UTF-8
Odtwarzacz multimedialny GStreamer.

%package devel
Summary:	GStreamer Multimedia Player development files
Summary(pl.UTF-8):	Pliki programistyczne odtwarzacza multimedialnego GStreamer
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
GStreamer Multimedia Player development files.

%description devel -l pl.UTF-8
Pliki programistyczne odtwarzacza multimedialnego GStreamer.

%package nautilus
Summary:	GStreamer nautilus view
Summary(pl.UTF-8):	Widok GStreamer dla nautilusa
Group:		Libraries/Multimedia
Requires:	gstreamer-player = %{epoch}:%{version}
Requires:	nautilus >= 2.4.0

%description nautilus
GStreamer nautilus view for media files.

%description nautilus -l pl.UTF-8
Widok GStreamer do nautilusa dla plików multimedialnych.

%prep
%setup -q -n %{gstname}-%{version}
%patch -P0 -p1
%patch -P1 -p1

mv -f po/{no,nb}.po

%build
cp /usr/share/automake/config.sub .
%configure \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog
%config %{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_datadir}/application-registry/*
%dir %{_datadir}/%{gstname}
%dir %{_datadir}/%{gstname}/ui
%{_datadir}/%{gstname}/ui/*
%{_datadir}/mime-info/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_mandir}/man?/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{gstname}-%{version}

%if %{with nautilus}
%files nautilus
%defattr(644,root,root,755)
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/%{gstname}-control
%attr(755,root,root) %{_libdir}/%{gstname}-view
%{_datadir}/gnome-2.0/ui/%{gstname}-view-ui.xml
%endif
