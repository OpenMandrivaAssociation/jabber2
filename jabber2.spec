%define pkgname         jabberd
%define name		jabber2
%define version		2.2.11
%define release		%mkrel 6

Summary:		OpenSource server implementation of the Jabber protocols
Name:			%name
Version:		%version
Release:		%release
License:		GPLv2+
Group:			System/Servers
BuildRoot: 		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:			http://codex.xiaoka.com/wiki/jabberd2:start
Source0:		http://codex.xiaoka.com/pub/jabberd2/releases/%{pkgname}-%{version}.tar.bz2
Source1:		%{pkgname}.rc
Source2:		%{pkgname}.sysconfig
Source3:		%{pkgname}.logrotate
Patch0:			%{pkgname}-2.2.8-fix-pid-path.patch
Patch1:			%{pkgname}-2.2.9-fix-log-path.patch
Patch2:			%{pkgname}-2.2.11-fix-pem-path.patch
Patch3:			%{pkgname}-2.2.11-fix-template-path.patch
Patch4:			%{pkgname}-2.2.11-fix-router-path.patch
Patch5:			%{pkgname}-2.2.11-fix-module-filename.patch
BuildRequires:		libgc-devel
BuildRequires:		libpq-devel
BuildRequires:		openssl-devel
BuildRequires:		glibc-devel 
BuildRequires:          zlib-devel
BuildRequires:		idn-devel
BuildRequires:		expat-devel
BuildRequires:          libgsasl-devel
Buildrequires:		udns-devel
%{!?_without_pam:BuildRequires: pam-devel}
%{!?_without_sqlite:BuildRequires: sqlite3-devel}
%{!?_without_db4:BuildRequires: db-devel}
%{!?_without_ldap:BuildRequires: openldap-devel}
%{!?_without_mysql:BuildRequires: mysql-devel}
%{!?_without_postgresql:BuildRequires: postgresql-devel}

Conflicts:		jabber
Requires(post,preun):	rpm-helper
Requires(pre,postun):	rpm-helper

%description
The jabberd project aims to provide an open-source server implementation of the
Jabber protocols for instant messaging and XML routing. The goal of this
project is to provide a scalable, reliable, efficient and extensible server
that provides a complete set of features and is up to date with the latest
protocol revisions.
jabberd 2 is the next generation of the jabberd server. It has been rewritten
from the ground up to be scalable, architecturally sound, and to support the
latest protocol extensions coming out of the JSF.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p0

%build
autoreconf -f -i
%serverbuild

%configure2_5x \
	%{!?_without_pam:--enable-pam} \
	%{?_without_pam:--disable-pam} \
	%{!?_without_db4:--enable-db} \
	%{?_without_db4:--disable-db} \
	%{!?_without_mysql:--enable-mysql} \
	%{?_without_mysql:--disable-mysql} \
	%{!?_without_ldap:--enable-ldap} \
	%{?_without_ldap:--disable-ldap} \
	%{!?_without_postgresql:--enable-pgsql} \
	%{?_without_postgresql:--disable-pgsql} \
	%{!?_without_sqlite:--enable-sqlite} \
	%{?_without_sqlite:--disable-sqlite} \
	--localstatedir=%{_var}/lib \
	--enable-fs --enable-anon --enable-pipe --enable-ssl \
	--with-sasl=gsasl --enable-debug --enable-mio=poll

%make

%install
rm -rf %buildroot
%makeinstall_std

# create needed directories 
mkdir -p %{buildroot}%{_var}/run/%{pkgname}
mkdir -p %{buildroot}%{_var}/lib/%{pkgname}/{db,stats}
mkdir -p %{buildroot}%{_var}/log/%{pkgname}
mkdir -p %{buildroot}%{_sysconfdir}/%{pkgname}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/{sysconfig,logrotate.d}

# install the initscript
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/%{pkgname}

# install the sysconfig file
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{pkgname}

# install the logrotate file
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{pkgname}

# and move some conf files to /etc/jabberd
mv %{buildroot}%{_sysconfdir}/{*.xml,*.cfg,*.dist,templates} %{buildroot}%{_sysconfdir}/%{pkgname}

# prepare to doc .dist files
mkdir examples
mv %{buildroot}%{_sysconfdir}/%{pkgname}/{*.dist,templates/*.dist} examples

# we have our own start script
rm -f %{buildroot}%{_bindir}/%{pkgname}
rm -f %{buildroot}%{_sysconfdir}/%{pkgname}/%{pkgname}.cfg*

# remove unused devel files
rm -f %{buildroot}%{_libdir}/%{pkgname}/*.la

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd %{pkgname} %{_var}/lib/%{pkgname} /bin/sh

%preun
%_preun_service %{pkgname}

%post
%_post_service %{pkgname}

%postun
%_postun_userdel %{pkgname}

%files
%defattr (0755,root,root,0755)
%_bindir/*
%_initrddir/%{pkgname}
%_libdir/%{pkgname}
%defattr (0644,root,root,0755)
%doc COPYING README INSTALL ChangeLog AUTHORS NEWS TODO
%doc tools/db-setup.mysql tools/db-setup.pgsql
%doc tools/*.pl examples
%{_sysconfdir}/logrotate.d/%{pkgname}
%{_sysconfdir}/sysconfig/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}
%config(noreplace) %{_sysconfdir}/%{pkgname}/c2s.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/router-users.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/router.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/router-filter.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/s2s.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/sm.xml
%config(noreplace) %{_sysconfdir}/%{pkgname}/templates/roster.xml
%{_mandir}/man8/*
%defattr (0644,jabberd,jabberd,755)
%{_var}/run/%{pkgname}
%{_var}/lib/%{pkgname}
%{_logdir}/%{pkgname}

