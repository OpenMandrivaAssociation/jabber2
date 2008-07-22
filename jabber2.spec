%define pkgname         jabberd
%define name		jabber2
%define version		2.1.23
%define release		%mkrel 6
%define __libtoolize    /bin/true

%{!?_without_pam:BuildRequires: pam-devel}
%{!?_without_sqlite:BuildRequires: sqlite-devel}
%{!?_without_db4:BuildRequires: db4-devel}
%{!?_without_ldap:BuildRequires: openldap-devel}
%{!?_without_mysql:BuildRequires: mysql-devel}
%{!?_without_postgresql:BuildRequires: postgresql-devel}

%define Summary		Jabber is an instant messaging System

Summary:		%Summary
Name:			%name
Version:		%version
Release:		%release
License:		GPL
Group:			System/Servers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
BuildRequires:		expat-devel
BuildRequires:          libgsasl-devel
Conflicts:		jabber
Requires(post,preun):	rpm-helper
Requires(pre,postun):	rpm-helper

%description
Jabber is an instant messaging System, similar to ICQ or AIM, yet far
different.
It is open source, absolutely free, simple, fast, extensible, modularized,
cross platform, and created with the future in mind. Jabber has been
designed from the ground up to serve the needs of the end user, satisfy
business demands, and maintain compatibility with other messaging systems.

%pre
%_pre_useradd %{pkgname} /var/run/%{pkgname} /bin/sh

%preun
%_preun_service %{pkgname}

%post
%_post_service %{pkgname}

%postun
%_postun_userdel %{pkgname}

%files
%defattr (0755,root,root,0755)
%_bindir/c2s
%_bindir/jabberd
%_bindir/resolver
%_bindir/router
%_bindir/s2s
%_bindir/sm
%_initrddir/%{pkgname}
%_libdir/%{pkgname}
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

#--------------------------------------------------------------------

%prep
%setup -q -n %{pkgname}-%{version}

%build
%serverbuild

export LIBS='-lgc'

%configure \
	%{!?_without_pam:--enable-pam} \
	%{?_without_pam:--disable-pam} \
	%{!?_without_db4:--enable-db} \
	%{?_without_db4:--disable-db} \
	%{!?_without_mysql:--enable-mysql} \
	%{!?_without_mysql:--with-extra-library-path=%{_libdir}/mysql} \
	%{?_without_mysql:--disable-mysql} \
	%{!?_without_ldap:--enable-ldap} \
	%{?_without_ldap:--disable-ldap} \
	%{!?_without_postgresql:--enable-pgsql} \
	%{?_without_postgresql:--disable-pgsql} \
	%{!?_without_sqlite:--enable-sqlite} \
	%{?_without_sqlite:--disable-sqlite} \
	--localstatedir=%{_var}/lib \
	--enable-fs --enable-anon --enable-pipe --enable-ssl \
	--enable-debug
%make

%install
rm -rf %buildroot
%makeinstall_std

mkdir -p %buildroot%{_sysconfdir}/jabberd
mv %buildroot%{_sysconfdir}/{*.xml,*.cfg,*.dist,templates} %buildroot%{_sysconfdir}/jabberd

install -D %{SOURCE1} ${RPM_BUILD_ROOT}%_initrddir/%{pkgname}

mkdir -p ${RPM_BUILD_ROOT}%{_var}/run/%{pkgname}

%{__mkdir_p} $RPM_BUILD_ROOT/%{_var}/lib/jabberd/{log,pid,db}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_initrddir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -p -m 644 tools/db-setup.mysql $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__install} -p -m 644 tools/db-setup.pgsql $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__install} -p -m 644 tools/migrate.pl $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__install} -p -m 644 tools/pipe-auth.pl $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__install} -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}
%{__install} -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}


%{__sed} -i -e "s,__BINDIR__,%{_bindir},g" \
            -e "s,__ETCDIR__,%{sysconfdir},g" \
            -e "s,__PIDDIR__,%{_var}/lib/jabberd/pid,g" \
            -e "s,__SYSCONF__,%{_sysconfdir}/sysconfig,g" \
		$RPM_BUILD_ROOT%{_initrddir}/%{name} \
		$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%{__cat} >> $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/jabberd << END
#%PAM-1.0
auth       required     pam_nologin.so
auth       include      system-auth
account    include      system-auth
session    include      system-auth
END

#default driver for storage
#the default pam backend needs auto creation of accounts
%{__sed} -i -e ':a;N;$!ba' \
            -e 's,<driver>mysql</driver>,<driver>db</driver>,g' \
            -e 's,<!--\n    <auto-create/>\n    -->,<auto-create/>,g' \
		$RPM_BUILD_ROOT%{sysconfdir}/sm.xml

#default authentication backend
#enable SSL certificate
#clients must do STARTTLS
#disable account registrations by default, because the default installation uses PAM
#set the realm to '' for a working authentication against PAM
%{__sed} -i -e ':a;N;$!ba' \
            -e 's,<module>mysql</module>,<module>pam</module>,g' \
            -e "s,register-enable='true'>,realm='' require-starttls='true' pemfile='/etc/jabberd/server.pem'>,g" \
		$RPM_BUILD_ROOT%{sysconfdir}/c2s.xml

#ghost file
touch $RPM_BUILD_ROOT%{sysconfdir}/server.pem

# we have our own start script
%{__rm} $RPM_BUILD_ROOT%{_bindir}/jabberd

# we have our own start script
%{__rm} $RPM_BUILD_ROOT%{sysconfdir}/jabberd.cfg*

# remove unused devel files
rm -f %buildroot%_libdir/%{pkgname}/{*.la,mod_*.so}

%clean
rm -rf %buildroot
