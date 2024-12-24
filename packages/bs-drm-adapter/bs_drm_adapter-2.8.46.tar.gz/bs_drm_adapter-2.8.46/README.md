# Beenius DRM adapter POC
## About application
Beenius DRM adapter is a service that provides DRM entitlement information to requesting DRM systems.

Supported DRM systems are:
* Castlabs

See Configuration and Using the application sections of this document for details on application usage.

## Installation
Currently only semi manual installation is supported. Python 3.6 is required to run the service.

### Centos 7 - Python 3 setup
Install EPEL repository, python36 and virtualenv packages
```bash
yum install -y epel-release
yum install -y python36 python36-virtualenv
```

### Centos 6 - Python 3 setup
Install required dependencies for compiling Python 3.6
```bash
yum install -y gcc zlib-devel openssl-devel
```

Download Python 3.6, compile it, create symbolic links (example for Python 3.6.8)
```bash
# Download and unpack
cd /tmp
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
tar -zxvf Python-3.6.8.tgz

# Configure and compile
cd Python-3.6.8
./configure --prefix=/usr/local/
make && make altinstall

# Create symbolic links
sudo ln -s /usr/local/bin/python3.6 /usr/local/bin/python3
sudo ln -s /usr/local/bin/pip3.6 /usr/local/bin/pip3
```

Update pip and install virtualenv module (as root)
```bash
pip3 install --upgrade pip
pip3 install virtualenv
```

### Application installation
Copy source code directory to target machine. This guide assumes `/tmp/bs-drm-adapter`

#### CentOS 7
Install systemd service file
```bash
cd /tmp/bs-drm-adapter
cp os/bs-drm-adapter.service /etc/systemd/system
systemctl daemon-reload
```

Prepare virtual environment
```bash
# Create virtual environment, this will also provide pip package manager
virtualenv-3 -p python3 /opt/bs-drm-adapter
```

#### CentOS 6
Install sysv init script file, logrotate file, register service, prepare pid file directory
```bash
cd /tmp/bs-drm-adapter
install -m 0755 os/bs-drm-adapter.init /etc/init.d/bs-drm-adapter
chkconfig --add bs-drm-adapter
install -o beenius -g beenius -d /var/run/bs-drm-adapter
```

Prepare virtual environment
```bash
# Create virtual environment, this will also provide pip package manager
virtualenv -p python3 /opt/bs-drm-adapter
```

#### CentOS 7 and CentOS 6
Prepare directory paths, copy configuration file, systemd unit file and create a virtual environment. This assumes
beenius user exists on the system. If it doesn't create it first.
```bash
# Create directory paths
cd /tmp/bs-drm-adapter
install -o beenius -g beenius -d /var/log/bs-drm-adapter

# Install UWSGI server configuration file
cp os/bs-drm-adapter-uwsgi.yml /etc/sysconfig/

# Copy bs-drm-adapter service configuration file
cp os/bs-drm-adapter.yml /etc/sysconfig/
```

Activate virtual environment and install the application
```bash
cd /tmp/bs-drm-adapter
. /opt/bs-drm-adapter/bin/activate
pip install .
deactivate
```

## Configuration
### UWSGI server
UWSGI server is configured in `/etc/sysconfig/bs-drm-adapter-uwsgi.yml` configuration file. If you plan to use Nginx's
`uwsgi_pass` directive to reverse proxy requests to the application make sure you comment out `socket` directive and
comment the `http` one.

### Application configuration
Application configuration file is `/etc/sysconfig/bs-drm-adapter.yml`. Application requires that `drm_adapter_mode` is
set to required adapter mode. Adapter specific options can be configured in `drm_adapter_options` dictionary.
`service_routing_host` has to be set to IPrAPI endpoint on Beenius server for integration with OB API.

Example configuration for Castlabs adapter
```yaml
service_routing_host: http://192.168.122.75:765
force_device_id_check
drm_adapter_mode: castlabs
drm_adapter_options:
  redirect_url: http://192.168.122.75:80/denied
  profile: purchase
```

Restart of application is required when configuration is changed. If running on multiple servers with reverse proxy make
sure that configuration files are in sync between them.

