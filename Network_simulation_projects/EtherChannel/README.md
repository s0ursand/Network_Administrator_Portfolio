# EtherChannel Project

## Overview

This project includes pre-configured end host and SVI IP addresses, making it easier to focus on the EtherChannel setup and routing configurations.

## Objectives

1. **Configure Layer 2 EtherChannel between ASW1 and DSW1 using LACP**: Set up as a trunk.
   
2. **Configure Layer 2 EtherChannel between ASW2 and DSW2 using PAgP**: Set up as a trunk.

3. **Configure Layer 3 EtherChannel between DSW1 and DSW2**: Utilize static EtherChannel.

4. **Configure routes**: Ensure PCs can reach SRV1.

5. **Identify default EtherChannel load-balancing methods**: Determine the default method used on each switch.

6. **Configure load-balancing**: Adjust the switches to load-balance based on source and destination IP addresses.

![Network_Diagram](Images/Network_Diagram.png)

## Getting Started

### Configuration Steps

1. **Layer 2 EtherChannel Configuration**:

   - **ASW1 to DSW1**:
	First, with the command **show spanning-tree** we can see that while G0/1 is the root port <br>
	G0/2 is blocked by the STP. <br>

![ASW1 spanning-tree](Images/ASW1_spanning-tree_1.png)

     - Use LACP to configure the EtherChannel.
	Enter the int mode and create the channel-port for the EtherChannel connection with the command <br>
	**channel-group 1 mode active** <br>
	where **active** attemps to form an active LACP connection

![ASW1 channel-group](Images/ASW1_channel-group_1.png)

     - Set the EtherChannel interface as a trunk.
	Enter the newly formed channel-group (po1) and by using the command <br>
	**switchport mode trunk** <br>
	a new trunk connection is enstablished. Because DSW1 isn't configured yet this won't show up in <br>
	**show interfaces trunk**, however we can confirm it by looking at the running-config. <br>

![ASW1 trunk](Images/ASW1_trunk.png)

   - **DSW1 to ASW1**:
	The configuration is the same as ASW1:

![DSW1 trunk](Images/DSW1_trunk.png)

	Confirm the connection is active with **do show etherchannel summary** <br>
	The flags SU confirms that the connection is active.

![DSW1 etherchannel summary](Images/DSW1_etherchannel_summary.png)

Going back to ASW1 we can confirm the etherchannel works as a single port by using the **show spanning-tree** <br>
command once again.

![ASW1 spanning tree 2](Images/ASW1_spanning_tree_2.png)

   - **ASW2 to DSW2**:
     - Use PAgP to configure the EtherChannel amd set it as a trunk port.
	The configurations of ASW2 and DSW2 will be almost identical to ASW1 and DSW1, the only difference is that we <br>
	will use **channel-group 1 mode desirable** instead of **channel-group 1 mode active** <br>

![ASW2 configuration](Images/ASW2_conf.png)

![DSW2 configuration](Images/DSW2_conf.png)

![ASW2 etherchannel summary](Images/ASW2_etherchannel_summary.png)

2. **Layer 3 EtherChannel Configuration**:
   - Configure static EtherChannel between DSW1 and DSW2.
	Enter the interface range g1/0/3 - 4 from DSW1. First thing we make these routed ports <br>
	with the command **no switchport**. Next we create a static etherchannel with the command 
	**channel-group 2 mode on** (channel-group 1 is already in use). Lastly we assign an ip address to p02:
	
	**ip add 10.0.0.2 255.255.255.252**

![DSW1 static conf](Images/DSW1_static_conf.png)

	Repeat the process on DSW2 (assign IP 10.0.0.1 255.255.255.252)

![DSW2 static conf](Images/DSW2_static_conf.png)

	Confirm with **do show etherchannel summary** (RU means layer 3 and active)

![DSW1 eth sum static](Images/DSW1_etherchannel_summary_static.png)

3. **Routing Configuration**:
   - Implement static routes to enable communication from PCs to SRV1.
	First step is to enable IP routing on both DSW.
	From config mode use the command **ip routing**. 
	Next we must configure a static route on DSW1 to SRV1's subnet with DSW2 as next-hop: 
	**ip route 172.16.2.0 255.255.255.0 10.0.0.1** <br>
	confirm with **do show ip route**

![DSW1 static route](Images/DSW1_static_route.png)

	Then we must configure a static route on DSW2 to PC1's network with DSW1 as next-hop

![DSW2 static route](Images/DSW2_static_route.png)

	Test connectivity sending a ping from PC1 to SRV1

![PC1 ping SRV1](Images/PC1_ping_SRV1.png)

4. **Load-Balancing Configuration**:
   - Identify and configure the load-balancing method on each switch.
	We can check the load balancing method with the following command <br>
	**do show etherchannel load-balance** <br>
	the current default is source MAC Address.

![ASW1 load-balance](Images/ASW1_load-balance.png)

   - Set the switches to load-balance based on source and destination IP addresses.
	To change the current load-balancing method use the command **port-channel load-balance src-dst-ip** <br>
	Confirm with **do sh etherchannel load-balance**

![ASW1 load-balance updated](Images/ASW1_load-balance_updated.png)

	Repeat the steps for ASW2 and DSW1-DSW2

## Conclusion

In this EtherChannel project, we successfully configured Layer 2 and Layer 3 EtherChannel connections using LACP and PAgP, ensuring efficient communication between switches and end hosts. We also implemented static routing and optimized load balancing based on source and destination IP addresses.
