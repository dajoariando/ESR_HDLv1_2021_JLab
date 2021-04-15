#!/usr/bin/python

# author: David Ariando
# description: avalon-memory mapped interface for DE0-Nano-SoC
# date: 2020/09/22

import mmap
import time
from random import randrange
import qsys_addr

# set random values to led
ledval = randrange( 0, 256, 1 )

# BASIC LED test
with open( "/dev/mem", "r+" ) as f:
    # memory-map the file starting with the lightweight axi bus offset and the span of the h2f_lwaxi_master_span
    mem = mmap.mmap( f.fileno(), qsys_addr.lwaxi_span, offset = qsys_addr.lwaxi_ofst )
    
    # seek to the led address
    mem.seek( qsys_addr.lwaxi_led_addr )
    
    # example of writing
    mem.write( ledval.to_bytes( 4, 'little' ) )
    print( "data written to LED = 0x%x" % ledval )
    
    # example of reading
    mem.seek( qsys_addr.lwaxi_led_addr )
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
