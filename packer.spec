# TODO
# - solve hacks better:
#   - hack1: git rev-parse expects .git repo and aborts
#   - hack2: go get ./... spews errors about "no install location for directory ... outside GOPATH" and aborts
#   - hack3: scripts/build.sh does kill 0, which kills jobs and makes it abort with error, ignore errors
#   - hack4: the same kill 0 kills make as well, use setsid to "fix"
# - building downloads go packages - not suitable for builders
#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Tool for creating identical machine images for multiple platforms from a single source configuration
Name:		packer
Version:	0.3.8
Release:	0.1
License:	MPL 2.0
Group:		Applications/Emulators
Source0:	https://github.com/mitchellh/packer/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2e8fbcf12e4cd9416b7c1c2ea1d97c3a
Patch0:		build.patch
URL:		http://www.packer.io/
BuildRequires:	golang >= 1.1
BuildRequires:	bash
BuildRequires:	mercurial
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Packer is lightweight, runs on every major operating system, and is
highly performant, creating machine images for multiple platforms in
parallel. Packer comes out of the box with support for creating AMIs
(EC2), VMware images, and VirtualBox images. Support for more
platforms can be added via plugins.

The images that Packer creates can easily be turned into Vagrant
boxes.

%prep
%setup -q
%patch0 -p1

%build
# avoid interfering with builder env
#unset GIT_WORK_TREE GIT_DIR

export GOPATH=$(pwd)/GOPATH
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOBIN
install -d $GOBIN

setsid %{__make} || :

%{?with_test:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md CONTRIBUTING.md LICENSE
%attr(755,root,root) %{_bindir}/packer
%attr(755,root,root) %{_bindir}/packer-builder-amazon-chroot
%attr(755,root,root) %{_bindir}/packer-builder-amazon-ebs
%attr(755,root,root) %{_bindir}/packer-builder-amazon-instance
%attr(755,root,root) %{_bindir}/packer-builder-digitalocean
%attr(755,root,root) %{_bindir}/packer-builder-openstack
%attr(755,root,root) %{_bindir}/packer-builder-virtualbox
%attr(755,root,root) %{_bindir}/packer-builder-vmware
%attr(755,root,root) %{_bindir}/packer-command-build
%attr(755,root,root) %{_bindir}/packer-command-fix
%attr(755,root,root) %{_bindir}/packer-command-inspect
%attr(755,root,root) %{_bindir}/packer-command-validate
%attr(755,root,root) %{_bindir}/packer-post-processor-vagrant
%attr(755,root,root) %{_bindir}/packer-provisioner-chef-solo
%attr(755,root,root) %{_bindir}/packer-provisioner-file
%attr(755,root,root) %{_bindir}/packer-provisioner-puppet-masterless
%attr(755,root,root) %{_bindir}/packer-provisioner-salt-masterless
%attr(755,root,root) %{_bindir}/packer-provisioner-shell
