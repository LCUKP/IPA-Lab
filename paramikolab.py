import paramiko
import time

devices = [
    {"name": "R0-P", "ip": "172.31.29.1"},
    {"name": "S0-P", "ip": "172.31.29.2"},
    {"name": "S1-P", "ip": "172.31.29.3"},
    {"name": "R1-P", "ip": "172.31.29.4"},
    {"name": "R2-P", "ip": "172.31.29.5"},
]

private_key_path = r"C:\Users\dtac6\.ssh\id_rsa"

for dev in devices:
    print(f"\n==========================================")
    print(f"Connecting to {dev['name']} ({dev['ip']})")
    print(f"==========================================")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh.connect(
            dev['ip'],
            username="admin",
            pkey=key,
            look_for_keys=False,
            allow_agent=False
        )
        print(f"[SUCCESS] Connected to {dev['name']}")

        shell = ssh.invoke_shell()
        #shell.send("show ip interface brief\n")
        time.sleep(2)

        #output = shell.recv(65535).decode("utf-8")
        #print(output)

    except Exception as e:
        print(f"[ERROR] {dev['name']}: {e}")

    finally:
        ssh.close()
        print(f"Closed {dev['name']}\n")