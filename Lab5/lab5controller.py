# Lab 5 controller skeleton 
#
# Based on of_tutorial by James McCauley
from pox.core import core
import pox.openflow.libopenflow_01 as of
import time 

log = core.getLogger()
 
class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection
    # This binds our PacketIn event listener
    connection.addListeners(self)
    #Dictionary to store the timespack of icmp messages last seen
    self.icmp_last_seen = {}

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet
    
    def accept():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 45
      msg.hard_timeout = 600
      msg.buffer_id = packet_in.buffer_id 
      msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL)) 
      msg.data = packet_in      
      self.connection.send(msg)
      log.info("Packet Accepted - Flow Table Installed on Switches")

    def drop():
      msg = of.ofp_packet_out()
      msg.buffer_id = packet_in.buffer_id
      msg.data = packet_in
      msg.in_port = packet_in.in_port
      self.connection.send(msg)
      log.info("Packet Dropped")

    ip = packet.find('ipv4')
    arp = packet.find('arp') 
    icmp = packet.find('icmp')
    tcp = packet.find('tcp')
    udp = packet.find('udp')

     #we ony allow general connectivity within the network"
    if icmp is not None:
      ip_src = ip.srcip
      ip_dst = ip.dstip
    #implement rate limit to prevent a high number of icmp packets
      current_time = time.time()
      last_seen = self.icmp_last_seen.get(ip_src, 0)
      if current_time - last_seen < 0.1:
        drop()
        log.info(f"ICMP Packet rate exceeded from {ip_src},packed dropped")
        return 
      else: 
        self.icmp_last_seen[ip_src] = current_time
      if( 
       #Server -> Laptop
      (ip_src == '10.1.1.1' and ip_dst == '10.1.1.2') or
      (ip_src == '10.1.1.2' and ip_dst == '10.1.1.1') or
      
      #Server -> Lights 
      (ip_src == '10.1.2.1' and ip_dst == '10.1.1.1') or
      (ip_src == '10.1.1.1' and ip_dst == '10.1.2.1') or 
      
      #Server -> Fridge
      (ip_src == '10.1.1.1' and ip_dst == '10.1.2.2') or
      (ip_src == '10.1.2.2' and ip_dst == '10.1.1.1') or
      
      # Laptop -> Lights 
      (ip_src == '10.1.1.2' and ip_dst == '10.1.2.1') or
      (ip_src == '10.1.2.1' and ip_dst == '10.1.1.2') or 
      
      #Laptop->Fridge 
      (ip_src == '10.1.1.2' and ip_dst == '10.1.2.2') or
      (ip_src == '10.1.2.2' and ip_dst == '10.1.1.2') or
      #Lights-> Fridge 
      (ip_src == '10.1.2.1' and ip_dst == '10.1.2.2') or 
      (ip_src == '10.1.2.2' and ip_dst == '10.1.2.1')) :
        accept()
        return

    if arp is not None:
      accept()
      return 
 
    if tcp is not None:
      ip_src = ip.srcip
      ip_dst = ip.dstip
        
      if((ip_src == '10.1.1.2' and ip_dst == '10.1.1.1') or
      (ip_src == '10.1.1.1' and ip_dst == '10.1.1.2') or
      (ip_src == '10.1.1.2' and ip_dst == '10.1.2.1') or
      (ip_src == '10.1.2.1' and ip_dst == '10.1.1.2' )) :
          accept()
          return
      
    if udp is not None: 
      ip_src = ip.srcip
      ip_dst = ip.dstip
        
      if ((ip_src == '10.1.1.2' and ip_dst == '10.1.2.2') or
      (ip_src == '10.1.2.2' and ip_dst == '10.1.1.2') or
      (ip_src == '10.1.1.2' and ip_dst == '10.1.1.1')) :
        accept()
        return

      #if not matches, drop
    drop()

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the components
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
