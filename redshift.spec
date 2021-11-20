Summary:	Adjusts the color temperature of your screen according to time of day
Name:		redshift
Version:	1.12
Release:	5
License:	GPL v3+
Group:		Applications/System
Source0:	https://github.com/jonls/redshift/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	5d04f2413dacdf3434cb86f373842462
URL:		http://jonls.dk/redshift/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	intltool >= 0.50
BuildRequires:	libdrm-devel
BuildRequires:	libtool
BuildRequires:	libxcb-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 3.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Redshift adjusts the color temperature of your screen according to
your surroundings. This may help your eyes hurt less if you are
working in front of the screen at night.

The color temperature is set according to the position of the sun. A
different color temperature is set during night and daytime. During
twilight and early morning, the color temperature transitions smoothly
from night to daytime temperature to allow your eyes to slowly adapt.

This package provides the base program.

%package -n %{name}-gtk
Summary:	GTK integration for Redshift
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+3
Requires:	python3 >= 3.2
Requires:	python3-pyxdg
Obsoletes:	gtk-redshift

%description -n %{name}-gtk
This package provides GTK integration for Redshift, a screen color
temperature adjustment program.

%prep
%setup -q

%{__sed} -i -e '1s,^#!.*python3,#!%{__python3},' src/redshift-gtk/redshift-gtk.in

%build
%{__gettextize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	am_cv_python_pythondir=%{py3_sitescriptdir} \
	--disable-silent-rules \
	--enable-drm \
	--enable-geoclue \
	--enable-geoclue2 \
	--enable-gui \
	--enable-randr \
	--enable-vidmode \
	--with-systemduserunitdir=%{systemduserunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%find_lang %{name}
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/redshift-gtk.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{name}-gtk
%update_icon_cache hicolor

%postun -n %{name}-gtk
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CONTRIBUTING.md DESIGN NEWS README README-colorramp redshift.conf.sample
%attr(755,root,root) %{_bindir}/redshift
%{_mandir}/man1/redshift.1*

%files -n %{name}-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/redshift-gtk
%{_datadir}/appdata/redshift-gtk.appdata.xml
%{py3_sitescriptdir}/redshift_gtk
%{_iconsdir}/hicolor/scalable/apps/redshift*.svg
%{_desktopdir}/redshift.desktop
%{_desktopdir}/redshift-gtk.desktop
%{systemduserunitdir}/redshift.service
%{systemduserunitdir}/redshift-gtk.service
