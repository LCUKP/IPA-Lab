import os
import paramiko
from netmiko import ConnectHandler

KEY_PATH = r"C:\Users\dtac6\.ssh\id_rsa"

devices = [
    {
        "device_type": "cisco_ios",
        "ip": "172.31.29.3",
        "username": "admin",
        "use_keys": True,
        "key_file": KEY_PATH,
        "banner_timeout": 30,
        "disabled_algorithms": {
            "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"],
        },
        "ssh_config_file": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "172.31.29.4",
        "username": "admin",
        "use_keys": True,
        "key_file": KEY_PATH,
        "banner_timeout": 30,
        "disabled_algorithms": {
            "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"],
        },
        "ssh_config_file": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "172.31.29.5",
        "username": "admin",
        "use_keys": True,
        "key_file": KEY_PATH,
        "banner_timeout": 30,
        "disabled_algorithms": {
            "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"],
        },
        "ssh_config_file": False,
    }
]

s1_configs = [
    "vlan 101",
    "name control_data_plane",
    "interface GigabitEthernet0/1",
    "switchport mode access",
    "switchport access vlan 101",
    "no shutdown",
    "interface GigabitEthernet0/2",
    "switchport mode access",
    "switchport access vlan 101",
    "no shutdown",
    "access-list 10 permit 172.31.29.0 0.0.0.255",
    "line vty 0 4",
    "access-class 10 in"
]

r1_configs = [
    "interface GigabitEthernet0/1",
    "ip vrf forwarding control-data",
    "ip address 10.10.29.1 255.255.255.0",
    "no shutdown",
    "interface GigabitEthernet0/2",
    "ip vrf forwarding control-data",
    "ip address 10.29.30.1 255.255.255.252",
    "no shutdown",
    "router ospf 1 vrf control-data",
    "router-id 1.1.1.1",
    "network 10.10.29.0 0.0.0.255 area 0",
    "network 10.29.30.0 0.0.0.3 area 0",
    "access-list 10 permit 172.31.29.0 0.0.0.255",
    "line vty 0 4",
    "access-class 10 in"
]

r2_configs = [
    "interface GigabitEthernet0/1",
    "ip vrf forwarding control-data",
    "ip address 10.29.30.2 255.255.255.252",
    "ip nat inside",
    "no shutdown",
    "interface GigabitEthernet0/2",
    "ip vrf forwarding control-data",
    "ip address 10.20.29.1 255.255.255.0",
    "ip nat inside",
    "no shutdown",
    "interface GigabitEthernet0/3",
    "ip address dhcp",
    "ip nat outside",
    "no shutdown",
    "router ospf 1 vrf control-data",
    "router-id 2.2.2.2",
    "network 10.20.29.0 0.0.0.255 area 0",
    "network 10.29.30.0 0.0.0.3 area 0",
    "default-information originate always",
    "ip route vrf control-data 0.0.0.0 0.0.0.0 192.168.122.1",
    "access-list 1 permit 10.0.0.0 0.255.255.255",
    "ip nat inside source list 1 interface GigabitEthernet0/3 vrf control-data overload",
    "access-list 10 permit 172.31.29.0 0.0.0.255",
    "line vty 0 4",
    "access-class 10 in"
]

for dev in devices:
    ip = dev['ip']
    print(f"\n--- Deploying configuration to {ip} ---")
    
    try:
        with ConnectHandler(**dev) as ssh:
            if ip == '172.31.29.3':
                output = ssh.send_config_set(s1_configs)
            elif ip == '172.31.29.4':
                output = ssh.send_config_set(r1_configs)
            elif ip == '172.31.29.5':
                output = ssh.send_config_set(r2_configs)
                
            print(output)
            save_out = ssh.save_config()
            print(f"Successfully configured and saved {ip}")
            
    except Exception as e:
        print(f"Failed to configure {ip}: {e}")