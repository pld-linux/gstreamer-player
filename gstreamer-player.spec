
%define		snap		20030127
%define 	gstname 	gst-player

Summary:	GStreamer Multimedia Player
Summary(pl):	Odtwarzacz multimedialny GStreamer
Name:		gstreamer-player
Version:	0.5.1
Release:	1
License:	GPL
Epoch:		1
Group:		X11/Multimedia
Source0:	http://dl.sf.net/gstreamer/%{gstname}-%{version}.tar.bz2
# Source0-md5: ece8fc2b458bc85e482733dd6f8630b6
#Source0:	%{gstname}-%{version}-%{snap}.tar.bz2
URL:		http://gstreamer.net/
BuildRequires:	gstreamer-plugins-devel >= 0.6.1
BuildRequires:	gstreamer-play-devel >= 0.6.1
BuildRequires:	libgnomeui-devel >= 2.0.5
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	nautilus-devel >= 2.2.0
Requires:		gstreamer-colorspace >= 0.6.1
Requires:		gstreamer-avi
Requires:		gstreamer-mpeg
Requires:		gstreamer-mad
Requires:		gstreamer-vorbis
Requires:		gstreamer-oss
Requires:		gstreamer-xvideosink
Requires:		gstreamer-gnomevfs
Requires:		gstreamer-audio-effects
Requires:		gstreamer-GConf
Requires:		gstreamer-plugins
Requires:		gstreamer-play
Requires:		gstreamer >= 0.6.1
Requires(post):	/sbin/ldconfig
Requires(post):	%{_bindir}/gconftool-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GStreamer Multimedia Player.

%description -l pl
Odtwarzacz multimedialny GStreamer.

%package devel
Summary:	GStreamer Multimedia Player development files
Summary(pl):	Pliki programistyczne odtwarzacza multimedialnego GStreamer
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
GStreamer Multimedia Player development files.

%description devel -l pl
Pliki programistyczne odtwarzacza multimedialnego GStreamer.

%package nautilus
Summary:        GStreamer nautilus view
Summary(pl):	Widok GStreamer dla nautilusa
Group:          Libraries/Multimedia
Requires:       gstreamer-player = %{version}
Requires:       nautilus >= 2.2.0

%description nautilus
GStreamer nautilus view for media files.

%description nautilus -l pl
Widok GStreamer do nautilusa dla plików multimedialnych.

%prep
%setup -q -n %{gstname}-%{version}

%build
%configure \
    --disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

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
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_datadir}/application-registry/*
%{_datadir}/applications/*
%dir %{_datadir}/%{gstname}
%dir %{_datadir}/%{gstname}/ui
%{_datadir}/%{gstname}/ui/*
%{_datadir}/mime-info/*
%{_pixmapsdir}/*
%{_mandir}/man?/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/%{gstname}-%{version}

%files nautilus
%defattr(644,root,root,755)
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/%{gstname}-control
%attr(755,root,root) %{_libdir}/%{gstname}-view
%{_datadir}/gnome-2.0/ui/%{gstname}-view-ui.xml
