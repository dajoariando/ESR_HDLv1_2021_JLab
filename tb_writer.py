#!/usr/bin/python

# author: David Ariando
# description: avalon-memory mapped interface for DE0-Nano-SoC
# date: 2020/09/22

import mmap
import time
from random import randrange
import qsys_addr

# static qsys_addr of the FPGA
h2f_axi_master_span = 0x40000000
h2f_axi_master_ofst = 0xC0000000
h2f_lwaxi_master_span = 0x200000
h2f_lwaxi_master_ofst = 0xff200000

# axi defined qsys_addr
h2f_switch_addr_ofst = 0x4000000

# lwaxi defined qsys_addr
h2f_led_addr = 0x000002c0

# set random values to led
ledval = randrange( 0, 256, 1 )

# BASIC LED test
with open( "/dev/mem", "r+" ) as f:
    # memory-map the file starting with the lightweight axi bus offset and the span of the h2f_lwaxi_master_span
    mem = mmap.mmap( f.fileno(), h2f_lwaxi_master_span, offset = h2f_lwaxi_master_ofst )
    
    # seek to the led address
    mem.seek( h2f_led_addr )
    
    # example of writing
    mem.write( ledval.to_bytes( 4, 'little' ) )
    print( "data written to LED = 0x%x" % ledval )
    
    # example of reading
    mem.seek( h2f_led_addr )
    data = mem.read( 4 )  # read the data in byte format
    dataint = int.from_bytes( data, byteorder = 'little' )
    time.sleep( 0.5 )
    print( "data read from LED = 0x%x" % dataint )
    
	# example of reading
    mem.seek( qsys_addr.lwaxi_bttn_addr )
    data = mem.read( 4 )  # read the data in byte format
    dataint = int.from_bytes( data, byteorder = 'little' )
    time.sleep( 0.5 )
    print( "data button from LED = 0x%x" % dataint )
	
    mem.close()  # close the map
