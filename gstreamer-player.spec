
%define 	gstname 	gst-player

Summary:	GStreamer Multimedia Player
Summary(pl):	Odtwarzacz multimedialny GStreamer
Name:		gstreamer-player
Version:	0.4.2
Release:	1
License:	GPL
Group:		X11/Multimedia
Source0:	http://gstreamer.net/releases/current/src/%{gstname}-%{version}.tar.gz
URL:		http://gstreamer.net/
BuildRequires:	gstreamer-plugins-devel >= 0.4.2-2
BuildRequires:	libgnomeui-devel >= 2.0.5
Requires(post):	/sbin/ldconfig
Requires(post):	/usr/X11R6/bin/gconftool-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir /etc/X11/GNOME2

%description
GStreamer Multimedia Player.

%description -l pl
Odtwarzacz multimedialny GStreamer.

%package devel
Summary:	GStreamer Multimedia Player development files
Summary(pl):	Pliki programistyczne odtwarzacza multimedialnego GStreamer
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
GStreamer Multimedia Player development files.

%description devel -l pl
Pliki programistyczne odtwarzacza multimedialnego GStreamer.

%prep
%setup -q -n %{gstname}-%{version}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
GCONF_CONFIG_SOURCE="`/usr/X11R6/bin/gconftool-2 --get-default-source`" \
/usr/X11R6/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null 

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog
%config %{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%{_libdir}/*.la
%attr(755,root,root) %{_libdir}/%{gstname}-control
%attr(755,root,root) %{_libdir}/%{gstname}-view
%{_libdir}/bonobo/servers/*
%{_datadir}/application-registry/*
%{_datadir}/applications/*
%dir %{_datadir}/%{gstname}
%dir %{_datadir}/%{gstname}/ui
%{_datadir}/%{gstname}/ui/*
%{_datadir}/mime-info/*
%{_datadir}/gnome-2.0/ui/*
%{_pixmapsdir}/*
%{_mandir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/%{gstname}-%{version}
#%{_pkgconfigdir}/*.pc
