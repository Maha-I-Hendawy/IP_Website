import ipaddress


ip = input("Enter Your IP Address: ")

ip_net = input("Enter Your IP Netweork")



ip_address = ipaddress.ip_address(ip)

ip_network = ipaddress.ip_network(ip_net)


def check(ipaddr, ipnet):
	if ipaddr in ipnet:
		print("Yes, it's in the network")
	else:
		print("Sorry, it's not in the network")




