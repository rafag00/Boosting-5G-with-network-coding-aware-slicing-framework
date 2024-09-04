#!/usr/bin/env python

import requests
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def basicTopo():

  #Just a simple topology with 4 hosts and 4 switches

  net = Mininet(switch=OVSKernelSwitch, link=TCLink, autoSetMacs=True)

  info('*** Adding controller ***\n')
  net.addController(RemoteController( 'c0', ip='172.17.0.3', port=6653))

  info('*** Adding hosts ***\n')
  h1 = net.addHost( 'h1')
  h2 = net.addHost( 'h2')

  info('*** Adding switch ***\n')
  s1 = net.addSwitch('s1', protocols='OpenFlow14')
  s2 = net.addSwitch('s2', protocols='OpenFlow14')
  s3 = net.addSwitch('s3', protocols='OpenFlow14')  

  info('*** Creating links ***\n')
  net.addLink(h1,s1,port1=0,port2=1)
  net.addLink(h2,s3,port1=0,port2=2)
  net.addLink(s1,s2,port1=3,port2=1, bw=8, delay='25ms', loss=5, jitter='15ms')
  net.addLink(s1,s3,port1=2,port2=1, bw=50, loss=0.00001)
  net.addLink(s2,s3,port1=2,port2=3, bw=8, delay='25ms', loss=5, jitter='15ms')

  return net

if __name__ == '__main__':
  setLogLevel( 'info' )
  
  print("This is a BE topology.")
      
  net = basicTopo()
  
  info('*** Starting network ***\n')
  net.start()
  
  info('*** Testing connectivity ***\n')
  net.pingAll()
  
  input("Press Enter to continue... Be sure you snapshoted the network!!")
    
  try:
    data = [{"sw_id_src": "of:0000000000000001","sw_id_dst": "of:0000000000000002","port_numb_src": 3,"port_numb_dst": 1,"bandwith": 8000000,
             "latency": 25,"jitter": 15,"loss_prob": 5,"energy_consumption": 138}
            ,{"sw_id_src": "of:0000000000000002","sw_id_dst": "of:0000000000000001","port_numb_src": 1,"port_numb_dst": 3,"bandwith": 8000000,
              "latency": 25,"jitter": 15,"loss_prob": 5,"energy_consumption": 138}
            ,{"sw_id_src": "of:0000000000000001","sw_id_dst": "of:0000000000000003","port_numb_src": 2,"port_numb_dst": 1,"bandwith": 50000000,
              "latency": 1,"jitter": 1,"loss_prob": 0.00001,"energy_consumption": 658}
            ,{"sw_id_src": "of:0000000000000003","sw_id_dst": "of:0000000000000001","port_numb_src": 1,"port_numb_dst": 2,"bandwith": 50000000,
              "latency": 1,"jitter": 1,"loss_prob": 0.00001,"energy_consumption": 658}
            ,{"sw_id_src": "of:0000000000000002","sw_id_dst": "of:0000000000000003","port_numb_src": 2,"port_numb_dst": 3,"bandwith": 8000000,
              "latency": 25,"jitter": 15,"loss_prob": 5,"energy_consumption": 138}
            ,{"sw_id_src": "of:0000000000000003","sw_id_dst": "of:0000000000000002","port_numb_src": 3,"port_numb_dst": 2,"bandwith": 8000000,
              "latency": 25,"jitter": 15,"loss_prob": 5,"energy_consumption": 138},]
    
    response = requests.post('http://172.17.0.4:8080/links', json=data)

    # Check the response status code
    if response.status_code == 200:
        info('API request successful!\n')
    else:
        info(f'API request failed with status code: {response.status_code} and response: {response.text}\n')
  except Exception as e:
    info(f'API request failed with error: {e}\n')

  #net.get('h1').cmd('python3 scapyScripth1.py')
  #net.get('h2').cmd('python3 scapyScripth2.py')

  info('*** Running CLI ***\n')
  CLI( net )

  info('*** Stopping network ***\n')
  net.stop()
