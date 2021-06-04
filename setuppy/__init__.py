#!/usr/bin/env python
import os
import setuptools

"""
https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
"""

METADATA_TYPES = dict(
    name=str,
    version=str,
    url=str,
    download_url=str,
    project_urls=dict,
    author=str,
    author_email=str,
    maintainer=str,
    maintainer_email=str,
    classifiers=list,
    license=str,
    description=str,
    long_description=str,
    long_description_content_type=str,
    keywords=list,
    platforms=list,
    provides=list,
    requires=list,
    obsoletes=list
)
OPTIONS_TYPES = dict(
    zip_safe=bool,
    setup_requires=list,
    install_requires=list,
    # extras_require=section,
    python_requires=list,
    # entry_points=section,
    use_2to3=bool,
    use_2to3_fixers=list,
    use_2to3_exclude_fixers=list,
    convert_2to3_doctests=list,
    scripts=list,
    eager_resources=list,
    dependency_links=list,
    tests_require=list,
    include_package_data=bool,
    packages=list,
    package_dir=dict,
    # package_data=section,
    # exclude_package_data=section,
    namespace_packages=list,
    py_modules=list,
)
TYPES = dict(list(METADATA_TYPES.items()) + list(OPTIONS_TYPES.items()))
KEYS = list(TYPES.keys())

def getenv(key):
    arg_type = TYPES.get(key,str)
    value = os.getenv(key)
    if isinstance(arg_type,bool):
        return value.lower() in ['1','true']
    if isinstance(arg_type,list):
        return value.splitlines()
    return value

class SetupPy:
    keys = None
    kwargs = None

    def __init__(self,**kwargs):
        self.kwargs = kwargs or self.kwargs

    def get_keys(self):
        return self.keys if self.keys else KEYS

    def get_kwargs(self):
        kwargs = {}
        for key in self.get_keys():
            value = self.get_value(key)
            if value:
                kwargs[key] = value
        return kwargs

    def format_kwargs(self,**kwargs):
        args = []
        keys = ['name','version']+list(sorted(set(kwargs.keys())-set(['name','version'])))
        for k in keys:
            v = kwargs[k]
            if v not in [None,'',[]]:
                s = "'%s'" % v if isinstance(v,str) else str(v)
                if isinstance(v,list):
                    s = "[\n"+",\n".join(map(lambda l: ' '*4+"'%s'" % l, sorted(filter(None,v))))+"\n]"
                args.append('%s=%s' % (k,s))
        return ",\n".join(map(lambda a:"\n".join(map(lambda l:' '*4 + l,a.splitlines())),args))

    def format_dict(self, value):
        lines = []
        for k, v in value.items():
            s = str(v) if isinstance(v, list) else "'%s'" % v
            lines.append("'%s': %s" % (k, s))
        return """{
%s
}""" % "\n".join(map(lambda l: "    %s," % l, lines))

    def get_value(self,key):
        env_key = 'SETUPPY_%s' % key.upper()
        if env_key in os.environ:
            return getenv(env_key)
        if self.kwargs and key in self.kwargs:
            return self.kwargs[key]
        if hasattr(self,key):
            return getattr(self,key)
        func_name = 'get_%s' % key
        if hasattr(self,func_name):
            return getattr(self,func_name)()

    def get_install_requires(self):
        if os.path.exists('requirements.txt'):
            return list(sorted(filter(None,
                map(lambda l:l.split('#')[0],open('requirements.txt').read().splitlines())
            )))

    def get_name(self):
        return os.path.basename(os.getcwd()).split('.')[0]

    def get_packages(self):
        return setuptools.find_packages()

    def get_scripts(self):
        for path in ['bin','scripts']:
            if os.path.exists(path) and os.path.isdir(path):
                return list(map(lambda l:os.path.join(path,l),os.listdir(path)))

    def __str__(self):
        return """from setuptools import setup

setup(
%s
)""" % self.format_kwargs(**self.get_kwargs())


