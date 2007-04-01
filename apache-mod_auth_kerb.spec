#
# Conditional build:
%bcond_with	krb4		# build with Kerberos V4 support
#
%define		mod_name	auth_kerb
%define 	apxs	/usr/sbin/apxs
Summary:	This is the Kerberos authentication module for Apache
Summary(pl.UTF-8):	Moduł uwierzytelnienia Kerberos dla Apache
Name:		apache-mod_%{mod_name}
Version:	5.3
Release:	1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modauthkerb/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	a363588578050b3d320a2ceccf3ed666
Source1:	%{name}.conf
URL:		http://modauthkerb.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	gdbm-devel
BuildRequires:	krb5-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an Kerberos directory.

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP z użyciem wpisów w katalogu Kerberosa.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%configure \
	%{?with_krb4:--with-krb4} \
	%{!?with_krb4:--without-krb4} \
	--with-apache=%{_prefix}

%{__sed} -i -e 's/-pthread/-lpthread/' Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/20_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
