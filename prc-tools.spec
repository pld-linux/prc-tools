Summary:	GCC and related tools for Palm OS development
Summary(pl.UTF-8):	GCC i związane z nim narzędzia do programowania pod Palm OS
Name:		prc-tools
Version:	2.3
%define	bver	2.14
%define	dver	5.3
%define	cver	3.3.1
%define	cver295	2.95.3
%define	mver	3.80
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/prc-tools/%{name}-%{version}.tar.gz
# Source0-md5:	038a42a71a984fee6f906abc85a032ec
Source1:	ftp://sources.redhat.com/pub/binutils/releases/binutils-%{bver}.tar.bz2
# Source1-md5:	2da8def15d28af3ec6af0982709ae90a
Source2:	ftp://ftp.gnu.org/pub/gnu/gdb/gdb-%{dver}.tar.gz
# Source2-md5:	1e8566325f222edfbdd93e40c6ae921b
Source3:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{cver}/gcc-%{cver}.tar.bz2
# Source3-md5:	1135a104e9fa36fdf7c663598fab5c40
Source4:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{cver295}/gcc-%{cver295}.tar.bz2
# Source4-md5:	87ee083a830683e2aaa57463940a0c3c
Source5:	ftp://ftp.gnu.org/pub/gnu/make/make-%{mver}.tar.gz
# Source5-md5:	c68540da9302a48068d5cce1f0099477
URL:		http://prc-tools.sourceforge.net/
BuildRequires:	texinfo
ExcludeArch:	amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# This is the canonical place to look for Palm OS-related header files and
# such on Unix-like file systems.
%define	palmdev_prefix		/opt/palmdev
%define	no_install_post_strip	1

%description
A complete compiler tool chain for building Palm OS applications in C
or C++. Includes (patched versions of) binutils %{bver}, GDB %{dver},
and GCC %{cver295}, along with various post-linker tools to produce Palm
OS .prc files.

You will also need a Palm OS SDK and some way of creating resources,
such as PilRC.

%description -l pl.UTF-8
Kompletny zestaw narzędzi kompilatora do budowania aplikacji pod Palm
OS w C lub C++. Zawiera zmodyfikowane wersje binutils %{bver}, GDB
%{dver} i GCC %{cver}, wraz z różnymi narzędziami postkonsolidacyjnymi
konsolidacji, aby stworzyć pliki .prc dla Palm OS. Do tworzenia
niektórych zasobów, takich jak PilRC, potrzebny jest jeszcze Palm OS
SDK.

%package arm
Summary:	GCC and related tools for ARM targeted Palm OS development
Summary(pl.UTF-8):	GCC i związane z nim narzędzia dla ARM do programowania pod Palm OS
Group:		Development/Tools
Requires:	prc-tools >= 2.2

%description arm
A compiler tool chain for building Palm OS armlets in C or C++.
Includes (patched versions of) binutils %{bver} and GCC %{cver}, and
requires the various post-linker tools from a corresponding prc-tools
package.

Note that this version of ARM prc-tools does not provide startup code
or other niceties: by itself, it is only useful for building
stand-alone code resources such as armlets.

%description arm -l pl.UTF-8
Zestaw narzędzi kompilatora do budowania armletów Palm OS w C lub C++.
Zawiera zmodyfikowane wersje binutils %{bver} i GCC %{cver}, a wymaga
różnych narzędzi postkonsolidacyjnych z pakietu prc-tools.

Ta wersja narzędzi ARM prc-tools nie dostarcza kodu startowego ani
innych subtelności - jako taka jest przydatna tylko do budowania
samodzielnych zasobów kodu, takich jak armlety.

%package htmldocs
Summary:	GCC, GDB, binutils, make, and prc-tools documentation as HTML
Summary(pl.UTF-8):	Dokumentacja GCC, GDB, binutils, make i prc-tools w HTML
Group:		Development/Tools

%description htmldocs
GCC, GDB, binutils, make, and general prc-tools documentation in HTML
format. The various native development packages and the main prc-tools
package, respectively, provide exactly this documentation in info
format. This optional package is for those who prefer HTML-formatted
documentation.

%description htmldocs -l pl.UTF-8
Dokumentacja do GCC, GDB, binutils, make i ogólna dla prc-tools w
formacie HTML. Różne pakiety do natywnego programowania oraz główny
pakiet prc-tools udostępniają tę samą dokumentację w formacie info.
Ten opcjonalny pakiet jest dla preferujących dokumentację w formacie
HTML.

