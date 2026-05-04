Vagrant.configure("2") do |config|
  # Force Vagrant to use VMware by default
  ENV['VAGRANT_DEFAULT_PROVIDER'] = 'vmware_desktop'
  
  # We use the official Kali Linux rolling release box
  config.vm.box = "kalilinux/rolling"
  
  # Enable bridged networking so the VM appears on the local network
  config.vm.network "public_network"
  
  # The directory containing the Vagrantfile is automatically synced to /vagrant.
  # We don't need to specify it explicitly unless we want to change the path.

  # Configuration for VMware Desktop (preferred if you have it)
  config.vm.provider "vmware_desktop" do |v|
    v.gui = true
    v.memory = "2048"
    v.cpus = 2
    # Disable 3D acceleration to fix invisible mouse bug
    v.vmx["mks.enable3d"] = "FALSE"
    # Enable USB controllers for Wi-Fi Adapter passthrough
    v.vmx["usb.present"] = "TRUE"
    v.vmx["ehci.present"] = "TRUE"
    v.vmx["usb_xhci.present"] = "TRUE"
  end

  # Shell provisioner to setup Python and the virtual environment
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    echo "Updating apt repositories..."
    apt-get update -y
    
    echo "Installing Python 3, venv, system packages, and GUI tools..."
    apt-get install -y python3 python3-venv python3-pip python3-netfilterqueue open-vm-tools-desktop
    
    echo "Creating virtual environment at /home/vagrant/venv..."
    rm -rf /home/vagrant/venv
    sudo -u vagrant python3 -m venv --system-site-packages /home/vagrant/venv
    
    echo "Installing requirements from /vagrant/requirements.txt..."
    if [ -f /vagrant/requirements.txt ]; then
      sudo -u vagrant /home/vagrant/venv/bin/pip install -r /vagrant/requirements.txt
    else
      echo "No requirements.txt found in /vagrant. Skipping pip install."
    fi
    
    echo "---------------------------------------------------------"
    echo "Provisioning complete!"
    echo "To use the virtual environment inside the VM, run:"
    echo "source /home/vagrant/venv/bin/activate"
    echo "---------------------------------------------------------"
  SHELL
end
