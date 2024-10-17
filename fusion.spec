
%define name	fusion
%define version	8.1.1
%define rel	1

%define tarball	linux-fusion-%version

Summary:	Fusion kernel module
Name:		%name
Version:	%version
Release:	%mkrel %rel
License:	GPL
Group:		System/Kernel and hardware
Source0:	http://www.directfb.org/downloads/Core/%tarball.tar.gz
URL:		https://www.directfb.org/
BuildArch:	noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root/

%description
Source package to build Fusion kernel module for DKMS and
Fusion development headers.

Fusion is a high level IPC API providing mechanisms for master/slave
environments.

%package -n dkms-%name
Summary:	Fusion kernel module
Group:		System/Kernel and hardware
Requires:	dkms
Requires(post):	dkms
Requires(preun):	dkms

%description -n dkms-%name
Fusion is a high level IPC API providing mechanisms for master/slave
environments.

%package devel
Summary:	Headers for developing programs that will use Fusion
Group:		Development/Kernel

%description devel
Fusion is a high level IPC API providing mechanisms for master/slave
environments.

This package contains the headers that programmers will need to develop
applications which will use Fusion.

%prep
%setup -q -n %tarball

%build

%install
rm -rf %{buildroot}

install -m 755 -d %{buildroot}/usr/src/%{name}-%{version}-%{release}
cp -r Makefile linux %{buildroot}/usr/src/%{name}-%{version}-%{release}

install -m 755 -d %{buildroot}%{_includedir}/linux
install -m 644 linux/include/linux/*.h %{buildroot}%{_includedir}/linux

cat > %{buildroot}/usr/src/%{name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%{name}"
PACKAGE_VERSION="%{version}-%{release}"

MAKE[0]="make KERNEL_VERSION=\$kernelver KERNEL_SOURCE=\$kernel_source_dir KERNEL_BUILD=\$kernel_source_dir"
BUILT_MODULE_LOCATION[0]="linux/drivers/char/fusion"
BUILT_MODULE_NAME[0]="fusion"
DEST_MODULE_LOCATION[0]="/kernel/drivers/char/fusion"

AUTOINSTALL=yes
EOF

%clean
rm -rf %{buildroot}

%post -n dkms-%name
dkms add     -m %{name} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms build   -m %{name} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms install -m %{name} -v %{version}-%{release} --rpm_safe_upgrade --force
true

%preun -n dkms-%name
dkms remove  -m %{name} -v %{version}-%{release} --rpm_safe_upgrade --all
true

%files -n dkms-%name
%defattr(-,root,root,-)
/usr/src/%{name}-%{version}-%{release}

%files devel
%defattr(-,root,root,-)
%doc ChangeLog README TODO doc/fusion.pdf
%{_includedir}/linux/fusion.h


%changelog
* Thu Jul 09 2009 Anssi Hannula <anssi@mandriva.org> 8.1.1-1mdv2010.0
+ Revision: 393968
- new version

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 7.0.1-1mdv2008.1
+ Revision: 140731
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 05 2007 Anssi Hannula <anssi@mandriva.org> 7.0.1-1mdv2008.0
+ Revision: 80155
- 7.0.1
- do not run next dkms step in %%post if one fails

* Sat May 19 2007 Anssi Hannula <anssi@mandriva.org> 3.2.3-1mdv2008.0
+ Revision: 28380
- 3.2.3
- adjustments to dkms make command


* Sat Feb 03 2007 Anssi Hannula <anssi@mandriva.org> 3.2.1-1mdv2007.0
+ Revision: 116075
- 3.2.1
- add requires(post), requires(preun), disable aborts in post and preun

* Fri Nov 03 2006 Anssi Hannula <anssi@mandriva.org> 3.2-1mdv2007.1
+ Revision: 76320
- 3.2
- Import fusion

* Fri Aug 25 2006 Anssi Hannula <anssi@mandriva.org> 3.0-2mdv2007.0
- fix building dkms module for non-running kernels

* Sat May 06 2006 Anssi Hannula <anssi@mandriva.org> 3.0-1mdk
- 3.0

* Thu Dec 22 2005 Anssi Hannula <anssi@mandriva.org> 1.1-1mdk
- initial Mandriva package

