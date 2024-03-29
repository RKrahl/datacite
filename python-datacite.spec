%global distname datacite

Name:		python3-%{distname}
Version:	$version
Release:	0
Url:		$url
Summary:	$description
License:	Apache-2.0
Group:		Development/Libraries/Python
Source:		%{distname}-%{version}.tar.gz
BuildRequires:	python3-base >= 3.4
BuildRequires:	python3-setuptools
Requires:	python3-PyYAML
Requires:	python3-lxml
Requires:	python3-requests
Requires:	python3-keyring
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
for f in `ls %{buildroot}%{_bindir}`
do
    mv %{buildroot}%{_bindir}/$$f %{buildroot}%{_bindir}/$${f%%.py}
done


%files
%defattr(-,root,root)
%doc README.rst CHANGES.rst
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/*


%changelog