#### Configuration options

| Option                             | Mandatory| Default | Description                                                                      |
|------------------------------------|:--------:|:-------:|----------------------------------------------------------------------------------|
| log_level                          | yes      | /       | Service log level `[DEBUG, INFO, WARNING, ERROR, CRITICAL]`                      |
| service_routing_host               | yes      | /       | Beenius IPrAPI endpoint `scheme://host:port`                                     |
| drm_adapter_mode                   | yes      | /       | DRM adapter vendor mode                                                          |
| drm_adapter_options                | no       | none    | DRM adapter specific options                                                     |
| minimum_entitlement_validity       | no       | 0       | Minimum validity of entitlement in seconds `int`                                 |
| content_entitlement_check          | no       | true    | Send content_uid when performing entitlement check `[true/false]`                |
| force_device_id_check              | no       | true    | Force using provided device_id when performing entitlement check `[true/false]`  |
| map_profile_to_subscriber          | no       | false   | Enable mapping of profileUid to subscriberUid `[true/false]`                     |
| map_profile_fallback_to_subscriber | no       | false   | Fallback to subscriberUid if profileUid mapping fails `[true/false]`             |

Minimum validity of entitlements can be increased by setting `minimum_entitlement_validity` property. This can be used
to ensure entitlements are not re-requested in short period of time when initially obtained before end of existing
billing period (normally end of month). It will also affect content availability when it is explicitly purchased for
short duration though.

Adapter supports mapping of profileUid to subscriberUid by enabling `map_profile_to_subscriber`. This is useful in cases
when consumer applications are unaware of subscriberUid and are sending profileUid in entitlement requests to DRM
system. Additionally, fallback to subscriberUid can be enabled by `map_profile_fallback_to_subscriber`. This is useful
during transition periods when some consumer applications send subscriberUid and some profileUid.

#### Adapter modes
Supported adapter modes are:
* castlabs

#### Adapter specific options
##### castlabs

| Option | Description                                                                                                                               |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------|
| redirect_url  | A URL the user can be redirected to on error (if supported by player and DRM system).                                               |
| profile       | The profile describes how the content may be used. Supported are 'purchase', 'rental'. Refer to Castlabs documentation for details. |
| crt_response_properties | Custom properties for customer rights token. Must be properly formatted YAML which will be transalted to JSON and merged with default CRT parameters. |

Configuration `force_device_id_check` should be set to `false` when integrating with Castlabs.

