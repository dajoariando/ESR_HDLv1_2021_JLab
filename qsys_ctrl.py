import mmap
from random import randrange
import qsys_addr
import qsys_ctrl

EN_PA_msk = 1<<2
EN_PWR2_msk = 1<<1
EN_PWR_msk = 1<<0

def rd_cnt():
	with open( "/dev/mem", "r+" ) as f:
		# memory-map the file starting with the lightweight axi bus offset and the span of the h2f_lwaxi_master_span
		mem = mmap.mmap( f.fileno(), qsys_addr.lwaxi_span, offset = qsys_addr.lwaxi_ofst )
		
		# turn on the power
		mem.seek( qsys_addr.lwaxi_gnrl_cntout_addr )
		data = mem.read( 4 )  # read the data in byte format
		dataint = int.from_bytes( data, byteorder = 'little' )

		mem.close()  # close the map
	return dataint

def wr_cnt( val ):
	with open( "/dev/mem", "r+" ) as f:
		# memory-map the file starting with the lightweight axi bus offset and the span of the h2f_lwaxi_master_span
		mem = mmap.mmap( f.fileno(), qsys_addr.lwaxi_span, offset = qsys_addr.lwaxi_ofst )
		
		# turn on the power
		mem.seek( qsys_addr.lwaxi_gnrl_cntout_addr )
		mem.write( val.to_bytes( 4, 'little' ) )

		mem.close()  # close the map
		
def assert_cnt(val):
	curr = rd_cnt() # get the current cnt value
	wr_cnt(curr | val)
	
def deassert_cnt(val):
	curr = rd_cnt() # get the current cnt value
	wr_cnt(curr & (~val))