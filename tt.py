from plugins.module_utils.vcenter_helper import VMwareAPI

ip = '192.168.2.10'
vma = VMwareAPI('vcenter.lou.land','administrator@lou.land','Gr33k*G0d7',False)
#srr = vma.search_ip_address(ip)

srr = vma.search_ip_address_in_hosts(ip)
print(srr)