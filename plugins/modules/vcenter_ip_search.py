#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vcenter_helper import VMwareAPI

def main():
    module_args = dict(
        ip_address=dict(type='str', required=True),
        vcenter_host=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        ssl_verify=dict(type='bool', required=False, default=False)
    )

    results = dict(
        changed=False,
        ip_test=None,
        error=None
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ip_address = module.params['ip_address']
    vcenter_host = module.params['vcenter_host']
    username = module.params['username']
    password = module.params['password']
    ssl_verify = module.params['ssl_verify']

    vmware_api = VMwareAPI(vcenter_host, username, password, ssl_verify)

    try:
        search_result = vmware_api.search_ip_address(ip_address)
        results['ip_test'] = search_result
    except Exception as e:
        results['error'] = str(e)
        module.fail_json(msg=results['error'])

    module.exit_json(**results)

if __name__ == '__main__':
    main()
