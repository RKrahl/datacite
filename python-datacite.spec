%global distname datacite

Name:		python3-%{distname}
Version:	$version
Release:	0
Url:		$url
Summary:	$description
License:	Internal-Use
Group:		Development/Libraries/Python
Source:		%{distname}-%{version}.tar.gz
BuildRequires:	python3-base >= 3.4
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
$long_description


%prep
%setup -q -n %{distname}-%{version}


%build
python3 setup.py build


%install
python3 setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}


%files
%defattr(-,root,root)
%doc README.rst
%{python3_sitelib}/*


%changelog
