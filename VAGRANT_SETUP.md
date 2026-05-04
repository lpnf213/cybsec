# Kali Linux Vagrant Environment Setup

This guide provides instructions on how to install the necessary tools and how to manage the Kali Linux Virtual Machine used for this project.

## 1. Prerequisites Installation

To run this environment, you will need to install a hypervisor (VMware or VirtualBox) and Vagrant. We recommend **VMware** for better performance.

### Step 1: Install VMware
VMware Workstation Pro is now free for personal use.
*   **Download Link:** [VMware Workstation Pro](https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware%20Workstation%20Pro) (Requires creating a free Broadcom account).
*   Run the installer and follow the standard Windows installation prompts.

### Step 2: Install Vagrant
Vagrant is the tool that automates the creation and provisioning of the Virtual Machine.
*   **Download Link:** [Vagrant by HashiCorp](https://developer.hashicorp.com/vagrant/install)
*   Download the Windows installer and run it. **You will need to restart your computer** after the installation is complete.

### Step 3: Install the Vagrant VMware Utility & Plugin
If you are using VMware, Vagrant requires a specific utility and plugin to communicate with it.
1.  **Download and Install the Utility:** [Vagrant VMware Utility](https://developer.hashicorp.com/vagrant/docs/providers/vmware/vagrant-vmware-utility)
2.  **Install the Plugin:** Open your Windows Terminal (PowerShell or Command Prompt) and run the following command to install the plugin:
    ```bash
    vagrant plugin install vagrant-vmware-desktop
    ```

*(Note: If you decide to use VirtualBox instead of VMware, you only need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and Vagrant. No extra plugins are required.)*

---

## 2. Managing the Environment

Once the prerequisites are installed, open a terminal in the root of this repository (`c:\repository\cybsec`).

### Starting the VM
To create and start the virtual machine, run:
```bash
vagrant up
```
*The first time you run this, it will download the Kali Linux image and install Python and your project requirements. This may take 5-10 minutes.*

### Accessing the VM
To open a secure shell (SSH) session into the running Kali Linux VM, run:
```bash
vagrant ssh
```
*(Note: If you ever need to manually log in, use the default Vagrant credentials: Username `vagrant`, Password `vagrant`. You also have passwordless `sudo` privileges.)*

### Running Your Python Code
Inside the VM, your Windows repository is automatically synced to the `/vagrant` directory.
1. Navigate to your source code folder:
   ```bash
   cd /vagrant/src
   ```
2. Run your scripts! Because tools like `netfilterqueue` require root access to interact with the Linux kernel networking, you MUST run your script as root using `sudo`. 
To ensure it uses the packages from your virtual environment, use the full path to the Python environment like this:
   ```bash
   sudo /home/vagrant/venv/bin/python main.py
   ```

### Checking Network Configuration
Since the VM is configured with a bridged network, it will receive its own IP address from your local router. To view your network interfaces and find this IP address, run the following command inside the VM:
```bash
ip addr
```
Look for an interface (usually `eth1` or `eth2`, as `eth0` is strictly used by Vagrant for NAT) that has an IP address matching your local network subnet (for example, `192.168.1.x`).

### Using a USB Wi-Fi Adapter (Monitor Mode)
If you have an external USB Wi-Fi adapter and want to use it for wireless attacks or monitor mode, you must pass it directly to the VM:
1. Plug the USB Wi-Fi adapter into your physical computer.
2. Ensure the Virtual Machine is running and the VMware window is open (we enabled the GUI for this reason).
3. In the VMware window menu at the very top, click on **VM** -> **Removable Devices**.
4. Find your USB Wi-Fi adapter in the list, hover over it, and click **Connect (Disconnect from Host)**.
5. Inside the Kali terminal, run `iwconfig`. You should now see a `wlan0` interface ready to use!

#### Connecting to Wi-Fi via Command Line
If you want to use your D-Link adapter to actually connect to the internet (instead of monitor mode), you can use the `nmcli` tool:
1. Scan for nearby Wi-Fi networks:
   ```bash
   nmcli device wifi list
   ```
2. Connect to your Wi-Fi network (replace `SSID_NAME` and `YOUR_PASSWORD`):
   ```bash
   sudo nmcli device wifi connect "SSID_NAME" password "YOUR_PASSWORD"
   ```

### Stopping and Cleaning Up
*   **Stop the VM:** To gracefully shut down the VM when you are done working:
    ```bash
    vagrant halt
    ```
*   **Re-run Provisioning:** If you update your `requirements.txt` and want Vagrant to install the new packages:
    ```bash
    vagrant provision
    ```
*   **Delete the VM:** If you want to completely destroy the VM to free up disk space (your code in Windows will **not** be deleted):
    ```bash
    vagrant destroy
    ```
