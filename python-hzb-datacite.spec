%if 0%{?sle_version} >= 150500
%global pythons python3 python311
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
BuildRequires:	    %{python_module base >= 3.4}
BuildRequires:	    %{python_module setuptools}
BuildRequires:	    fdupes
BuildRequires:	    python-rpm-macros
BuildRequires:	    update-alternatives
Requires:	    python-PyYAML
Requires:	    python-lxml
Requires:	    python-requests
Requires:	    python-keyring
Requires(post):	    update-alternatives
Requires(postun):   update-alternatives
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
    %python_clone -a %{buildroot}%{_bindir}/$$f
done
%fdupes %{buildroot}%{python_sitelib}


%post
%python_install_alternative datacite-doi datacite-validate-xml

%postun
%python_uninstall_alternative datacite-doi datacite-validate-xml


%files %{python_files}
%license LICENSE
%doc README.rst CHANGES.rst
%python_alternative %{_bindir}/datacite-doi
%python_alternative %{_bindir}/datacite-validate-xml
%{python_sitelib}/*


%changelog
