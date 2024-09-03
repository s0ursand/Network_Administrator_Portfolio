import ipaddress

menu = input('''
             Type from 1 - x: \n
             1. Convert IPv4 into binary \n
             2. Convert binary IP to decimal \n
             3. Given the subnet in CIDR notation (ex. 24 for /24), outputs subnet in decimal and binary \n
             4. Given the subnet in decimal (ex. 255.255.255.0), outputs it in CIDR notation and binary \n
             5. Given an Ipv4 and its subnet (CIDR notation), calculates network ip, first host, last host, broadcast ip and next subnet \n
             6. Given an IPv4 and how many subnets needed (ex. 192.168.1.0 50), outputs the network IP with CIDR subnet, subnet in decimal and usable ip range for every subnet \n
             > ''')

def ip_to_binary(ip_address):    
     # split ip address into octects
     octects = ip_address.split('.')
     #convert each octect in binary, padding with zeroes to ensure 8 bits
     binary_octects = [format(int(octect), '08b') for octect in octects]
     #join the binary octects into a single string
     binary_ip = '.'.join(binary_octects)
     return binary_ip  

def binary_to_ip(binary_ip):
    #split the binary ip into octects 
    binary_octects = binary_ip.split('.')
    #convert binary to decimal (the 2 is for base 2)
    ip_address = '.'.join(str(int(octect, 2)) for octect in binary_octects)
    return ip_address

def calculate_network_info(ip_cidr):
    #parse the input ip and subnet (CIDR)
    network = ipaddress.IPv4Network(ip_cidr, strict=False)
    #calculate the network address
    network_ip = network.network_address
    #calculate the first host (network + 1)
    first_host = network.network_address + 1
    #last host (broadcast - 1)
    last_host = network.broadcast_address - 1
    #calculate broadcast address
    broadcast_ip = network.broadcast_address
    #next subnet (broadcast + 1)
    next_subnet_ip = network.broadcast_address + 1
    
    return{
        'Network IP': str(network_ip),
        'First Host IP': str(first_host),
        'Last Host IP': str(last_host),
        'Broadcast IP': str(broadcast_ip),
        'Next Subnet IP': str(next_subnet_ip)
            }

if menu == '1':
    ip_address = input('Insert the IPv4 you want to translate in binary:> ')
    print(f'IPv4 {ip_address} is {ip_to_binary(ip_address)}')
elif menu == '2':
    binary_ip = input('Insert the binary number you want to translate into decimal:> ')
    print(f'{binary_ip} translates to {binary_to_ip(binary_ip)}')
elif menu == '3':
    pass
elif menu == '4':
    pass
elif menu == '5':
    ip_cidr = input('Input the IP address and subnet in CIDR notation (ex. 192.168.1.53/24):> ')
    # use calculate_network_info(ip_cidr) function as variable called result to extract data
    result = calculate_network_info(ip_cidr)
    print(f'Network IP is {result['Network IP']}')
    print(f'First usable IP host is {result['First Host IP']}')
    print(f'Last usable IP host is {result['Last Host IP']}')
    print(f'Broadcast address IP is {result['Broadcast IP']}')
    print(f'Next subnet IP is {result['Next Subnet IP']}')
