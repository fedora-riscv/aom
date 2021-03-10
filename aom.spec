# Force out of source build
%undefine __cmake_in_source_build

%global sover           2
# git describe
%global aom_version     v2.0.1

# Use commit with updated changelog for correct versioning
%global commit          b52ee6d44adaef8a08f6984390de050d64df9faa
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20201215
# %%global prerelease      1

%if 0%{?rhel} >= 8
%bcond_with vmaf
%else
%bcond_without vmaf
%endif

Name:       aom
Version:    2.0.1
Release:    5%{?prerelease:.%{snapshotdate}git%{shortcommit}}%{?dist}
Summary:    Royalty-free next-generation video format

License:    BSD
URL:        http://aomedia.org/
Source0:    https://aomedia.googlesource.com/%{name}/+archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  cmake3
BuildRequires:  doxygen
BuildRequires:  git-core
BuildRequires:  graphviz
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)
BuildRequires:  python3-devel
BuildRequires:  yasm
%if %{with vmaf}
%ifarch x86_64
BuildRequires:  pkgconfig(libvmaf)
%endif
%endif

Provides:       av1 = %{version}-%{release}
Requires:       libaom%{?_isa} = %{version}-%{release}

%description
The Alliance for Open Media’s focus is to deliver a next-generation
video format that is:

 - Interoperable and open;
 - Optimized for the Internet;
 - Scalable to any modern device at any bandwidth;
 - Designed with a low computational footprint and optimized for hardware;
 - Capable of consistent, highest-quality, real-time video delivery; and
 - Flexible for both commercial and non-commercial content, including
   user-generated content.

This package contains the reference encoder and decoder.

%package -n libaom
Summary:        Library files for aom

%description -n libaom
Library files for aom, the royalty-free next-generation
video format.

%package -n libaom-devel
Summary:        Development files for aom
Requires:       libaom%{?_isa} = %{version}-%{release}

%description -n libaom-devel
Development files for aom, the royalty-free next-generation
video format.

%prep
%autosetup -p1 -c %{name}-%{commit}
# Set GIT revision in version
sed -i 's@set(aom_version "")@set(aom_version "%{aom_version}")@' build/cmake/version.cmake
# Fix VMAF detection
sed -i 's@libvmaf\.a @@' CMakeLists.txt

%build
%ifarch %{arm}
%global optflags %{__global_compiler_flags} -march=armv7-a -mfpu=neon -mtune=cortex-a8 -mabi=aapcs-linux -mfloat-abi=hard
%endif

%cmake3 -DENABLE_CCACHE=1 \
        -DCMAKE_SKIP_RPATH=1 \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCONFIG_WEBM_IO=1 \
        -DENABLE_DOCS=1 \
        -DENABLE_TESTS=0 \
        -DCONFIG_ANALYZER=0 \
        -DCONFIG_SHARED=1 \
%if %{with vmaf}
%ifarch x86_64
        -DCONFIG_TUNE_VMAF=1 \
%endif
%endif
        %{nil}
%cmake3_build

%install
%cmake3_install
rm -rf %{buildroot}%{_libdir}/libaom.a

%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomdec
%{_bindir}/aomenc

%files -n libaom
%license LICENSE PATENTS
%{_libdir}/libaom.so.%{sover}*

%files -n libaom-devel
%doc %{_vpath_builddir}/docs/html/
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Mar 10 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.1-5
- Rebuild for new libvmaf version

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Wim Taymans <wtaymans@redhat.com> - 2.0.1-3
- Disable vmaf on rhel

* Tue Dec 15 01:26:44 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.1-2
- Disable tests

* Sat Dec 05 21:18:20 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.1-1
- Update to 2.0.1
- Close rhbz#1852847

* Tue Jul 28 16:30:33 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.0-3
- Fix FTBFS

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 14:33:18 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.0-1
- Update to 2.0.0 (#1852847)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9.20190810git9666276
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 17:45:23 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-8.20190810git9666276
- Update to commit 9666276accea505cd14cbcb9e3f7ff5033da9172

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7.20180925gitd0076f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6.20180925gitd0076f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-5.20180925gitd0076f5
- Update to commit d0076f507a6027455540e2e4f25f84ca38803e07
- Set CONFIG_LOWBITDEPTH to 1
- Fix #1632658

* Thu Sep 13 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-4
- Split the package into libs/tools

* Tue Sep 11 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-3
- Update the archive in order to detect the correct version from the changelog

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-1
- First RPM release

