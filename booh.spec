%define name    booh
%define version 0.8.6
%define release %mkrel 5
%define	title       Booh
%define	longtitle   Web-Album generator

%{expand:%%define ruby_libdir %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{expand:%%define ruby_archdir %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Web-Album generator
License:        GPL
Group:          Graphics
URL:            http://www.booh.org
Source:         http://www.booh.org/packages/%{name}-%{version}.tar.bz2
Patch0:         %{name}-0.8.6.fixedruby.patch
Patch1:         %{name}-0.8.6.gtkfix.patch
Patch2:		%{name}-0.8.6.original_size.patch
Requires:       ruby >= 1.8
Requires:       ruby-gtk2 >= 0.12
Requires:       ruby-gettext >= 0.8.0
Requires:       mencoder
Requires:       ImageMagick
BuildRequires:  ruby-devel
BuildRequires:  ruby-gnome2-devel
BuildRequires:  gettext
BuildRequires:  ImageMagick
#BuildRequires:  gdk-pixbuf-devel 
BuildRoot:      %{_tmppath}/%{name}-%{version}


%description
Yet another Web-Album generator. Highlights:

  * automatic rotation of portrait images thanks to information
    put by digital camera in .jpg file
  * immediate display of images (preloading in browser)
  * keep position of "next/previous" hyperlinks in browser
    between images
  * advanced video support (thumbnailing etc)
  * clever use of the whole space of a typical browser window
    (the need to scroll portrait images is stupid)
  * themability
  * sub-albums support
  * remember your preferred size of thumbnails accross sub-albums
  * multi-processor support
  * a GUI to input captions, rotate, reorder and remove
    images FAST (extensive use of keyboard shortcuts)

%prep
rm -rf %buildroot
%setup -q
%patch0 -p 1
%patch1 -p 1
%patch2 -p 1

%build
ruby setup.rb config
ruby setup.rb setup
cd ext
ruby extconf.rb
make

%install
rm -rf %buildroot
ruby setup.rb install --prefix=%buildroot
cd ext
make install DESTDIR=%buildroot libdir=%buildroot%{_libdir} archdir=%buildroot%ruby_archdir
cd ..

mkdir -p %{buildroot}%{_menudir}
cat << "EOF" > %{buildroot}%{_menudir}/%{name}
?package(%{name}): \
    needs=X11 \
    section=Multimedia/Graphics \
    command="%{_bindir}/booh" \
    icon="booh.png" \
    title="%{title}" \
    longtitle="%{longtitle}" \
    xdg="true"
EOF

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/booh
Icon=booh
Terminal=false
Type=Application
StartupNotify=false
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics;Photography;
EOF

# icons
mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_liconsdir}
cp icons/booh-16x16.png %{buildroot}%{_miconsdir}/%{name}.png
cp icons/booh-32x32.png %{buildroot}%{_iconsdir}/%{name}.png
cp icons/booh-48x48.png %{buildroot}%{_liconsdir}/%{name}.png

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{name}.bash-completion %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%find_lang %name --all-name 

%post
%{update_menus}

%postun 
%{clean_menus}

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-, root, root)
%doc README
%{_bindir}/*
%{ruby_libdir}/%{name}*
%{ruby_archdir}/*
%{_datadir}/%{name}
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/*/*
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
