%define pkgname         jabberd
%define name		jabber2
%define version		2.2.16
%define release		2

Summary:		OpenSource server implementation of the Jabber protocols
Name:			%name
Version:		%version
Release:		%release
License:		GPLv2+
Group:			System/Servers
URL:			http://codex.xiaoka.com/wiki/jabberd2:start
Source0:		http://codex.xiaoka.com/pub/jabberd2/releases/%{pkgname}-%{version}.tar.gz
Source1:		%{pkgname}.rc
Source2:		%{pkgname}.sysconfig
Source3:		%{pkgname}.logrotate
Patch0:			%{pkgname}-2.2.8-fix-pid-path.patch
Patch1:			%{pkgname}-2.2.9-fix-log-path.patch
Patch2:			%{pkgname}-2.2.11-fix-pem-path.patch
Patch3:			%{pkgname}-2.2.11-fix-template-path.patch
Patch4:			%{pkgname}-2.2.11-fix-router-path.patch
Patch5:			%{pkgname}-2.2.11-fix-module-filename.patch
Patch6:			%{pkgname}-2.2.16-link.patch
patch7:			jabberd-2.2.16.interpreter.patch
BuildRequires:		gc-devel
BuildRequires:		pq-devel
BuildRequires:		pkgconfig(openssl)
BuildRequires:		glibc-devel 
BuildRequires:          pkgconfig(zlib)
BuildRequires:		idn-devel
BuildRequires:		expat-devel
BuildRequires:          pkgconfig(libgsasl)
Buildrequires:		udns-devel
BuildRequires:		cppunit-devel
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
%patch6 -p0
%patch7 -p1 -b .interpreter

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
mv %{buildroot}%{_sysconfdir}/{*.xml,*.cfg,*.conf,*.dist,templates} %{buildroot}%{_sysconfdir}/%{pkgname}

# prepare to doc .dist files
mkdir examples
mv %{buildroot}%{_sysconfdir}/%{pkgname}/{*.dist,templates/*.dist} examples

# we have our own start script
rm -f %{buildroot}%{_bindir}/%{pkgname}
rm -f %{buildroot}%{_sysconfdir}/%{pkgname}/%{pkgname}.cfg*
rm -f %{buildroot}%{_sysconfdir}/%{pkgname}/%{pkgname}-*.conf
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}/init

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
%config(noreplace) %{_sysconfdir}/%{pkgname}/templates
%{_mandir}/man8/*
%defattr (0644,jabberd,jabberd,755)
%{_var}/run/%{pkgname}
%{_var}/lib/%{pkgname}
%{_logdir}/%{pkgname}



%changelog
* Thu May 10 2012 Crispin Boylan <crisb@mandriva.org> 2.2.16-1
+ Revision: 798032
- Patch6: Fix link
- Update patches
- New release

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - build with db 5.1 (from fwang | 2011-04-12 11:10:18 +0200)

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.11-5
+ Revision: 645806
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.11-4mdv2011.0
+ Revision: 627252
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.11-3mdv2011.0
+ Revision: 626531
- rebuilt against mysql-5.5.8 libs

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 2.2.11-1mdv2011.0
+ Revision: 567844
- New version 2.2.11

* Wed Apr 28 2010 Funda Wang <fwang@mandriva.org> 2.2.9-4mdv2010.1
+ Revision: 539941
- use correct name for plugins

* Wed Dec 30 2009 Jérôme Brenier <incubusss@mandriva.org> 2.2.9-3mdv2010.1
+ Revision: 484068
- rebuild for db-4.8

* Sun Nov 08 2009 Jérôme Brenier <incubusss@mandriva.org> 2.2.9-2mdv2010.1
+ Revision: 463209
- fix sm log path

* Fri Nov 06 2009 Jérôme Brenier <incubusss@mandriva.org> 2.2.9-1mdv2010.1
+ Revision: 461726
- update to new version 2.2.9
- rediff P1

* Sat May 30 2009 Jérôme Brenier <incubusss@mandriva.org> 2.2.8-2mdv2010.0
+ Revision: 381269
- add a workaround for a memory leak and the associated BR

* Thu May 28 2009 Jérôme Brenier <incubusss@mandriva.org> 2.2.8-1mdv2010.0
+ Revision: 380642
- fix BR on sqlite3
- readd default runlevels (initscript)
- new version 2.2.8
- spec file reworked
- add 5 patches to fix paths in conf files
- add a sysconfig file
- add logrotate
- fix initscript
- add missings BR and remove duplicates
- use poll MIO backend
- use autoreconf

  + Luis Daniel Lucio Quiroz <dlucio@mandriva.org>
    - 2.2.7.1

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix no-buildroot-tag

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - New version 2.1.23
      Sync spec file with fedora

* Fri Sep 21 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.1.14-4mdv2008.0
+ Revision: 91998
- [BUGFIX] Add missing slash (Bug  #33855)

* Mon Aug 20 2007 Funda Wang <fwang@mandriva.org> 2.1.14-3mdv2008.0
+ Revision: 67319
- fix bug#32693

* Sat Aug 18 2007 Funda Wang <fwang@mandriva.org> 2.1.14-2mdv2008.0
+ Revision: 66424
- add ldconfig for lib package
- align startup script with jabber

* Sat Aug 18 2007 Funda Wang <fwang@mandriva.org> 2.1.14-1mdv2008.0
+ Revision: 66421
- BR expat
- fix pre script
- pinit friendly
- bunzip source1
- Fix building and file list
- use cyrus sasl implementation rather gsasl
- New versino 2.1.14

  + Thierry Vignaud <tv@mandriva.org>
    - fix man pages

