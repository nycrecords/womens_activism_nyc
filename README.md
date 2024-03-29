# Womens Activism #
## Development Environment Setup ##
*Make sure your version of VirtualBox matches the version used to create the vagrant box.*

1. Copy `rhel-6.8.virtualbox.box` from the repository into your desired directory.
2. Run `vagrant box add rhel-6.8 <path-to-box-file>`
    - If you change the name of the box, remember to edit Vagrantfile (config.vm.box)
3. Clone this repository.
4. Copy `Vagrantfile.example` into `Vagrantfile`
5. Add your RedHat Developer credentials to `Vagrantfile`
    - If you do not have a developer account, [create one](https://www.redhat.com/en/developers).
6. Run `vagrant plugin install vagrant-reload vagrant-vbguest`
7. Run `vagrant up`
    - If there is an error during this process, try running `vagrant provision`
8. Run `vagrant ssh` to connect to your development environment.