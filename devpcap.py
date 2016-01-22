import binascii
import socket
import getopt, sys
import dpkt, pcap

#PROTO_GOOSE = 0x88BB
#PROTO_SV = 0x88BA
#PROTO_IP4 = 0x8000

# 1 = GOOSE, 2 = MMS, 3 = SV
def apply_filter(x):
    filterer = {
        1: 'ether proto 0x88B8',
        2: 'tcp port 102',
        3: 'ether proto 0x88BA'
    }
    return filterer.get(x, '')

def usage():
	print >>sys.stderr, 'usage: %s [-i device] [pattern]' % sys.argv[0]
	sys.exit(1)

def main():
	opts, args = getopt.getopt(sys.argv[1:], 'i:h')
	name = None
	for o, a in opts:
		if o == '-i': name = a
		else: usage()
	x = 2 #Test for capping MMS
	f = open('pcaplog.txt' , 'w')
	z = apply_filter(x) #contains the filter string
	
	#f = open('pcaplog.txt' , 'w')
		
	pc = pcap.pcap(name)
	#pc.setfilter(' '.join(args))
	pc.setfilter(z)
	decode = { pcap.DLT_LOOP:dpkt.loopback.Loopback,
			   pcap.DLT_NULL:dpkt.loopback.Loopback,
			   pcap.DLT_EN10MB:dpkt.ethernet.Ethernet }[pc.datalink()]
	try:
		print 'listening on %s: %s' % (pc.name, pc.filter)
		for ts, pkt in pc:
			print ts, `decode(pkt)`
			eth = dpkt.ethernet.Ethernet(pkt)

			addr_filter = 0			
			
			# here get pipe parameters
			# 
			
			if eth.type == PROTO_IP4:
				ip = eth.data
			
				if addr_filter != 0:
					_addr_filter = socket.inet_aton(ip_filter)

				if ip.p == dpkt.ip.IP_PROTO_ICMP:
					print "PING!!"
			
				elif (ip.p == dpkt.ip.IP_PROTO_TCP) and (addr_filter == 0 or (_addr_filter == ip.dst or _addr_filter == ip.src )):
					tcp = ip.data
					pipe_message = "%s;%s;%d;%d;%d;%d" % (socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst), ip.ttl, tcp.sport, tcp.dport, tcp.data.id)
					print pipe_message				
			
			elif eth.type == PROTO_GOOSE:
				goose = eth.data
				
				if addr_filter != 0:
					_addr_filter = 0
				
			elif eth.type == PROTO_SV:
				sv = eth.data
				
			print socket.inet_ntoa(ip.src), '\t', socket.inet_ntoa(ip.dst), '\t', tcp.data.id

			#packet = decode(pkt)
			#s = str(packet)
			#f.write(str(ts))
			#f.write('\t')
			#f.write(s)
			#f.write('\n')
	except KeyboardInterrupt:
		nrecv, ndrop, nifdrop = pc.stats()
		print '\n%d packets received by filter' % nrecv
		print '%d packets dropped by kernel' % ndrop

if __name__ == '__main__':
	main()
