Summary:	GCC and related tools for Palm OS development
Summary(pl):	GCC i zwi±zane z nim narzêdzia do programowania pod Palm OS
Name:		prc-tools
Version:	2.2
%define	bver	2.12.1
%define	dver	5.0
%define	cver	2.95.3
%define	mver	3.79.1
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/prc-tools/%{name}-%{version}.tar.gz
# Source0-md5:	91a9a04d2042fcf673ff212a3ffd7ab9
Source1:	ftp://sources.redhat.com/pub/binutils/releases/binutils-%{bver}.tar.bz2
# Source1-md5:	f67fe2e8065c5683bc34782de131f5d3
Source2:	ftp://sourceware.cygnus.com/pub/gdb/old-releases/gdb-%{dver}.tar.bz2
# Source2-md5:	b2720def719fd024e380793d9084da2a
Source3:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{cver}/gcc-%{cver}.tar.bz2
# Source3-md5:	87ee083a830683e2aaa57463940a0c3c
Source4:	ftp://ftp.gnu.org/pub/gnu/make/make-%{mver}.tar.gz
# Source4-md5:	22ea95c125c7b80e04354d4ee4ae960d
URL:		http://prc-tools.sourceforge.net/
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# This is the canonical place to look for Palm OS-related header files and
# such on Unix-like file systems.
%define palmdev_prefix /opt/palmdev

%description
A complete compiler tool chain for building Palm OS applications in C
or C++. Includes (patched versions of) binutils %{bver}, GDB %{dver},
and GCC %{cver}, along with various post-linker tools to produce Palm
OS .prc files.

You will also need a Palm OS SDK and some way of creating resources,
such as PilRC.

%description -l pl
Kompletny zestaw narzêdzi kompilatora do budowania aplikacji pod Palm
OS w C lub C++. Zawiera zmodyfikowane wersje binutils %{bver}, GDB
%{dver} i GCC %{cver}, wraz z ró¿nymi narzêdziami postkonsolidacyjnymi
konsolidacji, aby stworzyæ pliki .prc dla Palm OS. Do tworzenia
niektórych zasobów, takich jak PilRC, potrzebny jest jeszcze Palm OS
SDK.

%package arm
Summary:	GCC and related tools for ARM targeted Palm OS development
Summary(pl):	GCC i zwi±zane z nim narzêdzia dla ARM do programowania pod Palm OS
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

%description arm -l pl
Zestaw narzêdzi kompilatora do budowania armletów Palm OS w C lub C++.
Zawiera zmodyfikowane wersje binutils %{bver} i GCC %{cver}, a wymaga
ró¿nych narzêdzi postkonsolidacyjnych z pakietu prc-tools.

Ta wersja narzêdzi ARM prc-tools nie dostarcza kodu startowego ani
innych subtelno¶ci - jako taka jest przydatna tylko do budowania
samodzielnych zasobów kodu, takich jak armlety.

%package htmldocs
Summary:	GCC, GDB, binutils, make, and prc-tools documentation as HTML
Summary(pl):	Dokumentacja GCC, GDB, binutils, make i prc-tools w HTML
Group:		Development/Tools

%description htmldocs
GCC, GDB, binutils, make, and general prc-tools documentation in HTML
format. The various native development packages and the main prc-tools
package, respectively, provide exactly this documentation in info
format. This optional package is for those who prefer HTML-formatted
documentation.

%description htmldocs -l pl
Dokumentacja do GCC, GDB, binutils, make i ogólna dla prc-tools w
formacie HTML. Ró¿ne pakiety do natywnego programowania oraz g³ówny
pakiet prc-tools udostêpniaj± tê sam± dokumentacjê w formacie info.
Ten opcjonalny pakiet jest dla preferuj±cych dokumentacjê w formacie
HTML.

%prep
%setup -q -n binutils-2.12.1 -T -b 1
%setup -q -n gdb-5.0 -T -b 2
%setup -q -n gcc-2.95.3 -T -b 3
%setup -q -n make-3.79.1 -T -b 4
%setup -q

cat *.palmos.diff | (cd .. && patch -p0)

mv ../binutils-2.12.1 binutils
mv ../gdb-5.0 gdb
mv ../gcc-2.95.3 gcc
mv ../make-3.79.1 make

# The patch touches a file this depends on, and you need autoconf to remake
# it.  There's no changes, so let's just touch it so people don't have to
# have autoconf installed.
touch gcc/gcc/cstamp-h.in

mkdir static-libs

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
  --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} --sbindir=%{_sbindir} --libexecdir=%{_libexecdir} \
  --localstatedir=%{_localstatedir} --sharedstatedir=%{_sharedstatedir} \
  --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} \
  --includedir=%{_includedir} --libdir=%{_libdir} \
  --mandir=%{_mandir} --infodir=%{_infodir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
	htmldir=$RPM_BUILD_ROOT%{palmdev_prefix}/doc

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
%attr(755,root,root) %{_bindir}/[b-z]*
%attr(755,root,root) %{_exec_prefix}/m68k*
%{_libdir}/gcc-lib/m68k*
%{_datadir}/prc-tools
# Native packages provide gcc.info* etc, so we limit ourselves to this one
%doc %{_infodir}/prc-tools*
# Similarly, the native packages have already provided equivalent manpages
#%doc %{_mandir}/man1/*

%files arm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/arm*
%attr(755,root,root) %{_exec_prefix}/arm*
%{_libdir}/gcc-lib/arm*

%files htmldocs
%defattr(644,root,root,755)
%doc %{palmdev_prefix}/doc
