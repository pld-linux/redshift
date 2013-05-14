Summary:	Adjusts the color temperature of your screen according to time of day
Name:		redshift
Version:	1.7
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://launchpad.net/redshift/trunk/%{version}/+download/%{name}-%{version}.tar.bz2
# Source0-md5:	c56512afa292b5a94b715ed4a1841d4c
# Remove Ubuntu specific geoclue provider
Patch0:		%{name}-geoclue-provider.patch
# https://bugs.launchpad.net/redshift/+bug/888661
# http://bazaar.launchpad.net/~jonls/redshift/trunk/revision/165
Patch1:		%{name}-geoclue-client-check.patch
URL:		http://jonls.dk/redshift/
BuildRequires:	GConf2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	geoclue-devel
BuildRequires:	gettext-devel
BuildRequires:	sed >= 4.0
BuildRequires:	python
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xorg-lib-libXrandr-devel
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

%package -n gtk-%{name}
Summary:	GTK integration for Redshift
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-gtk
Requires:	python-pyxdg

%description -n gtk-%{name}
This package provides GTK integration for Redshift, a screen color
temperature adjustment program.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%{__sed} -i -e '1s,^#!.*python,#!%{__python},' src/gtk-redshift/gtk-redshift

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
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/gtk-redshift.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post -n gtk-%{name}
%update_icon_cache hicolor

%postun -n gtk-%{name}
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/redshift
%{_mandir}/man1/redshift.1*

%files -n gtk-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gtk-redshift
%{py_sitescriptdir}/gtk_redshift
%{_iconsdir}/hicolor/scalable/apps/redshift*.svg
%{_desktopdir}/gtk-redshift.desktop