###### Custom CRT properties
When specifying custom CRT properties using crt_response_properties configuration key make sure that it's value is a
properly formatted YAML. This YAML will then be translated to JSON and merged with CRT properties provided by the
CastlabsAdapter class. There is no schema validation for the properties configured so make sure they conform with
[Castlabs' CRT specification](https://fe.drmtoday.com/frontend/documentation/integration/customer_rights_token.html).

Following parameters MUST NOT be set in the *crt_response_properties* as they are already provided by CastlabsAdapter
class:
- accountingId
- assetId
- profile
- message

Example configuration:
```yaml
  crt_response_properties:
    storeLicense: true
    overrides:
      selectors:
        - selector-2
      crt:
        op:
          config:
            UHD:
              WidevineM:
                deny: true
            HD:
              WidevineM:
                require HDCP: HDCP_V1
                allowRevokedDevice: true
            SD:
              WidevineM:
                require HDCP: HDCP_NONE
                allowRevokedDevice: false
            AUDIO:
              WidevineM:
                require HDCP: HDCP_NONE
                allowRevokedDevice: false
```

Resulting JSON response:
```json
{
    "accountingId": "cl_channel1-125c4d72-5d0f-4e22-8032-9f3ee34bfd51",
    "assetId": "cl_channel1",
    "profile": {
        "rental": {
            "absoluteExpiration": "2021-07-01T00:00:00+00:00",
            "playDuration": 86400000
        }
    },
    "message": "granted",
    "storeLicense": true,
    "overrides": {
        "selectors": [
            "selector-2"
        ],
        "crt": {
            "op": {
                "config": {
                    "UHD": {
                        "WidevineM": {
                            "deny": true
                        }
                    },
                    "HD": {
                        "WidevineM": {
                            "require HDCP": "HDCP_V1",
                            "allowRevokedDevice": true
                        }
                    },
                    "SD": {
                        "WidevineM": {
                            "require HDCP": "HDCP_NONE",
                            "allowRevokedDevice": false
                        }
                    },
                    "AUDIO": {
                        "WidevineM": {
                            "require HDCP": "HDCP_NONE",
                            "allowRevokedDevice": false
                        }
                    }
                }
            }
        }
    }
}
```

### Nginx as uwsgi reverse proxy
Example upstream location on Nginx. If using more than one upstream server define an upstream block instead of using
direct IP:port as upstream definition.
```
location /bs-drm-adapter {
    include uwsgi_params;
    uwsgi_pass 192.168.122.30:9010;
}
```

## Running the application
### Controlling application
#### Centos 7
Start application using `systemctl start bs-drm-adapter`

Stop application using `systemctl stop bs-drm-adapter`

Check status of application using `systemctl status bs-drm-adapter`

#### Centos 6
Start application using `service bs-drm-adapter start`

Stop application using `service bs-drm-adapter stop`

Check status of application using `service bs-drm-adapter status`

### Debugging runtime issues
#### Startup issues
For startup issues check system journal `journalctl -xe -f -u bs-drm-adapter`

#### Runtime issues
For runtime issues check application logs in `/var/log/bs-drm-adapter` directory.

### Deployment guidelines
In production environments it is recommended to deploy more than one instance of application behind Nginx reverse proxy
and distribute requests to it in round robin manner by properly configuring upstream servers block on Nginx.

See configuration section for proper configuration of UWSGI server and Nginx reverse proxy.

## Application in Docker container
### Building the container image
Building the image is as simple as running proper `docker build` command. It is possible to override adapter version at
build time using `DRM_ADAPTER_VERSION` build argument using `--build-arg` flag.

### Running application in container
Following application runtime parameters are available via environment variables:

| VARIABLE | DEFAULT VALUE   | DESCRIPTION |
|----------|:---------------:|-------------|
| UWSGI_SOCKET_TYPE | http | Type of socket to use. Valid options are ['http', 'uwsgi'] |
| UWSGI_PORT | 8080 | Port to bind application to |
| UWSGI_PROCESSES | 2 | Number of worker processes to spawn |
| UWSGI_THREADS | 2 | Number of threads available to worker |
| BS_DRM_ADAPTER_CONFIGURATION | /opt/bs-drm-adapter.yml | Location of application configuration file |

Default configuration file included in the image only contains test parameters and should not be used for anything but
development testing. Mount an external configuration file into container or otherwise present it to container (sidecar,
configMap...). Refer to the application configuration section for details on how to configure the app.

Example of running the application in Docker with default parameters
```bash
docker run \
    -ti \
    --name bs-drm-adapter \
    -v /home/user/bs-drm-adapter.yml:/opt/bs-drm-adapter.yml \
    -p8080:8080 \
    nexus-docker.lab.beenius.tv/bs-drm-adapter:2.0-1
```

## Extending and contributing to the project
### Development requirements
Any development on the project should be done with running using Python 3.6 in mind. Do not use features from higher
Python versions.

### Environment setup
Clone the project from [gitlab repository](https://git.beenius.tv/devops/tools/bs-drm-adapter).
```.bash
git clone git@git.beenius.tv:devops/tools/bs-drm-adapter.git
```

Set up virtual environment for development using `pipenv`. This requires Python 3.6 to be available on development
system. Running following commands a virtual environment with all dependencies including development ones will be set
up. It will also install git pre-commit hooks.
```.bash
pipenv install --dev
pipenv run pre-commit install
```

### Building and publishing to Beenius PyPi
`Dockerfile.beepypi` is included and can be used to build/publish packages to Beenius' hosted PyPi repository. Please
use for publishing tags only! You may want to clean up after building.
```.bash
# Build
docker build . -f Dockerfile.beepypi

# Cleanup - remove danging image that remains after building
docker image prune
```
