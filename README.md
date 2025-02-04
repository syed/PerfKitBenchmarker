PerfKitBenchmarker
==================

PerfKit Benchmarker is an open effort to define a canonical set of benchmarks to measure and compare cloud
offerings.  It's designed to operate via vendor provided command line tools. The benchmarks are not
tuned (ie the defaults) because this is what most users will use.  This should help us drive to great defaults.
Only in the rare cause where there is a common practice like setting the buffer pool size of a database do we
change any settings.


KNOWN ISSUES
============


LICENSING
=========

PerfKitBenchmarker provides wrappers and workload definitions around popular benchmark tools. We made it very simple
to use and automate everything we can.  It instantiates VMs on the Cloud provider of your choice, automatically
installs benchmarks, and run the workloads without user interaction.

Due to the level of automation you will not see prompts for software installed as part of a benchmark run.
Therefore you must accept the license of each benchmarks individually, and take responsibility for using them
before you use the PerfKitBenchmarker.

In its current release these are the benchmarks that are executed:

  - `aerospike`: Apache V2 for the client and GNU AGPL v3.0 for the server (http://www.aerospike.com/products-services/)
  - `bonnie++`: GPL v2 (http://www.coker.com.au/bonnie++/readme.html)
  - `cassandra_ycsb`: Apache v2 (http://cassandra.apache.org/)
  - `cassandra_stress`: Apache v2 (http://cassandra.apache.org/)
  - `cluster_boot`: MIT License
  - `coremark`: EEMBC (https://www.eembc.org/)
  - `copy_throughput`: Apache v2.
  - `fio`: GPL v2 (https://github.com/axboe/fio/blob/master/COPYING)
  - `hadoop_terasort`: Apache v2 (http://hadoop.apache.org/)
  - `hpcc`: Original BSD license (http://icl.cs.utk.edu/hpcc/faq/#263)
  - `iperf`: BSD license(http://iperf.sourceforge.net/)
  - `memtier_benchmark`: GPL v2 (https://github.com/RedisLabs/memtier_benchmark)
  - `mesh_network`: HP license (http://www.calculate-linux.org/packages/licenses/netperf)
  - `mongodb`: **Deprecated**. GNU AGPL v3.0 (http://www.mongodb.org/about/licensing/)
  - `mongodb_ycsb`: GNU AGPL v3.0 (http://www.mongodb.org/about/licensing/)
  - `netperf`: HP license (http://www.calculate-linux.org/packages/licenses/netperf)
  - `oldisim`: Apache v2.
  - `object_storage_service`: Apache v2.
  - `ping`: No license needed.
  - `silo`: MIT License
  - `scimark2`: public domain (http://math.nist.gov/scimark2/credits.html)
  - `speccpu2006`: Spec CPU2006 (http://www.spec.org/cpu2006/)
  - `sysbench_oltp`: GPL v2 (https://github.com/akopytov/sysbench)
  - `unixbench`: GPL v2 (https://code.google.com/p/byte-unixbench/)
  - `ycsb` (used by `mongodb`, `hbase_ycsb`, and others): Apache V2 (https://github.com/brianfrankcooper/YCSB/blob/master/LICENSE.txt)

Some of the benchmarks invoked require Java. You must also agree with the following license:

  - openjdk-7-jre: GPL v2 with the Classpath Exception (http://openjdk.java.net/legal/gplv2+ce.html)

[CoreMark](http://www.eembc.org/coremark/) setup cannot be automated. EEMBC requires users to agree with their terms and conditions, and PerfKit
Benchmarker users must manually download the CoreMark tarball from their website and save it under the
`perfkitbenchmarker/data` folder (e.g. `~/PerfKitBenchmarker/perfkitbenchmarker/data/coremark_v1.0.tgz`)

[SpecCPU2006](https://www.spec.org/cpu2006/) benchmark setup cannot be automated. SPEC requires users to purchase a license and agree with their terms and conditions.
PerfKit Benchmarker users must manually download SpecCPU2006 tarball from their website and save it under
the `perfkitbenchmarker/data` folder (e.g. `~/PerfKitBenchmarker/perfkitbenchmarker/data/cpu2006v1.2.tgz`)

Installing Prerequisites
========================
Before you can run the PerfKit Benchmaker on Cloud providers you need accounts and access:

* Get a GCE account to run tests on GCE. Our site is https://cloud.google.com
* Get an AWS account to run tests on AWS. Their site is http://aws.amazon.com/
* Get an Azure account to run tests on Azure. Their site is http://azure.microsoft.com/
* Get a DigitalOcean account to run tests on DigitalOcean. Their site is https://www.digitalocean.com/
* Get a Rackspace Cloud account to run tests on Rackspace. Their site is https://www.rackspace.com/

You also need the software dependencies, which are mostly command line tools and credentials to access your
accounts without a password.  The following steps should help you get the CLI tool auth in place.

If you are running on Windows, you will need to install GitHub Windows
since it includes tools like `openssl` and an `ssh` client. Alternatively you can
install Cygwin since it should include the same tools.

## Install Python 2.7 and `pip`
If you are running on Windows, get the latest version of Python 2.7
[here](https://www.python.org/downloads/windows/). This should have pip bundled
with it. Make sure your `PATH` environment variable is set so that you can use
both `python` and `pip` on the command line (you can have the installer do it
for you if you select the correct option).

Most Linux distributions and recent Mac OS X version already have Python 2.7
installed.
If Python is not installed, you can likely install it using your distribution's package manager, or see the [Python Download page](https://www.python.org/downloads/).

If you need to install `pip`, see [these instructions](http://pip.readthedocs.org/en/stable/installing/).

## (*Windows Only*) Install GitHub Windows

Instructions: https://windows.github.com/

Make sure that `openssl`/`ssh`/`scp`/`ssh-keygen` are on your path (you will need to update the `PATH` environment variable).
The path to these commands should be

`C:\\Users\\\<user\>\\AppData\\Local\\GitHub\\PortableGit\_\<guid\>\\bin`

## Install `gcloud` and setup authentication
Instructions: https://developers.google.com/cloud/sdk/. If you're using OS X or Linux you can run the command below.

When prompted pick the local folder, then Python project, then the defaults for all the rest
```
$ curl https://sdk.cloud.google.com | bash
```
Restart your shell window (or logout/ssh again if running on a VM)

On Windows, visit the same page and follow the Windows installation instructions on the page.

Set your credentials up: https://developers.google.com/cloud/sdk/gcloud/#gcloud.auth. Run the command below.
It will print a web page URL. Navigate there, authorize the gcloud instance you just installed to use the services
it lists, copy the access token and give it to the shell prompt.
```
$ gcloud auth login
```

You will need a project ID before you can run. Please navigate to https://console.developers.google.com and
create one.


## Install OpenStack Nova client and setup authentication
Make sure you have installed pip (see the section above).

Install python-novaclient by following command:
```
sudo pip install python-novaclient
```

You must specify authentication information for test execution, including user
name (``--openstack_username` flag or `OS_USERNAME` environment variable), tenant name
(`--openstack_tenant` flag or `OS_TENANT_NAME` environment variable), and
authentication URL (`--openstack_auth_url` flag or `OS_AUTH_URL` environment
variable).

The password cannot be set through a flag. You can specify it through the
`OS_PASSWORD` environment variable, or alternatively you can save it in a file
and specify the file location with the `--openstack_password_file` flag or
`OPENSTACK_PASSWORD_FILE` environment variable.

Example using environment variables:

```bash
export OS_USERNAME=admin
export OS_TENANT=myproject
export OS_AUTH_URL=http://localhost:5000
export OS_PASSWORD=<password>
```

Example using a password file at the default file location:

```bash
echo topsecretpassword > ~/.config/openstack-password.txt
./pkb.py --cloud=OpenStack --benchmarks=ping
```

## Kubernetes configuration and credentials
Perfkit uses `kubectl` binary in order to communicate with Kubernetes cluster - you need to pass the path to `kubectl` binary using `--kubectl` flag. It's recommended to use version 1.0.1 (available to download here: https://storage.googleapis.com/kubernetes-release/release/v1.0.1/bin/linux/amd64/kubectl).
Authentication to Kubernetes cluster is done via `kubeconfig` file (https://github.com/kubernetes/kubernetes/blob/release-1.0/docs/user-guide/kubeconfig-file.md). Its path is passed using `--kubeconfig` flag.

**Image prerequisites**  
Docker instances by default don't allow to SSH into them. Thus it is important to configure your Docker image so that it has SSH server installed. You can rely on `https://quay.io/repository/mateusz_blaszkowski/pkb-k8s ` while creating your own image.

**Kubernetes cluster configuration**  
If your Kubernetes cluster is running on CoreOS:

1. Fix `$PATH` environment variable so that the appropriate binaries can be found:

   ```
   sudo mkdir /etc/systemd/system/kubelet.service.d
   sudo vim /etc/systemd/system/kubelet.service.d/10-env.conf
   ```
   Add the following line to `[Service]` section:
   ```
   Environment=PATH=/opt/bin:/usr/bin:/usr/sbin:$PATH
   ```
2. Reboot the node:
   ```
   sudo reboot
   ```

Note that some benchmark require to run within a privileged container. By default Kubernetes doesn't allow to schedule Dockers in privileged mode - you have to add `--allow-privileged=true` flag to `kube-apiserver` and each `kubelet` startup commands.

**Ceph integration**  
When you run benchmarks with standard scratch disk type (`--scratch_disk_type=standard` - which is a default option), Ceph storage will be used. There are some configuration steps you need to follow before you will be able to spawn Kubernetes PODs with Ceph volume. On each of Kubernetes-Nodes and on the machine which is running Perfkit benchmarks do the following:

1. Copy `/etc/ceph` directory from Ceph-host  
2. Install `ceph-common` package so that `rbd` command is available

  * If your Kubernetes cluster is running on CoreOS, then you need to create a bash script called `rbd` which will run `rbd` command inside a Docker container:

      ```
      #!/usr/bin/bash
      /usr/bin/docker run -v /etc/ceph:/etc/ceph -v /dev:/dev -v /sys:/sys  --net=host --privileged=true --rm=true ceph/rbd $@
      ```
      Save the file as 'rbd'. Then:
      ```
      chmod +x rbd
      sudo mkdir /opt/bin
      sudo cp rbd /opt/bin
      ```
      Install `rbdmap` (https://github.com/ceph/ceph-docker/tree/master/examples/coreos/rbdmap):
      ```
      git clone https://github.com/ceph/ceph-docker.git
      cd ceph-docker/examples/coreos/rbdmap/
      sudo mkdir /opt/sbin
      sudo cp rbdmap /opt/sbin
      sudo cp ceph-rbdnamer /opt/bin
      sudo cp 50-rbd.rules /etc/udev/rules.d
      sudo reboot
      ```



You have two Ceph authentication options available (http://kubernetes.io/v1.0/examples/rbd/README.html):

1. Keyring - pass the path to the keyring file using `--ceph_keyring` flag
2. Secret. In this case you have to create a secret first:

   Retrieve base64-encoded Ceph admin key:
   ```
   ceph auth get-key client.admin | base64
   QVFEYnpPWlZWWnJLQVJBQXdtNDZrUDlJUFo3OXdSenBVTUdYNHc9PQ==  
   ```
   Create a file called `create_ceph_admin.yml` and replace the `key` value with the output from the previous command:
   ```
   apiVersion: v1
   kind: Secret
   metadata:
     name: my-ceph-secret
   data:
     key: QVFEYnpPWlZWWnJLQVJBQXdtNDZrUDlJUFo3OXdSenBVTUdYNHc9PQ==
   ```
   Add secret to Kubernetes:  
   ```
   kubectl create -f create_ceph_admin.yml
   ```
   You will have to pass the Secret name (using `--ceph_secret` flag) when running the benchmakrs. In this case it should be: `--ceph_secret=my-ceph-secret`.

## Cloudstack: Install `csapi` and set the API keys
```
sudo pip install csapi
```

Get the API key and SECRET from Cloudstack. Set the following environement variables.

```bash
export CS_API_URL=<insert API endpoint>
export CS_API_KEY=<insert API key>
export CS_API_SECRET=<insert API secret>
```

Specify the network offering when running the benchmark. If using VPC
(`--cs_use_vpc`), also specify the VPC offering (`--cs_vpc_offering`).

```bash
./pkb.py --cloud=CloudStack --benchmarks=ping --cs_network_offering=DefaultNetworkOffering
```

## Install AWS CLI and setup authentication
Make sure you have installed pip (see the section above).

Follow instructions at http://aws.amazon.com/cli/ or run the following command (omit the 'sudo' on Windows)
```
$ sudo pip install awscli
```
Navigate to the AWS console to create access credentials: https://console.aws.amazon.com/ec2/
* On the console click on your name (top left)
* Click on "Security Credentials"
* Click on "Access Keys", the create New Access Key. Download the file, it contains the Access key and Secret keys
  to access services. Note the values and delete the file.

Configure the CLI using the keys from the previous step
```
$ aws configure
```

## Windows Azure CLI and credentials
You first need to install node.js and NPM.
This version of Perfkit Benchmarker is compatible with azure version 0.9.9.

Go [here](https://nodejs.org/download/), and follow the setup instructions.

Next, run the following (omit the `sudo` on Windows):

```
$ sudo npm install azure-cli@0.9.9 -g
$ azure account download
```

Read the output of the previous command. It will contain a webpage URL. Open that in a browser. It will download
a file (`.publishsettings`) file. Copy to the folder you're running PerfKit Benchmarker. In my case the file was called
`Free Trial-7-18-2014-credentials.publishsettings`
```
$ azure account import [path to .publishsettings file]
```

Test that azure is installed correctly
```
$ azure vm list
```

## DigitalOcean configuration and credentials

PerfKitBenchmarker uses the *curl* tool to interact with
DigitalOcean's REST API. This API uses oauth for authentication.
Please set this up as follows:

Log in to your DigitalOcean account and create a Personal Access Token
for use by PerfKitBenchmarker with read/write access in Settings /
API: https://cloud.digitalocean.com/settings/applications

Save a copy of the authentication token it shows, this is a
64-character hex string.

Create a curl configuration file containing the needed authorization
header. The double quotes are required. Example:

```
$ cat > ~/.config/digitalocean-oauth.curl
header = "Authorization: Bearer 9876543210fedc...ba98765432"
^D
```

Confirm that the authentication works:

```
$ curl --config ~/.config/digitalocean-oauth.curl https://api.digitalocean.com/v2/sizes
{"sizes":[{"slug":"512mb","memory":512,"vcpus":1,...
```

PerfKitBenchmarker uses the file location `~/.config/digitalocean-oauth.curl`
by default, you can use the `--digitalocean_curl_config` flag to
override the path.


## Installing CLIs and credentials for Rackspace

In order to interact with the Rackspace Public Cloud, PerfKitBenchmarker makes
use of the Nova, and the Neutron CLI clients with the Rackspace extensions.

To run PerfKitBenchmarker against Rackspace is very easy. First, install the
CLI clients as follows:
```bash
pip install -U rackspace-neutronclient
pip install -U rackspace-novaclient
```

Once these are installed, all we need to do is to set 3 environment variables,
```bash
export OS_USERNAME=<your_rackspace_username>
export OS_PASSWORD=<your_rackspace_API_key>
export OS_TENANT_NAME=<your_rackspace_account_number>
```

For a Rackspace UK Public Cloud account, an extra environment variable has to
be set, please remember that only the LON region is available under
a Rackspace UK Public Cloud account.
```bash
export OS_AUTH_URL=https://lon.identity.api.rackspacecloud.com/v2.0/

export OS_USERNAME=<your_rackspace_uk_username>
export OS_PASSWORD=<your_rackspace_uk_API_key>
export OS_TENANT_NAME=<your_rackspace_uk_account_number>
```
*Tip*: Put these variables in a file, and simple source them to your shell with
`source <filename>` 

**Note:** Not all flavors are supported on every region. Always check first
if the flavor is supported in the region.

## Create and Configure a `.boto` file for object storage benchmarks

In order to run object storage benchmark tests, you need to have a properly configured `~/.boto` file.

Here is how:

* Create the `~/.boto` file (If you already have ~/.boto, you can skip this step. Consider making a backup copy of your existing .boto file.)

To create a new `~/.boto` file, issue the following command and follow the instructions given by this command:
```
$ gsutil config
```
As a result, a `.boto` file is created under your home directory.

* Open the `.boto` file and edit the following fields:
1. In the [Credentials] section:

`gs_oauth2_refresh_token`: set it to be the same as the `refresh_token` field in your gcloud credential file (~/.config/gcloud/credentials), which was setup as part of the `gcloud auth login` step.

`aws_access_key_id`, `aws_secret_access_key`: set these to be the AWS access keys you intend to use for these tests, or you can use the same keys as those in your existing AWS credentials file (`~/.aws/credentials`).

2. In the `[GSUtil]` section:

`default_project_id`: if it is not already set, set it to be the google cloud storage project ID you intend to use for this test. (If you used `gsutil config` to generate the `.boto` file, you should have been prompted to supply this information at this step).

3. In the [OAuth2] section:
`client_id`, `client_secret`: set these to be the same as those in your gcloud credentials file (`~/.config/gcloud/credentials`), which was setup as part of the 'gcloud auth login' step.


## Install PerfKit

[Download PerfKitBenchmarker](http://github.com/GoogleCloudPlatform/PerfKitBenchmarker/releases) from GitHub.

## Install PerfKit Benchmakrer dependencies
```
$ cd /path/to/PerfKitBenchmarker
$ sudo pip install -r requirements.txt
```

RUNNING A SINGLE BENCHMARK
==========================
PerfKitBenchmarks can run benchmarks both on Cloud Providers (GCP,
AWS, Azure, DigitalOcean) as well as any "machine" you can SSH into.

## Example run on GCP
```
$ ./pkb.py --project=<GCP project ID> --benchmarks=iperf --machine_type=f1-micro
```

## Example run on AWS
```
$ cd PerfKitBenchmarker
$ ./pkb.py --cloud=AWS --benchmarks=iperf --machine_type=t1.micro
```

## Example run on Azure
```
$ ./pkb.py --cloud=Azure --machine_type=ExtraSmall --benchmarks=iperf
```

## Example run on DigitalOcean
```
$ ./pkb.py --cloud=DigitalOcean --machine_type=16gb --benchmarks=iperf
```

## Example run on OpenStack
```
$ ./pkb.py --cloud=OpenStack --benchmarks=iperf --os_auth_url=http://localhost:5000/v2.0/
```

## Example run on Kubernetes
```
$ ./pkb.py --cloud=Kubernetes --benchmarks=iperf --kubectl=/path/to/kubectl --kubeconfig=/path/to/kubeconfig --image=image-with-ssh-server  --ceph_monitors=10.20.30.40:6789,10.20.30.41:6789 --kubernetes_nodes=10.20.30.42,10.20.30.43
```

## Example run on CloudStack
```bash
./pkb.py --cloud=CloudStack --benchmarks=ping --cs_network_offering=DefaultNetworkOffering
```

## Example run on Rackspace
```
$ ./pkb.py --cloud=Rackspace --machine_type=general1-2 --benchmarks=iperf
```

HOW TO RUN WINDOWS BENCHMARKS
==================
You must be running on a Windows machine in order to run Windows benchmarks.
Install all dependencies as above and set TrustedHosts to accept all hosts so
that you can open PowerShell sessions with the VMs (both machines having each
other in their TrustedHosts list is neccessary, but not sufficient to issue
remote commands; valid credentials are still required):

```
set-item wsman:\localhost\Client\TrustedHosts -value *
```

Now you can run Windows benchmarks by running with `--os_type=windows`. Windows has a
different set of benchmarks than Linux does. They can be found under
perfkitbenchmarker/windows_benchmarks/. The target VM OS is Windows Server 2012
R2.

HOW TO RUN ALL STANDARD BENCHMARKS
==================
Run without the --benchmarks parameter and every benchmark in the standard set will run serially which can take a couple of hours (alternatively run with --benchmarks="standard_set").  Additionally if you dont specify --cloud=... all benchmarks will run on the Google Cloud Platform.


HOW TO RUN ALL BENCHMARKS IN A NAMED SET
==================
Named sets are are grouping of one or more benchmarks in the benchmarking directory. This feature allows parallel innovation of what is important to measure in the Cloud, and is defined by the set owner. For example the GoogleSet is maintained by Google, whereas the StanfordSet is managed by Stanford. Once a quarter a meeting is held to review all the sets to determine what benchmarks should be promoted to the standard_set. The Standard Set is also reviewed to see if anything should be removed.
To run all benchmarks in a named set, specify the set name in the benchmarks parameter (e.g. --benchmarks="standard_set"). Sets can be combined with individual benchmarks or other named sets.


USEFUL GLOBAL FLAGS
==================

The following are some common flags used when configuring
PerfKitBenchmaker.

Flag | Notes
-----|------
`--help`       | see all flags
`--cloud`      | Cloud where the bechmarks are run. See the table below for choices.
`--zone`       | This flag allows you to override the default zone. See the table below.
`--benchmarks` | A comma separated list of benchmarks or benchmark sets to run such as `--benchmarks=iperf,ping` . To see the full list, run `./pkb.py --help`

The default cloud is 'GCP', override with the `--cloud` flag. Each cloud has a default
zone which you can override with the `--zone` flag, the flag supports the same values
that the corresponding Cloud CLIs take:

Cloud name | Default zone | Notes
-------|---------|-------
GCP | us-central1-a | |
AWS | us-east-1a | |
Azure | East US | |
DigitalOcean | sfo1 | You must use a zone that supports the features 'metadata' (for cloud config) and 'private_networking'.
OpenStack | nova | |
CloudStack | QC-1 | |
Rackspace | IAD | OnMetal machine-types are available only in IAD zone
Kubernetes | k8s | |

Example:

```bash
./pkb.py --cloud=GCP --zone=us-central1-a --benchmarks=iperf,ping
```

## Proxy configuration for VM guests.

If the VM guests do not have direct Internet access in the cloud
environment, you can configure proxy settings through `pkb.py` flags.

To do that simple setup three flags (All urls are in notation ): The
flag values use the same `<protocol>://<server>:<port>` syntax as the
corresponding environment variables, for example
`--http_proxy=http://proxy.example.com:8080` .

Flag | Notes
-----|------
`--http_proxy`       | Needed for package manager on Guest OS and for some Perfkit packages
`--https_proxy`      | Needed for package manager or Ubuntu guest and for from github downloaded packages
`--ftp_proxy`       | Needed for some Perfkit packages

CONFIGURATIONS AND CONFIGURATION OVERRIDES
==================
Each benchmark now has an independent configuration which is written in YAML.
Users may override this default configuration by providing a configuration.
This allows for much more complex setups than previously possible,
including running benchmarks across clouds.

A benchmark configuration has a somewhat simple structure. It is essentially
just a series of nested dictionaries. At the top level, it contains VM groups.
VM groups are logical groups of homogenous machines. The VM groups hold both a
`vm_spec` and a `disk_spec` which contain the parameters needed to
create members of that group. Here is an example of an expanded configuration:
```
hbase_ycsb:
  vm_groups:
    loaders:
      vm_count: 4
      vm_spec:
        GCP:
          machine_type: n1-standard-1
          image: ubuntu-14-04
          zone: us-central1-c
        AWS:
          machine_type: m3.medium
          image: ami-######
          zone: us-east-1a
        # Other clouds here...
      # This specifies the cloud to use for the group. This allows for
      # benchmark configurations that span clouds.
      cloud: AWS
      # No disk_spec here since these are loaders.
    master:
      vm_count: 1
      cloud: GCP
      vm_spec:
        GCP:
          machine_type: n1-standard-1
          image: ubuntu-14-04
          zone: us-central1-c
        # Other clouds here...
      disk_count: 1
      disk_spec:
        GCP:
          disk_size: 100
          disk_type: standard
          mount_point: /scratch
        # Other clouds here...
    workers:
      vm_count: 4
      cloud: GCP
      vm_spec:
        GCP:
          machine_type: n1-standard-4
          image: ubuntu-14-04
          zone: us-central1-c
        # Other clouds here...
      disk_count: 1
      disk_spec:
        GCP:
          disk_size: 500
          disk_type: remote_ssd
          mount_point: /scratch
        # Other clouds here...
```

For a complete list of keys for `vm_spec`s and `disk_spec`s see
[virtual_machine.BaseVmSpec](https://github.com/GoogleCloudPlatform/PerfKitBenchmarker/blob/master/perfkitbenchmarker/virtual_machine.py)
and
[disk.BaseDiskSpec](https://github.com/GoogleCloudPlatform/PerfKitBenchmarker/blob/master/perfkitbenchmarker/disk.py)
and their derived classes.

User configs are applied on top of the existing default config and can be
specified in two ways. The first is by supplying a config file via the
`--benchmark_config_file` flag. The second is by specifying a single setting to
override via the `--config_override` flag.

A user config file only needs to specify the settings which it is intended to
override. For example if the only thing you want to do is change the number of
VMs for the `cluster_boot` benchmark, this config is sufficient:
```
cluster_boot:
  vm_groups:
    default:
      vm_count: 100
```
You can achieve the same effect by specifying the `--config_override` flag.
The value of the flag should be a path within the YAML (with keys delimited by
periods), an equals sign, and finally the new value:
```
--config_override=cluster_boot.vm_groups.default.vm_count=100
```
See the section below for how to use static (i.e. pre-provisioned) machines in your config.

ADVANCED: HOW TO RUN BENCHMARKS WITHOUT CLOUD PROVISIONING (eg: local workstation)
==================
It is possible to run PerfKitBenchmarker without running the Cloud provioning steps.  This is useful if you want to run on a local machine, or have a benchmark like iperf run from an external point to a Cloud VM.

In order to do this you need to make sure:
* The static (ie not provisioned by PerfKitBenchmarker) machine is ssh'able
* The user PerfKitBenchmarker will login as has 'sudo' access.  (*** Note we hope to remove this restriction soon ***)

Next you will want to create a YAML user config file describing how to connect to the machine as follows:
```
static_vms:
  - &vm1 # Using the & character creates an anchor that we can
         # reference later by using the same name and a * character.
    ip_address: 170.200.60.23
    user_name: voellm
    ssh_private_key: /home/voellm/perfkitkeys/my_key_file.pem
    zone: Siberia
    disk_specs:
      - mount_point: /data_dir
```


* The `ip_address` is the address where you want benchmarks to run.
* `ssh_private_key` is where to find the private ssh key.
* `zone` can be anything you want.  It is used when publishing results.
* `disk_specs` is used by all benchmarks which use disk (i.e., `fio`, `bonnie++`, many others).

In the same file, configure any number of benchmarks (in this case just iperf),
and reference the static VM as follows:
```
iperf:
  vm_groups:
    iperf_vm_1:
      static_vms:
        - *vm1
```

I called my file iperf.yaml and used it to run iperf from Siberia to a GCP VM in us-central1-f as follows:
```
./pkb.py --benchmarks=iperf --machine_type=f1-micro --benchmark_config_file=iperf.yaml --zone=us-central1-f --ip_addresses=EXTERNAL
```
* ip_addresses=EXTERNAL tells PerfKitBechmarker not to use 10.X (ie Internal) machine addresses that all Cloud VMs have.  Just use the external IP address.

If a benchmark requires two machines like iperf, you can have two machines in the same YAML file as shown below.  This means you can indeed run between two machines and never provision any VM's in the Cloud.

```
static_vms:
  - &vm1
    ip_address: <ip1>
    user_name: connormccoy
    ssh_private_key: /home/connormccoy/.ssh/google_compute_engine
    internal_ip: 10.240.223.37
    install_packages: false
  - &vm2
    ip_address: <ip2>
    user_name: connormccoy
    ssh_private_key: /home/connormccoy/.ssh/google_compute_engine
    internal_ip: 10.240.234.189
    ssh_port: 2222

iperf:
  vm_groups:
    iperf_vm_1:
      static_vms:
        - *vm2
    iperf_vm_2:
      static_vms:
        - *vm1
```

SPECIFYING FLAGS IN CONFIGURATION FILES
=================
You can now specify flags in configuration files by using the `flags` key at the
top level in a benchmark config. The expected value is a dictionary mapping
flag names to their new default values. The flags are only defaults; it's still
possible to override them via the command line. It's even possible to specify
conflicting values of the same flag in different benchmarks:

```
iperf:
  flags:
    machine_type: n1-standard-2
    zone: us-central1-b
    iperf_sending_thread_count: 2

netperf:
  flags:
    machine_type: n1-standard-8
```

The new defaults will only apply to the benchmark in which they are specified.


HOW TO EXTEND PerfKitBenchmarker
=================
First start with the [CONTRIBUTING.md] (https://github.com/GoogleCloudPlatform/PerfKitBenchmarker/blob/master/CONTRIBUTING.md)
file.  It has the basics on how to work with PerfKitBenchmarker, and how to submit your pull requests.

In addition to the [CONTRIBUTING.md] (https://github.com/GoogleCloudPlatform/PerfKitBenchmarker/blob/master/CONTRIBUTING.md)
file we have added a lot of comments into the code to make it easy to;
* Add new benchmarks (eg: --benchmarks=<new benchmark>)
* Add new package/os type support (eg: --os_type=<new os type>)
* Add new providers (eg: --cloud=<new provider>)
* etc...

Even with lots of comments we make to support more detailed documention.  You will find the documatation we have on the [Wiki pages] (https://github.com/GoogleCloudPlatform/PerfKitBenchmarker/wiki).  Missing documentation you want?  Start a page and/or open an [issue] (https://github.com/GoogleCloudPlatform/PerfKitBenchmarker/issues) to get it added.

INTEGRATION TESTING
===================

In addition to regular unit tests, which are run via `hooks/check-everything`,
PerfKitBenchmarker has integration tests, which create actual cloud resources
and take time and money to run. For this reason, they will only run when the
variable PERFKIT_INTEGRATION is defined in the environment. For instance, the
command

  `PERFKIT_INTEGRATION=1 hooks/check-everything`

will run the integration tests. The integration tests depend on having installed
and configured all of the relevant cloud provider SDKs, and will fail if you
have not done so.


PLANNED IMPROVEMENTS
=======================
Many... please add new requests via GitHub issues.
