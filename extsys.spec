%define name extsys
%define version 0.2
%define release %mkrel 1

%define extsysdir %{_var}/lib/extsys
%define mdvversion 2010.0

Summary: External Mandriva build system
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://git.fensystems.co.uk/release/%{name}/%{name}-%{version}.tar.bz2
License: GPL
Group: Development/Other
BuildArchitectures: noarch
Requires: subversion-tools subversion-server bm mdvsys mdv-youri-submit
Requires: genhdlist2
Requires: mandriva-release-common = %{mdvversion}

%description
extsys provides a mechanism for maintaining a Mandriva external
package repository using the mdvsys family of tools.

%prep
%setup

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -m 0755 extsys %{buildroot}%{_bindir}/
install -m 0755 mkextrepo %{buildroot}%{_bindir}/
install -m 0755 ext-create-srpm %{buildroot}%{_bindir}/
install -m 0755 ext-upload-srpm %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 extsys.conf %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}%{_sysconfdir}/youri
install -m 0644 extsubmit.conf %{buildroot}%{_sysconfdir}/youri/
mkdir -p %{buildroot}%{extsysdir}/{svn,dist,tmp}

%clean
rm -rf %{buildroot}

%pre
%_pre_groupadd extsys

%post
umask 002
if [ ! -f %{extsysdir}/svn/format ]; then
   # Create empty subversion repository
   svnadmin create %{extsysdir}/svn
   find /var/lib/extsys/svn -type f -and -perm -u+w -exec chmod g+w \{\} \;
   # Populate subversion repository with minimal directory structure
   rm -rf %{extsysdir}/tmp/svn
   cd %{extsysdir}/tmp
   svn co -q file://%{extsysdir}/svn
   cd %{extsysdir}/tmp/svn
   mkdir cooker misc updates
   svn add -q cooker misc updates
   svn ci -q -m "Creating empty directory structure"
   cd %{extsysdir}
   rm -rf %{extsysdir}/tmp/svn
fi
if [ ! -d %{extsysdir}/dist/%{mdvversion} ]; then
   # Create empty distribution tree
   mkextrepo -q %{mdvversion}
fi

%files
%defattr(-,root,root)
%{_bindir}/extsys
%{_bindir}/mkextrepo
%{_bindir}/ext-create-srpm
%{_bindir}/ext-upload-srpm
%config(noreplace) %{_sysconfdir}/extsys.conf
%config(noreplace) %{_sysconfdir}/youri/extsubmit.conf
%dir %{extsysdir}
%attr (02775,root,extsys) %dir %{extsysdir}/svn
%attr (02775,root,extsys) %dir %{extsysdir}/dist
%attr (02775,root,extsys) %dir %{extsysdir}/tmp
%doc README

%changelog
* Sun May  9 2010 Michael Brown <mbrown@fensystems.co.uk> 0.2-1fs
- Generate empty hdlist files on repository initialisation

* Sun May  9 2010 Michael Brown <mbrown@fensystems.co.uk> 0.1-1fs
- First packaged version
