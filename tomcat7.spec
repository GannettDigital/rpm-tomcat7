# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
#
# wget https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.spec -O ~/rpmbuild/SPECS/tomcat7.spec
# wget https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.init -O ~/rpmbuild/SOURCES/tomcat7.init
# wget https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.sysconfig -O ~/rpmbuild/SOURCES/tomcat7.sysconfig
# wget https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.logrotate -O ~/rpmbuild/SOURCES/tomcat7.logrotate
# wget http://www.motorlogy.com/apache/tomcat/tomcat-7/v7.0.55/bin/apache-tomcat-7.0.55.tar.gz -O ~/rpmbuild/SOURCES/apache-tomcat-7.0.55.tar.gz
# rpmbuild -bb ~/rpmbuild/SPECS/tomcat7.spec

%define __jar_repack %{nil}
%define tomcat_home /usr/share/tomcat7
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine, RI for Servlet 2.4/JSP 2.0 API
Name:       tomcat7
Version:    7.0.55
BuildArch:  noarch
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Source1:    %{name}.init2
Source2:    %{name}.sysconfig
Source3:    %{name}.logrotate
Requires:   jdk
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on Sun's JDK and not
on JPP packages.

%package manager
Summary: The management web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description manager
The management web application of Apache Tomcat.

%package docs
Summary: The docs web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description docs
The docs web application of Apache Tomcat.

%package examples
Summary: The examples web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description examples
The examples web application of Apache Tomcat.

%package host-manager
Summary: The host-manager web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description host-manager
The host-manager web application of Apache Tomcat.


%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/%{name}/
cd %{buildroot}/%{tomcat_home}/
ln -s /var/log/%{name}/ logs
cd -

# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{tomcat_home}/conf %{buildroot}/%{_sysconfdir}/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s %{_sysconfdir}/%{name} conf
cd -

# Drop init script
install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{name}.init2 %{buildroot}/%{_initrddir}/%{name}

# Drop sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_home}
%{tomcat_home}/bin
%{tomcat_home}/conf
%{tomcat_home}/lib
%{tomcat_home}/logs
%{tomcat_home}/temp
%{tomcat_home}/LICENSE
%{tomcat_home}/NOTICE
%{tomcat_home}/RELEASE-NOTES
%{tomcat_home}/RUNNING.txt
%dir %{tomcat_home}/webapps
%{tomcat_home}/webapps/ROOT
/var/log/%{name}/
%defattr(-,root,root)
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*

%files manager
%{tomcat_home}/webapps/manager

%files docs
%{tomcat_home}/webapps/docs

%files examples
%{tomcat_home}/webapps/examples

%files host-manager
%{tomcat_home}/webapps/host-manager

%post
chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  service %{name} condrestart >/dev/null 2>&1
fi

%changelog
* Thu Sep 4 2014 Edward Bartholomew <edward@bartholomew>
- 7.0.55
* Mon Jul 1 2013 Nathan Milford <nathan@milford.io>
- 7.0.41
