
%define gstname gst-player

Summary:	GStreamer Multimedia Player
Name:		gstreamer-player
Version:	0.4.1
Release:	1
License:	GPL
Group:		X11/Multimedia
Source0:	http://gstreamer.net/releases/current/src/%{gstname}-%{version}.tar.gz
URL:		http://gstreamer.net/
BuildRequires:	gstreamer-plugins-devel >= 0.4.0.2
BuildRequires:	libgnomeui-devel >= 2.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir /etc/X11/GNOME2

%description
GStreamer Multimedia Player.

%package devel
Summary:	GStreamer Multimedia Player development files
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
GStreamer Multimedia Player development files.

%prep
%setup -q -n %{gstname}-%{version}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
GCONF_CONFIG_SOURCE="`%{_bindir}/gconftool-2 --get-default-source`" \
%{_bindir}/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null 

%postun	
/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog
%config %{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%attr(755,root,root) %{_libdir}/*.la
%{_libdir}/bonobo/servers/*
%{_datadir}/application-registry/*
%{_datadir}/applications/*
%{_datadir}/%{gstname}/ui/*
%{_datadir}/mime-info/*
%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*
%attr(755,root,root) %{_libdir}/*.la
%{_includedir}/%{gstname}-%{version}
%{_pkgconfigdir}/*.pc
