# -*- mode: ruby -*-
# vi: set ft=ruby :
# source: https://github.com/jackdb/pg-app-dev-vm

$script = <<SCRIPT
echo I am provisioning...
date > /etc/vagrant_provisioned_at
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: $script
end

Vagrant::Config.run do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.share_folder "bootstrap", "/mnt/bootstrap", ".", :create => true
  config.vm.provision :shell, :path => "Vagrant-setup/bootstrap-pg.sh"

  # my custom provisioning script
  config.vm.provision :shell, :path => "Vagrant-setup/bootstrap-py.sh"

  # PostgreSQL Server port forwarding
  config.vm.forward_port 5432, 15432
end
