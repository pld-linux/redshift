Summary:	Adjusts the color temperature of your screen according to time of day
Name:		redshift
Version:	1.9.1
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://launchpad.net/redshift/trunk/%{version}/+download/%{name}-%{version}.tar.xz
# Source0-md5:	4c5dd6ea043116f9c15a9d5ec4c608de
# Remove Ubuntu specific geoclue provider
Patch0:		%{name}-geoclue-provider.patch
# https://bugs.launchpad.net/redshift/+bug/888661
# http://bazaar.launchpad.net/~jonls/redshift/trunk/revision/165
URL:		http://jonls.dk/redshift/
BuildRequires:	GConf2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	geoclue-devel
BuildRequires:	gettext-tools
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 3.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires:	python3 >= 3.2
Requires:	python3-pyxdg
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
Requires:	python-pygtk-gtk
Requires:	python-pyxdg
Obsoletes:	gtk-redshift

%description -n %{name}-gtk
This package provides GTK integration for Redshift, a screen color
temperature adjustment program.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,^#!.*python,#!%{__python},' src/redshift-gtk/redshift-gtk.in

%build
%configure \
	--disable-silent-rules
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
%doc DESIGN HACKING NEWS README README-colorramp
%attr(755,root,root) %{_bindir}/redshift
%{_mandir}/man1/redshift.1*

%files -n %{name}-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/redshift-gtk
%{py3_sitescriptdir}/redshift_gtk
%{_iconsdir}/hicolor/scalable/apps/redshift*.svg
%{_desktopdir}/redshift-gtk.desktop
%{systemduserunitdir}/redshift.service
%{systemduserunitdir}/redshift-gtk.service
