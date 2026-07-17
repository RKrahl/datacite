%if 0%{?sle_version} >= 150500
%global pythons python311
%else
%{?!python_module:%define python_module() python3-%{**}}
%define skip_python2 1
%endif

%global distname datacite

Name:		    python-hzb-%{distname}
Version:	    $version
Release:	    0
Summary:	    $description
License:	    Apache-2.0
URL:		    $url
Group:		    Development/Libraries/Python
Source:		    %{distname}-%{version}.tar.gz
BuildRequires:	    %{python_module base >= 3.11}
BuildRequires:	    %{python_module setuptools}
BuildRequires:	    fdupes
BuildRequires:	    python-rpm-macros
Requires:	    python-lxml
Requires:	    python-requests
Requires:	    python-keyring
BuildArch:	    noarch
%python_subpackages

%description
$long_description


%prep
%setup -q -n %{distname}-%{version}


%build
%python_build


%install
%python_install
for f in datacite-doi datacite-validate-xml
do
    mv %{buildroot}%{_bindir}/$$f.py %{buildroot}%{_bindir}/$$f
done
%fdupes %{buildroot}%{python_sitelib}


%files %{python_files}
%license LICENSE.txt
%doc README.rst CHANGES.rst
%{_bindir}/datacite-doi
%{_bindir}/datacite-validate-xml
%{python_sitelib}/*


%changelog
