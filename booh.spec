%define name    booh
%define version 0.9.2
%define release %mkrel 1
%define	title       Booh
%define	longtitle   Web-Album generator

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Web-Album generator
License:        GPLv2
Group:          Graphics
URL:            http://www.booh.org
Source:         http://www.booh.org/packages/%{name}-%{version}.tar.bz2
Requires:       ruby >= 1.8
Requires:       ruby-gtk2 >= 0.12
Requires:       ruby-gettext >= 0.8.0
Requires:       mplayer
Requires:       exif
Requires:       gimp
Requires:       imagemagick
BuildRequires:  ruby-devel
BuildRequires:  ruby-gnome2-devel
BuildRequires:  gettext
BuildRequires:  imagemagick
BuildRequires:  gdk-pixbuf-devel 
BuildRequires:  libexiv-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Yet another Web-Album generator. Highlights:

  * automatic rotation of portrait images thanks to information
    put by digital camera in .jpg file (EXIF)
  * immediate display of images (preloading in browser)
  * keep position of "next/previous" hyperlinks in browser
    between images
  * full video support (including thumbnailing)
  * clever use of the whole space of a typical browser window
    (the need to scroll portrait images is stupid)
  * themability
  * sub-albums support
  * remember your preferred size of thumbnails accross sub-albums
  * multi-processor support to speed up thumbnails generation
  * smooth integration of panoramic images in thumbnails pages
  * multi-languages web-album navigation (navigation links are
    automatically shown in user's language)
  * a GUI to input captions, rotate, reorder and remove
    images FAST (extensive use of keyboard shortcuts)
  * another GUI to classify photos and videos in a powerful manner

%prep
%setup -q

%build
ruby setup.rb config --rbdir=%ruby_vendorlibdir --sodir=%ruby_vendorarchdir
ruby setup.rb setup
cd ext
ruby extconf.rb --vendor
make

%install
rm -rf %buildroot
ruby setup.rb install --prefix=%buildroot
cd ext
make install DESTDIR=%buildroot libdir=%buildroot%{_libdir} archdir=%buildroot%ruby_sitearchdir
cd ..


install -d -m 755 %{buildroot}%{_datadir}/applications
install -m 644 desktop/booh.desktop %{buildroot}%{_datadir}/applications
install -m 644 desktop/booh-classifier.desktop %{buildroot}%{_datadir}/applications

perl -pi -e 's/^Icon=%{name}.*/Icon=%{name}/g' %{buildroot}%{_datadir}/applications/*

# icons
mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_liconsdir}
cp desktop/booh-16x16.png %{buildroot}%{_miconsdir}/%{name}.png
cp desktop/booh-32x32.png %{buildroot}%{_iconsdir}/%{name}.png
cp desktop/booh-48x48.png %{buildroot}%{_liconsdir}/%{name}.png

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{name}.bash-completion %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%find_lang %name --all-name 

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun 
%{clean_menus}
%endif

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-, root, root)
%doc README
%{_bindir}/*
%{ruby_vendorlibdir}/%{name}*
%{ruby_vendorarchdir}/*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-classifier.desktop
%{_mandir}/*/*
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
