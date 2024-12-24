# NetBox SVM

<p align="center"><i>Netbox Plugin software version manager of software components, including versions and installations.</i></p>

<div align="center">
<a href="https://pypi.org/project/netbox-svm/"><img src="https://img.shields.io/pypi/v/netbox-svm" alt="PyPi"/></a>
<a href="https://github.com/hocchudong/netbox-software-version-manager/stargazers"><img src="https://img.shields.io/github/stars/hocchudong/netbox-software-version-manager" alt="Stars Badge"/></a>
<a href="https://github.com/hocchudong/netbox-software-version-manager/network/members"><img src="https://img.shields.io/github/forks/hocchudong/netbox-software-version-manager" alt="Forks Badge"/></a>
<a href="https://github.com/hocchudong/netbox-software-version-manager/pulls"><img src="https://img.shields.io/github/issues-pr/hocchudong/netbox-software-version-manager" alt="Pull Requests Badge"/></a>
<a href="https://github.com/hocchudong/netbox-software-version-manager/issues"><img src="https://img.shields.io/github/issues/hocchudong/netbox-software-version-manager" alt="Issues Badge"/></a>
<a href="https://github.com/hocchudong/netbox-software-version-manager/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/hocchudong/netbox-software-version-manager?color=2b9348"></a>
<a href="https://github.com/hocchudong/netbox-software-version-manager/blob/master/LICENSE"><img src="https://img.shields.io/github/license/hocchudong/netbox-software-version-manager?color=2b9348" alt="License Badge"/></a>
</div>

## Install Require

netbox version >= 4.0

## Known Issues

- WARNING: This plugin is only tested with a single NetBox version at this time.
- CSV/Bulk imports for SoftwareProduct, Version and Installation are currently broken (WIP)

## Installation Guide

### In mono service:

To install the plugin, first using pip and install netbox-svm:

   ```
   cd /opt/netbox
   source venv/bin/activate
   pip install netbox-svm
   ```

Next, enable the plugin in /opt/netbox/netbox/netbox/configuration.py, or if you have a /configuration/plugins.py file, the plugins.py file will take precedence.

   ```
   PLUGINS = [
      'netbox_svm'
   ]
   ```
Then you may need to perform the final step of restarting the service to ensure that the changes take effect correctly:

   ```
   python netbox/manage.py migrate netbox_svm
   sudo systemctl restart netbox
   ```

### In docker env

When using the Docker version of NetBox, first follow the netbox-docker [quickstart](https://github.com/netbox-community/netbox-docker#quickstart) instructions to clone the netbox-docker repo and set up the ``docker-compose.override.yml``.

Next, follow these instructions (based on the NetBox docker variant
[instructions](https://github.com/netbox-community/netbox-docker/wiki/Configuration#custom-configuration-files))
to install the NetBox SVM plugin:

1. Add ``netbox_svm`` to the ``PLUGINS`` list in
   ``configuration/plugins.py``.
2. Create a ``plugin_requirements.txt`` with ``netbox-svm`` as
   contents.
3. Create a ``Dockerfile-SVM`` with contents:

   ```
   FROM netboxcommunity/netbox:v4.0

   COPY ./plugin_requirements.txt /
   RUN /opt/netbox/venv/bin/pip install --no-warn-script-location -r /plugin_requirements.txt
   ```

4. Create a ``docker-compose.override.yml`` with contents:

   ```
   version: '3.7'
   services:
     netbox:
       ports:
         - 8000:8080
       build:
         context: .
         dockerfile: Dockerfile-SVM
       image: netbox:svm
     netbox-worker:
       image: netbox:svm
     netbox-housekeeping:
       image: netbox:svm
   ```

Now, build the image: ``docker compose build --no-cache``

And finally, run NetBox with the SVM plugin: ``docker compose up -d``

## Releasing Guide

To draft a release;

update the `netbox_svm/__init__.py` file to reflect the new version, then from the *src*
directory run

   ```
   $ python -m build
   $ twine upload dist/*
   ```

On Github.com create a similar tag and version. These steps could be
automated with a github workflow.