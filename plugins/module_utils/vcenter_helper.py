from ansible.errors import AnsibleError
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError  

class VMwareAPI:
    def __init__(self, vcenter_host, username, password, ssl_verify):
        self.vcenter_host = vcenter_host
        self.session = requests.Session()
        self.authenticate(username, password, ssl_verify)

    def authenticate(self, username, password, ssl_verify=False):

        #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        auth_url = f"https://{self.vcenter_host}/rest/com/vmware/cis/session"

        if not ssl_verify:
            # Suppress InsecureRequestWarning when SSL verification is disabled
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            response = self.session.post(auth_url, auth=HTTPBasicAuth(username, password), verify=ssl_verify)

            # Check for successful authentication
            if response.status_code == 200:
                print("Authentication successful.")
            else:
                print("Failed to authenticate.")
                #response.raise_for_status()

        except Exception as e:
            print(f"Authentication failed: {e}")


    def search_ip_address(self, ip_address):
        """
        Search for an IP address among VMs.
        """
        vms_url = f"https://{self.vcenter_host}/rest/vcenter/vm"
        response = self.session.get(vms_url)
        value = "Pass"

        if response.status_code == 200:
            vms = response.json().get('value', [])
        else:
            print("Failed to retrieve VMs.")
            response.raise_for_status()

        for vm in vms:
            if self.search_ip_address_in_vm(vm, ip_address):
                vm_name = vm['name']
                value = f"This IP has been claimed by:  {vm_name}"
        return value


    def search_ip_address_in_vm(self, vm, ip_address):
        """
        Search for an IP address in a single VM.
        """
        vm_network_info = self.get_vm_guest_network_info(vm['vm'])

        if vm_network_info is None or len(vm_network_info['value']) == 0:
            return False
                
        for interface in vm_network_info['value']:
            for ip in interface['ip']['ip_addresses']:
                if ip['ip_address'] == ip_address:
                    return True

    def get_vm_guest_network_info(self, vm_id):
        """
        Retrieve network information for a specific virtual machine.
        """
        try:
            network_info_url = f"https://{self.vcenter_host}/rest/vcenter/vm/{vm_id}/guest/networking/interfaces"
            response = self.session.get(network_info_url)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            if response.status_code == 503:
                return None
            else:
                print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