%prep
%setup -q -n binutils-%{bver} -T -b 1
%setup -q -n gdb-%{dver} -T -b 2
%setup -q -n gcc-%{cver} -T -b 3
%setup -q -n gcc-%{cver295} -T -b 4
%setup -q -n make-%{mver} -T -b 5
%setup -q

cat 	binutils-%{bver}.palmos.diff \
	gdb-%{dver}.palmos.diff \
	gcc-%{cver}.palmos.diff \
	gcc-%{cver295}.palmos.diff \
	| (cd .. && patch -p0)

mv ../binutils-%{bver} binutils
mv ../gdb-%{dver} gdb
mv ../gcc-%{cver} gcc
mv ../gcc-%{cver295} gcc295

# The patch touches a file this depends on, and you need autoconf to remake
# it.  There's no changes, so let's just touch it so people don't have to
# have autoconf installed.
touch gcc/gcc/cstamp-h.in

install -d static-libs empty

%build
# Ensure that we link *statically* against the stdc++ library
rm -f static-libs/*
ln -s `${CXX:-g++} -print-file-name=libstdc++.a` static-libs/libstdc++.a

# The m68k target used to be 'm68k-palmos-coff'.  Some people may want to
# leave it thus to avoid changing their makefiles a little bit.

# We can't use %%configure because it insists on libtoolizing, which will
# likely break our config.sub.
LDFLAGS=-L`pwd`/static-libs ./configure \
	--enable-targets=m68k-palmos,arm-palmos \
	--enable-languages=c,c++ \
	--with-palmdev-prefix=%{palmdev_prefix} \
	--enable-html-docs=%{palmdev_prefix}/doc \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--disable-generic

%{__make} -j 1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -j 1 install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	tooldir=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	htmldir=$RPM_BUILD_ROOT%{palmdev_prefix}/doc

for i in arm-palmos m68k-palmos; do
for j in as ld; do
	ln -sf %{_bindir}/$i-$j $RPM_BUILD_ROOT%{_libdir}/gcc-lib/$i/$j
done;
done;

mv $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_exec_prefix}/arm-palmos/lib
mv $RPM_BUILD_ROOT%{_libdir}/mown-gp/*.a $RPM_BUILD_ROOT%{_exec_prefix}/m68k-palmos/lib
mv $RPM_BUILD_ROOT%{_includedir}/* $RPM_BUILD_ROOT%{_exec_prefix}/m68k-palmos/include

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%preun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	palmdev-prep --remove
fi

%preun arm
if [ "$1" = "0" ]; then
	rm -f %{_libdir}/gcc-lib/arm-palmos/specs
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/m68k*
%attr(755,root,root) %{_exec_prefix}/m68k*
%dir %{_libdir}/gcc-lib/m68k-palmos
%dir %{_libdir}/gcc-lib/m68k-palmos/%{cver295}-kgpd
%{_libdir}/gcc-lib/m68k-palmos/%{cver295}-kgpd/[ilms]*
%attr(755,root,root) %{_libdir}/gcc-lib/m68k-palmos/%{cver295}-kgpd/c*
%{_libdir}/gcc-lib/m68k-palmos/[al]*
%{_libdir}/ldscripts/m68k*
#%{_datadir}/prc-tools
# Native packages provide gcc.info* etc, so we limit ourselves to this one
#%doc %{_infodir}/prc-tools*
# Similarly, the native packages have already provided equivalent manpages
#%doc %{_mandir}/man1/*

%files arm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/arm*
%attr(755,root,root) %{_exec_prefix}/arm*
%dir %{_libdir}/gcc-lib/arm-palmos
%dir %{_libdir}/gcc-lib/arm-palmos/%{cver}
%{_libdir}/gcc-lib/arm-palmos/%{cver}/[tsli]*
%attr(755,root,root) %{_libdir}/gcc-lib/arm-palmos/%{cver}/cc*
%{_libdir}/gcc-lib/arm-palmos/[al]*
%{_libdir}/gcc-lib/arm-palmos/%{cver}/c[co]*
%{_libdir}/gcc-lib/arm-palmos/%{cver}/c*.o
%{_libdir}/ldscripts/arm*
%attr(755,root,root) %{_exec_prefix}/arm*

%files htmldocs
%defattr(644,root,root,755)
#%doc %{palmdev_prefix}/doc
