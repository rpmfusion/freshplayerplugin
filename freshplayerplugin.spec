%undefine __cmake_in_source_build

Name:       freshplayerplugin
Version:    0.3.11
Release:    7%{?dist}
Summary:    PPAPI-host NPAPI-plugin adapter

License:    MIT
URL:        https://github.com/i-rinat/%{name}
Source0:    %url/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake3
BuildRequires: make
BuildRequires: ragel
BuildRequires: glib2-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel
BuildRequires: pango-devel
BuildRequires: libX11-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: libconfig-devel
BuildRequires: libevent-devel
BuildRequires: freetype-devel
BuildRequires: cairo-devel
BuildRequires: gtk2-devel
BuildRequires: uriparser-devel
BuildRequires: openssl-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: soxr-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel

BuildRequires: ffmpeg-devel
BuildRequires: libv4l-devel
Requires: mozilla-filesystem

%description
As you know, Adobe have suspended further development of Flash player plugin
for GNU/Linux. Latest available as an NPAPI plugin version 11.2 will get
security updates for five years (since its release on May 4th, 2012), but
further development have been ceased.
Fortunately or not, newer versions are still available for Linux as a part of
Chrome browser, where Flash comes bundled in a form of PPAPI plugin. PPAPI or
Pepper Plugin API is an interface promoted by Chromium/Chrome team for browser
plugins.
It's NPAPI-inspired yet significantly different API which have every
conceivable function plugin may want. Two-dimensional graphics, OpenGL ES,
font rendering, network access, audio, and so on.
It's huge, there are 107 groups of functions, called interfaces which today's
Chromium browser offers to plugins.
And specs are not final yet. Interfaces are changing, newer versions are
arising, older ones are getting deleted. For various reasons Firefox
developers are not interested now in implementing PPAPI in Firefox.
However that does not mean it cannot be done.
The main goal of this project is to get PPAPI (Pepper) Flash player working
in Firefox. This can be done in two ways. First one is to implement full PPAPI
interface in Firefox itself.
Other one is to implement a wrapper, some kind of adapter which will look like
browser to PPAPI plugin and look like NPAPI plugin for browser.
First approach requires strong knowledge of Firefox internals,and moreover
additional effort to get the code into mainstream.
Maintaining a set of patches doesn't look like a good idea.
Second approach allows to concentrate on two APIs only.
Yes one of them is big, but still graspable.
Second way will be used for the project. It will benefit other browsers too,
not only Firefox.

%prep
%autosetup -p1
# Disable 3D (because some intel graphics i915 and others display slow videos)
#sed -i 's|enable_3d = 1|enable_3d = 0|g' data/freshwrapper.conf.example
#sed -i 's|enable_3d           =      1,|enable_3d           =      0,|g' src/config.c

# https://github.com/i-rinat/freshplayerplugin/issues/380
sed -i 's|include_directories("${CMAKE_BINARY_DIR}")|include_directories("${CMAKE_BINARY_DIR}")\ninclude_directories("/usr/include/alsa")|' \
    CMakeLists.txt


%build
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_SKIP_RPATH=true
%cmake3_build

%install
%cmake3_install
install -Dm 0644 data/freshwrapper.conf.example %{buildroot}/etc/freshwrapper.conf

%files
%doc ChangeLog README.md doc/*
%license LICENSE
%{_libdir}/mozilla/plugins/libfreshwrapper-flashplayer.so
%config(noreplace) %{_sysconfdir}/freshwrapper.conf

%changelog
* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 0.3.11-6
- Rebuilt for new ffmpeg snapshot

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.11-4
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 0.3.11-2
- Rebuild for new ffmpeg version

* Mon May 27 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-1
- Update to 0.3.11

* Mon Mar 18 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.10-1
- Update to 0.3.10

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.9-3
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.9-1
- Update  to 0.3.9

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.7-5
- Rebuilt for ffmpeg-3.5 git

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.3.7-4
- Update to VA-API 1.0.0

* Fri Sep 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.3.7-3
- Add build requires mesa-libGL-devel

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Sérgio Basto <sergio@serjux.com> - 0.3.7-1
- Update  to 0.3.7, rfbz #4551
- sed already upstreamed

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.3.6-4
- Rebuild for ffmpeg update

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.6-2
- bz#4411 Add Adobe PPAPI directory to search list (from flash-player-ppapi

* Fri Oct 07 2016 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.6-1
- Upgrade to 0.3.6

* Wed Aug 31 2016 Sérgio Basto <sergio@serjux.com> - 0.3.5-3
- Clean spec, Vascom patches series, rfbz #4192
- Reorder BR to match with unitedrpms
- Add possibility to disable 3D

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.3.5-2
- Rebuilt for ffmpeg-3.1.1

* Tue Jul 12 2016 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.5-1
- Upgrade to 0.3.5

* Tue Jan 05 2016 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.4-1
- Upgrade to 0.3.4

* Thu Nov 12 2015 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.3-1
- Update to 0.3.3
- Added install rule to cmake (patch from sergio@serjux.com)

* Tue Sep 29 2015 Sérgio Basto <sergio@serjux.com> - 0.3.2-2
- Removed Requires it is a shared library, so requires will be automatic.

* Tue Sep 22 2015 Sérgio Basto <sergio@serjux.com> - 0.3.2-1
- Some fixes and merged some of the work of postinstallerf.

* Mon Sep 21 2015 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.2-0
- Initial RPM Fusion package based on retired 'dacr' package (Fedora Copr)

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.1-20150810-acb0ee4-1
- Updated to 0.3.1-20150810-acb0ee4
