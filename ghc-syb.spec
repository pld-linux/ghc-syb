#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	syb
Summary:	Scrab Your Boilerplate generics system
Summary(pl.UTF-8):	System generyczny Scrab Your Boilerplate
Name:		ghc-%{pkgname}
Version:	0.7.1
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/syb
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	8b4330cc60f6f61efc2a937e4658d0f5
URL:		http://hackage.haskell.org/package/syb
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.0
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3}
BuildRequires:	ghc-base-prof >= 4.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc >= 6.12.3
Requires:	ghc-base >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package contains the generics system described in the Scrap Your
Boilerplate papers (see
<http://www.cs.uu.nl/wiki/GenericProgramming/SYB>). It defines the
Data class of types permitting folding and unfolding of constructor
applications, instances of this class for primitive types, and a
variety of traversals.

%description -l pl.UTF-8
Ten pakiet zawiera system generyczny opisany w dokumencie "Scrap Your
Boilerplate" (p. <http://www.cs.uu.nl/wiki/GenericProgramming/SYB>).
Definiuje on klasę Data typów pozwalających na zwijanie i rozwijanie
aplikacji konstruktorów, instancje tej klasy dla typów prostych oraz
różne przejścia.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.0

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSsyb-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSsyb-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSsyb-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSsyb-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/SYB/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
