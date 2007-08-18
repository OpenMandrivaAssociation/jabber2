%define pkgname         jabberd
%define name		jabber2
%define version		2.1.14
%define release		%mkrel 1
%define __libtoolize    /bin/true
%define libname		%mklibname %{pkgname} 0

%define Summary		Jabber is an instant messaging System

Summary:		%Summary
Name:			%name
Version:		%version
Release:		%release
License:		GPL
Group:			System/Servers
URL:			http://jabberd2.xiaoka.com/
Source0:		http://ftp.xiaoka.com/jabberd2/releases/%{pkgname}-%version.tar.bz2
Source1:		%{pkgname}.rc
BuildRequires:		postgresql-devel 
BuildRequires:          mysql-devel
BuildRequires:		openldap-devel 
BuildRequires:          pam-devel 
BuildRequires:          libsasl-devel
BuildRequires:		openssl-devel
BuildRequires:		glibc-devel 
BuildRequires:          zlib-devel
BuildRequires:		idn-devel
BuildRequires:          db4-devel
Conflicts:		jabber
Requires(post,preun):	rpm-helper
Requires(pre,postun):	rpm-helper
Requires:		%libname = %verison-%release

%description
Jabber is an instant messaging System, similar to ICQ or AIM, yet far
different.
It is open source, absolutely free, simple, fast, extensible, modularized,
cross platform, and created with the future in mind. Jabber has been
designed from the ground up to serve the needs of the end user, satisfy
business demands, and maintain compatibility with other messaging systems.

%package -n %{libname}
Summary:	Library files for jabber2
Group:		System/Libraries

%description -n %{libname}
This package contains library files needed for running jabber2.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%serverbuild
%configure2_5x	--enable-pgsql=yes \
		--enable-db=yes \
		--enable-ldap=yes \
		--enable-pam=yes \
		--with-extra-include-path=/usr/include/pgsql \
		--enable-ipv6=yes \
		--enable-sasl=cyrus \
		--enable-debug
		

%make

%install
rm -rf %buildroot
%makeinstall_std

mkdir -p %buildroot%{_sysconfdir}/jabberd
mv %buildroot%{_sysconfdir}/{*.xml,*.cfg,*.dist,templates} %buildroot%{_sysconfdir}/jabberd

install -D %{SOURCE1} ${RPM_BUILD_ROOT}%_initrddir/%{pkgname}

mkdir -p ${RPM_BUILD_ROOT}%{_var}/run/%{pkgname}

# remove unused devel files
rm -f %buildroot%_libdir/%{pkgname}/{*.la,mod_*.so}

%pre
%_pre_useradd %{pkgname} /var/run/%{pkgname} /bin/sh

%preun
%_preun_service %{pkgname}

%post
%_post_service %{pkgname}

%postun
%_postun_userdel %{pkgname}

%clean
rm -rf %buildroot

%files
%defattr (0755,root,root,0755)
%_bindir/c2s
%_bindir/jabberd
%_bindir/resolver
%_bindir/router
%_bindir/s2s
%_bindir/sm
%_initrddir/%{pkgname}

%defattr (0644,root,root,0755)
%doc COPYING README INSTALL ChangeLog AUTHORS NEWS PROTOCOL TODO tools/db-setup.mysql tools/db-setup.pgsql tools/migrate.pl tools/pipe-auth.pl
%dir %{_sysconfdir}/%{pkgname}
%config(noreplace) %{_sysconfdir}/%{pkgname}/c2s.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/resolver.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/router-users.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/router.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/router-filter.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/s2s.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/sm.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/jabberd.cfg
%config(noreplace) %{_sysconfdir}/%{pkgname}/templates/roster.xml
%{_sysconfdir}/%{pkgname}/*.dist
%{_sysconfdir}/%{pkgname}/templates/*.dist

%{_mandir}/man8/c2s.*
%{_mandir}/man8/jabberd.*
%{_mandir}/man8/resolver.*
%{_mandir}/man8/router.*
%{_mandir}/man8/s2s.*
%{_mandir}/man8/sm.*

%defattr (0644,jabberd,jabberd,755)
%{_var}/run/%{pkgname}

%files -n %{libname}
%_libdir/%{pkgname}
