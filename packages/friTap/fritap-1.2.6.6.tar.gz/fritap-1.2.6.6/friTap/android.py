#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import exists as file_exists
import os
import frida
import subprocess
import sys
import shlex

if sys.version_info >= (3,10):
    from importlib.resources import files


class Android:
    
    def __init__(self,debug_infos=False, arch=""):
        self.dst_path = "/data/local/tmp/"
        self.device = None
        self.pcap_name = ""
        self.print_debug_infos = debug_infos
        self.is_magisk_mode = False
        self.do_we_have_an_android_device = False
        if self._is_Android():
            self.tcpdump_version = self._get_appropriate_android_tcpdump_version(arch)
            self.adb_check_root() # set is_magisk_mode

        
    def adb_check_root(self):
        if bool(subprocess.run(['adb', 'shell','su -v'], capture_output=True, text=True).stdout):
            self.is_magisk_mode = True
            return True

        return bool(subprocess.run(['adb', 'shell','su 0 id -u'], capture_output=True, text=True).stdout)
    
    def run_adb_command_as_root(self,command):
        if self.adb_check_root() == False:
            print("[-] none rooted device. Please root it before trying a full-capture with friTap and ensure that you are able to run commands with the su-binary....")
            exit(2)

        if self.is_magisk_mode:
            output = subprocess.run(['adb', 'shell','su -c '+command], capture_output=True, text=True)
        else:
            output = subprocess.run(['adb', 'shell','su 0 '+command], capture_output=True, text=True)
            
        return output

    def _adb_push_file(self,file,dst):
        output = subprocess.run(['adb', 'push',file,dst], capture_output=True, text=True)
        return output
    
    def _adb_pull_file(self,src_file,dst):
        output = subprocess.run(['adb', 'pull',src_file,dst], capture_output=True, text=True)
        return output
    
    def _get_android_device_arch(self):
        frida_usb_json_data = frida.get_usb_device().query_system_parameters()
        return frida_usb_json_data['arch']
    
    
    def _adb_make_binary_executable(self, path):
        output = self.run_adb_command_as_root("chmod +x "+path+self.tcpdump_version)
    
    
    def _get_appropriate_android_tcpdump_version(self,passed_arch):
        arch = ""
        if len(passed_arch)  > 2:
            arch = passed_arch
        else:
            arch = self._get_android_device_arch()
        
        tcpdump_version = ""
        if arch == "arm64":
            tcpdump_version = "tcpdump_arm64_android"
        elif arch == "arm":
            tcpdump_version = "tcpdump_arm32_android"
        elif arch == "ia32":
            tcpdump_version = "tcpdump_x86_android"
        elif arch == "x64":
            tcpdump_version = "tcpdump_x86_64_android"
        else:
            print("[-] unknown arch.\n We can't find your device architecture using frida, please set mobile arch via --m_arch <arm64|arm|ia32|x64>\n[-] Leaving....")
            exit(2)
            
        return tcpdump_version


    def is_tcpdump_available(self):
        try:
            # Check if tcpdump is available on the device
            result = self.run_adb_command_as_root("tcpdump --version")
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error checking tcpdump availability: {e}")
            return False
            
    
    def _get_tcpdump_version(self):
        # Get the path to the current file
        current_dir = os.path.dirname(__file__)

        # Construct the path to the assets directory
        tcpdump_path = os.path.join(current_dir, 'assets', 'tcpdump_binaries', self.tcpdump_version)

        if file_exists(tcpdump_path):
            print(f"[*] installing tcpdump to Android device: {tcpdump_path}")
            return tcpdump_path
        else:
            print("[-] error: can't find "+str(tcpdump_path))
            print("[-] ensure that "+str(tcpdump_path)+" exits\n")
            os._exit(2)
    
    def push_tcpdump_to_device(self):
        self.close_friTap_if_none_android()
        tcpdump_path = self._get_tcpdump_version()
        return_Value = self._adb_push_file(tcpdump_path,self.dst_path)
        

        if return_Value.returncode != 0:
            print("[-] error: " +  return_Value.stderr)
            print("    it might help to adjust the dst_path or to ensure that you have adb in your path\n")
            os._exit(2)
        else:
            self._adb_make_binary_executable(self.dst_path)
            print(f"[*] pushed tcpdump to {self.dst_path} on your android device")
            
    def pull_pcap_from_device(self):
        self.close_friTap_if_none_android()
        pcap_path = self.dst_path + self.pcap_name
        return_Value = self._adb_pull_file(pcap_path,".")
        print(f"[*] pulling capture from device: {return_Value}")
        if self.print_debug_infos:
            print("---------------------------------")
            print(return_Value)
        if return_Value.returncode !=0:
            print(f"[-] error pulling pcap ({pcap_path}) from android device")
    
    def get_pid_via_adb(self, process_name):
        try:
            pid_result =self.run_adb_command_as_root(f"pidof -s {process_name}")
            pid = pid_result.stdout.strip()

            if not pid:
                if self.print_debug_infos:
                    print("[-] No PID found. Process may not be running.")
                return "-1"
            return pid
        except subprocess.CalledProcessError as e:
            if self.print_debug_infos:
                print(f"Error: {e.stderr.strip()}")
            return "-1"
            
    def send_ctrlC_over_adb(self):
        self.close_friTap_if_none_android()
        if self.is_tcpdump_available():
            pid = self.get_pid_via_adb("tcpdump")
        else:
            pid = self.get_pid_via_adb(self.tcpdump_version)
        
        if int(pid) > 0:
            self.run_adb_command_as_root(f"kill -INT {pid}")

    def send_kill_tcpdump_over_adb(self):
        self.close_friTap_if_none_android()
        if self.is_tcpdump_available():
            pid = self.get_pid_via_adb("tcpdump")
        else:
            pid = self.get_pid_via_adb(self.tcpdump_version)
        
        if int(pid) > 0:
            self.run_adb_command_as_root(f"kill -9 {pid}")
        
    def close_friTap_if_none_android(self):
        if self.is_Android == False:
            print("[-] none android device\nclosing friTap...")
            exit(2)
    
    def run_tcpdump_capture(self,pcap_name):
        self.close_friTap_if_none_android()
        self.pcap_name = pcap_name

        if self.is_tcpdump_available():
            tcpdump_cmd = f'tcpdump -U -i any -s 0 -w {self.dst_path}{pcap_name} \\"not \\(tcp port 5555 or tcp port 27042\\)\\"'
        else:
            tcpdump_cmd = f'{self.dst_path}./{self.tcpdump_version} -i any -s 0 -w {self.dst_path}{pcap_name} \\"not \\(tcp port 5555 or tcp port 27042\\)\\"'

        
        if self.is_magisk_mode:
            cmd = f'adb shell su -c "{tcpdump_cmd}"'
        else:
            cmd = f'adb shell su 0 "{tcpdump_cmd}"'

        if self.print_debug_infos:
            print("[*] Running tcpdump in background:", cmd)
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process

    
    def _is_Android(self):
        try:
            subprocess.run(['adb'], capture_output=True, text=True)
        except FileNotFoundError:
            print("[-] can't find adb in your path. Please ensure that adb is installed and in your path if you are trying a full capture on Android.")
            return False
        
        if len(subprocess.run(['adb', 'devices'], capture_output=True, text=True).stdout) > 27:
            self.do_we_have_an_android_device = True
            return True
        else:
            print("[-] No device connected to adb. Ensure that adb devices will print your device if you are trying a full capture on Android.")
            return False
        
    def is_Android(self):
        return self.do_we_have_an_android_device
