%if 0%{?sle_version} >= 150500
%global pythons python3 python311
%else
%{?!python_module:%define python_module() python3-%{**}}
%define skip_python2 1
%endif

%global distname datacite

Name:		python-hzb-%{distname}
Version:	$version
Release:	0
Summary:	$description
License:	Apache-2.0
URL:		$url
Group:		Development/Libraries/Python
Source:		%{distname}-%{version}.tar.gz
BuildRequires:	%{python_module base >= 3.4}
BuildRequires:	%{python_module setuptools}
BuildRequires:	fdupes
BuildRequires:	python-rpm-macros
Requires:	python-PyYAML
Requires:	python-lxml
Requires:	python-requests
Requires:	python-keyring
BuildArch:	noarch
%python_subpackages

%description
$long_description


%prep
%setup -q -n %{distname}-%{version}


%build
%python_build


%install
%python_install
%fdupes %{buildroot}%{python_sitelib}
for f in `ls %{buildroot}%{_bindir}`
do
    mv %{buildroot}%{_bindir}/$$f %{buildroot}%{_bindir}/$${f%%.py}
done


%files %{python_files}
%license LICENSE
%doc README.rst CHANGES.rst
%{python_sitelib}/*
%{_bindir}/*


%changelog
