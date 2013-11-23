# Copyright (c) 2013 Paul Richards <paul@minimoo.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

%define revision 1

%define nsca_user nsca
%define nsca_group nsca

Summary: NSCA-ng
Name: nsca-ng
Version: 1.2
Release: %{revision}%{?dist}
License: BSD
Group: Applications/System
Source: %{name}-%{version}.tar.gz
URL: https://www.nsca-ng.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libconfuse-devel
BuildRequires: openssl-devel

Requires: %{name}-client
Requires: %{name}-server

%description
NSCA-ng provides a client-server pair that makes the Nagios command file accessible to remote systems.

%package common
Summary:      NSCA-ng common files
Group:        Applications/System

%description common
NSCA-ng provides a client-server pair that makes the Nagios command file accessible to remote systems.

This package creates the nsca user and group.

%package server
Summary:      NSCA-ng server
Group:        Applications/System
Requires:     %{name}-common
Requires:     libconfuse
Requires:     openssl

%description server
NSCA-ng provides a client-server pair that makes the Nagios command file accessible to remote systems.

This is the server component of NSCA-ng.

%package client
Summary:      NSCA-ng client
Group:        Applications/System
Requires:     %{name}-common
Requires:     libconfuse
Requires:     openssl

%description client
NSCA-ng provides a client-server pair that makes the Nagios command file accessible to remote systems.

This is the client component of NSCA-ng.


%prep
%setup -q -n %{name}-%{version}

%build
./autogen.sh
%configure --enable-server

make %{?_smp_mflags}

%install
[ "%{buildroot}" != "/" ] && [ -d "%{buildroot}" ] && rm -rf %{buildroot}
make install \
	DESTDIR="%{buildroot}"

mkdir %{buildroot}/etc/init.d
install contrib/nsca-ng.init %{buildroot}/etc/init.d/%{name}

%clean
[ "%{buildroot}" != "/" ] && [ -d "%{buildroot}" ] && rm -rf %{buildroot}

%pre common
getent group %{nsca_group} >/dev/null || %{_sbindir}/groupadd -r %{nsca_group}
getent passwd %{nsca_user} >/dev/null || %{_sbindir}/useradd -c "nsca" -s /sbin/nologin -r -d %{_localstatedir}/spool/%{nsca_user} -g %{nsca_group} %{nsca_user}
exit 0

%files common
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS

%files server
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS
%attr(755,-,-) %{_sysconfdir}/init.d/%{name}
%config(noreplace) %attr(0640,%{nsca_user},%{nsca_group}) %dir %{_sysconfdir}/nsca-ng.cfg
%{_sbindir}/nsca-ng
%{_mandir}/man5/nsca-ng.cfg.5.gz
%{_mandir}/man8/nsca-ng.8.gz

%files client
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS
%config(noreplace) %attr(0640,%{nsca_user},%{nsca_group}) %dir %{_sysconfdir}/send_nsca.cfg
%{_sbindir}/send_nsca
%{_mandir}/man5/send_nsca.cfg.5.gz
%{_mandir}/man8/send_nsca.8.gz

%changelog
