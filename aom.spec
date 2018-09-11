%global sover           0

# Use commit with updated changelog for correct versioning
%global commit          0ddc150516b7672101265eac032a11a9aae4cb53
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20180911

Name:       aom
Version:    1.0.0
Release:    2%{?dist}
Summary:    Royalty-free next-generation video format

License:    BSD
URL:        http://aomedia.org/
# We want to keep the git data for versioning aom.pc correctly
# so we can't download the archive directly from the repo.
Source0:    %{name}-%{version}.tar.gz
Source1:    makesrc.sh

BuildRequires:  gcc
BuildRequires:  cmake3
BuildRequires:  doxygen
BuildRequires:  git-core
BuildRequires:  graphviz
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)
BuildRequires:  wxGTK3-devel
BuildRequires:  yasm

Provides:       av1 = %{version}-%{release}


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


%package devel
Summary:        Development files for aom
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for aom the royalty-free next-generation 
video format.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
mkdir _build && cd _build
%cmake3 ../ -DENABLE_CCACHE=1 \
            -DCMAKE_SKIP_RPATH=1 \
            -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%ifnarch aarch64 %{arm} %{ix86} x86_64
            -DAOM_TARGET_CPU=generic \
%endif
%ifarch %{arm}
            -DAOM_TARGET_CPU=arm \
%endif
%ifarch aarch64
            -DAOM_TARGET_CPU=arm64 \
%endif
%ifarch %{ix86}
            -DAOM_TARGET_CPU=x86 \
%endif
%ifarch x86_64
            -DAOM_TARGET_CPU=x86_64 \
%endif
            -DCONFIG_WEBM_IO=1 \
            -DENABLE_DOCS=1 \
            -DCONFIG_ANALYZER=1
%make_build


%install
cd _build
%make_install
install -pm 0755 examples/analyzer %{buildroot}%{_bindir}/aomanalyzer


%ldconfig_scriptlets


%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomanalyzer
%{_bindir}/aomdec
%{_bindir}/aomenc
%{_libdir}/libaom.so.%{sover}


%files devel
%doc _build/docs/html/
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Sep 11 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-2
- Update the archive in order to detect the correct version from the changelog

* Wed Mar 07 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-1
- First RPM release

