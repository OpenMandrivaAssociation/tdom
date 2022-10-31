Summary:	A XML/DOM/XPath/XSLT Implementation for Tcl
Name:		tdom
Version:	0.9.3
Release:	1
License:	MPLv1.1
Group:		System/Libraries
Url:		https://core.tcl.tk/tdom/timeline
Source0:	https://core.tcl.tk/tdom/tarball#/tdom-%{version}.tar.gz
Patch2:		tdom-tnc.patch
BuildRequires:	tcl-tcllib
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(expat)

%description
tDOM combines high performance XML data processing with easy and
powerful Tcl scripting functionality. tDOM should be one of the fastest
ways to manipulate XML with a scripting language and uses very few
memory: for example, the DOM tree of the XML recommendation in XML
(160K) needs only about 450K of memory.

%files
%doc ChangeLog CHANGES README NPL-1_1Final.html LICENSE
%{_libdir}/*.so
%{tcl_sitearch}/%{name}%{version}/
%{tcl_sitearch}/tnc0.3.0/
%{_mandir}/mann/*.n.*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for tDOM
Group:		Development/Other
Requires:	tcl-devel
Requires:	%{name} = %{EVRD}

%description devel
This package contains files for developing software based on tDOM.

%files devel
%{_libdir}/tdomConfig.sh
%{_libdir}/*.a
%{_includedir}/tdom.h

#----------------------------------------------------------------------------

%prep
%autosetup -p0 -c -n tDOM-%{version}

%build
autoreconf --force
mkdir build
cd build
CFLAGS="%{optflags} -DUSE_INTERP_ERRORLINE" ../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--with-tcl=%{tcl_sitearch} \
	--disable-tdomalloc \
	--with-expat
%make
cd ../extensions/tnc
autoreconf --force
CFLAGS="%{optflags}" ./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--with-tcl=%{tcl_sitearch} \
	--with-tdom=../../build
%make

%install
%makeinstall_std pkglibdir=%{tcl_sitearch}/%{name}%{version} -C build
%makeinstall_std pkglibdir=%{tcl_sitearch}/tnc0.3.0 -C extensions/tnc

mv %{buildroot}%{_libdir}/lib%{name}%{version}.so %{buildroot}%{tcl_sitearch}/%{name}%{version}/
ln -s tcl%{tcl_version}/%{name}%{version}/lib%{name}%{version}.so %{buildroot}%{_libdir}/lib%{name}%{version}.so

mv %{buildroot}%{_libdir}/libtnc0.3.0.so %{buildroot}%{tcl_sitearch}/tnc0.3.0/
ln -s tcl%{tcl_version}/tnc0.3.0/libtnc0.3.0.so %{buildroot}%{_libdir}/libtnc0.3.0.so

chmod 644 %{buildroot}%{_libdir}/*.a

