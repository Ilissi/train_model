#!/usr/bin/env python3
import sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog = '{}\n{}'.format(
	'example : anonymizepcap.py original.pcap anonymized.pcap',
	'example : anonymizepcap.py -v -vb 10000 -m /absolute/path/to/modules/folder original.pcap anonymized.pcap'
))
parser.add_argument('srcfile', help = 'input pcap file')
parser.add_argument('dstfile', help = 'output pcap file')
parser.add_argument('-m', '--modules', help = 'absolute path to the modules folder\nuse this option if the script can not import the modules', metavar = 'path', default = None)
parser.add_argument('-v', '--verbose', help = 'print the progress to stdout', action = 'store_true', default=False)
parser.add_argument('-vb', '--vbuffer', help = 'print progress every n packets.\nShould be used with -v option.\nDefault 5000', type=int, metavar ='n', default=5000)
parser.add_argument('-s', '--split', help = 'split traces for a max length of time', type=int, metavar ='time', default=None)
args = parser.parse_args()


from scapy.all import wrpcap, raw
from scapy.utils import RawPcapReader, RawPcapWriter
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP
if args.modules is not None : sys.path.insert(0, args.modules)
try:
	from anonymizer import IpAnonymizer
except : sys.exit('Can not import required modules. Try using -m option')

pkt_count = 0
verbose_count = 0
start = None
file_count = 0
dstfile = '{}.{}'.format(args.dstfile, file_count) if args.split is not None else args.dstfile

reader = RawPcapReader(args.srcfile)
writer = RawPcapWriter(dstfile, append=True, linktype=reader.linktype)
anonym = IpAnonymizer(anonimize_private = False)

for (pkt_data, pkt_metadata,) in reader:
	ether_pkt = Ether(pkt_data)

	#FILTER NON RELEVANT PACKETS
	if 'type' not in ether_pkt.fields: continue
	if ether_pkt.type != 0x0800: continue

	#ANONIMIZE
	ip_pkt = ether_pkt[IP]
	ip_pkt.src = anonym.anonimize(ip_pkt.src)
	ip_pkt.dst = anonym.anonimize(ip_pkt.dst)
	ether_pkt[IP] = ip_pkt

	#ROTATE OUTPUT FILE IF -s OPTION WAS USED
	if args.split is not None:
		if start is None: start = pkt_metadata.sec
		else :
			if pkt_metadata.sec - start > args.split:
				file_count += 1
				if args.verbose: print('Time limit ({}) reached. File at {}'.format(args.split, dstfile))
				dstfile = '{}.{}'.format(args.dstfile, file_count)
				writer = RawPcapWriter(dstfile, append=True, linktype=reader.linktype)
				start = pkt_metadata.sec

	#REFRESH VERBOSE VARIABLES AND PRINT IF REQUIRED
	pkt_count += 1
	verbose_count += 1
	if args.verbose and verbose_count >= args.vbuffer:
		print('Packets parsed : {}'.format(pkt_count), end = '\r')
		verbose_count = 0

	#WRITE TO OUTPUT FILE
	#writer.write(raw(ether_pkt), sec = pkt_metadata.sec, usec = pkt_metadata.usec)
	if not writer.header_present: writer._write_header(raw(ether_pkt))
	writer._write_packet(raw(ether_pkt), sec = pkt_metadata.sec, usec = pkt_metadata.usec)

if args.verbose:
	if args.split is not None: print('File anonymized, new pcap in {}'.format(args.dstfile))
	else : print('EOF reached. File at {}'.format(dstfile))
