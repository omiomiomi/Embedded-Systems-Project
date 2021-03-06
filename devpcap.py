import os
import binascii
import socket
import getopt, sys
import dpkt, pcap
import posix_ipc

PROTO_GOOSE = 0x88B8
PROTO_SV = 0x88BA
PROTO_IP4 = 0x800

messageQueue = "/msg_que"
readPipe = "/tmp/pipe"
mq = posix_ipc.MessageQueue(messageQueue, posix_ipc.O_CREAT)

# 1 = GOOSE, 2 = MMS, 3 = SV
def apply_filter(x):
    filterer = {
        1: 'tcp port 80',				##MMS
        2: 'ether proto 0x88B8',		##GOOSE
        3: 'ether proto 0x88BA'			##SV
    }
    return filterer.get(x, '')

def usage():
	print >>sys.stderr, 'usage: %s [-i device] [pattern]' % sys.argv[0]
	sys.exit(1)

def main():
	opts, args = getopt.getopt(sys.argv[1:], 'i:h') #fetches arguments from command line
	name = None #contains interface that's used for capture
	for o, a in opts:
		if o == '-i': name = a
		else: usage()
<<<<<<< HEAD
	x = 2 #Test for capping MMS
=======
	x = 1 #Test for capping MMS
#	f = open('pcaplog.txt' , 'w')
>>>>>>> kivy
	z = apply_filter(x) #contains the filter string

	try:
		os.mkfifo(readPipe)
	except OSError:
		pass
		
	pc = pcap.pcap(name) #set the interface that is going to be capturing
	#pc.setfilter(' '.join(args))
	pc.setfilter(z) #add filters for the capture interface
	decode = { pcap.DLT_LOOP:dpkt.loopback.Loopback,
			   pcap.DLT_NULL:dpkt.loopback.Loopback,
			   pcap.DLT_EN10MB:dpkt.ethernet.Ethernet }[pc.datalink()]
	try:
		print 'listening on %s: %s' % (pc.name, pc.filter)
		for ts, pkt in pc:
			mq = posix_ipc.MessageQueue(messageQueue)
			#print ts, `decode(pkt)`
			eth = dpkt.ethernet.Ethernet(pkt)

			# Get pipe parameters as string
			# "<proto_id>,<src>,<dst>"
			
			pipe_message = ""
			addr_filter = 0			
#			addr = "192.168.69.150"
			
			# here get pipe parameters
			# 
			
##			print hex(eth.type)
			
			if eth.type == PROTO_IP4:
				ip = eth.data
			
				if addr_filter != 0:
					_addr_filter = socket.inet_aton(addr)

				if ip.p == dpkt.ip.IP_PROTO_ICMP:
					print "PING!!"
			
				elif (ip.p == dpkt.ip.IP_PROTO_TCP) and (addr_filter == 0 or (_addr_filter == ip.dst or _addr_filter == ip.src )):
					tcp = ip.data
					pipe_message = "%s;%s;%s;%d;%d;%d;%s" % (ts, socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst), ip.ttl, tcp.sport, tcp.dport, tcp.data) #format pipe message
					print pipe_message #print pipe message i terminal				
					mq.send(pipe_message) #write captured packages into the pipe
			
			elif eth.type == PROTO_GOOSE:
				print "GOOSE"
				goose = eth.data
				
				if addr_filter != 0:
					_addr_filter = 0
				
			elif eth.type == PROTO_SV:
				sv = eth.data
#			print socket.inet_ntoa(ip.src), '\t', socket.inet_ntoa(ip.dst), '\t', tcp.data.id

##			f.write(pipe_message)
##			f.write('\n')
##			f.close()

	except KeyboardInterrupt:
		nrecv, ndrop, nifdrop = pc.stats()
		print '\n%d packets received by filter' % nrecv
		print '%d packets dropped by kernel' % ndrop
		mq.close()
		mq.unlink()
if __name__ == '__main__':
	main()
