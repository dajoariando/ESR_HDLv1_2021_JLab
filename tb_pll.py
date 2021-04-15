#!/usr/bin/python

# author: David Ariando
# description: PLL frequency, phase, and duty-cycle programmer 
# date: 2020/09/22

import mmap
from array import array

# static addresses of the FPGA
h2f_axi_master_span = 0x40000000
h2f_axi_master_ofst = 0xC0000000
h2f_lwaxi_master_span = 0x200000
h2f_lwaxi_master_ofst = 0xff200000

# axi defined addresses
h2f_switch_addr_ofst = 0x4000000

# lwaxi defined addresses
h2f_led_addr = 0x00000000
pll_base_addr = 0x00000100
h2f_cntout_addr = 0x00000010
h2f_cntin_addr = 0x00000020

# pll_register addresses (shifted by 2 due for 32-bit word addressing)
pll_mode_reg = 0x00 << 2
pll_status_reg = 0x01 << 2
pll_start_reg = 0x02 << 2
pll_n_cnt_reg = 0x03 << 2
pll_m_cnt_reg = 0x04 << 2
pll_c_cnt_reg = 0x05 << 2
pll_dps_reg = 0x06 << 2
pll_mfrac_reg = 0x07 << 2
pll_bw_reg = 0x08 << 2
pll_chpump_reg = 0x09 << 2
pll_vcodiv_reg = 0x1C << 2
pll_mif_reg = 0x1F << 2
pll_c_rd_reg = array ( 'i', [  # these registers are already shifted by 2
        0x28,  # address C00
        0x2C,  # address C01
        0x30,  # address C02
        0x34,  # address C03
        0x38,  # address C04
        0x3C,  # address C05
        0x40,  # address C06
        0x44,  # address C07
        0x48,  # address C08
        0x4C,  # address C09
        0x50,  # address C10
        0x54,  # address C11
        0x58,  # address C12
        0x5C,  # address C13
        0x60,  # address C14
        0x64,  # address C15
        0x68,  # address C16
        0x6C  # address C17
        ] )

# set to polling mode
with open( "/dev/mem", "r+" ) as f:    
    # memory-map the file, size 0 means whole file
    mem = mmap.mmap( f.fileno(), h2f_lwaxi_master_span, offset = h2f_lwaxi_master_ofst )
        
    # set to polling mode
    val = 1
    mem.seek( pll_base_addr + pll_mode_reg )
    mem.write( val.to_bytes( 1, 'little' ) )
    
    mem.close()  # close the map


# compute the pll param, conversion from frequency and duty cycle input to register values
def compute_pll_param ( freq, duty_cycle ):
    
    # set M
    m_high = 4
    m_low = 4
    m_bypass = 0
    m_odd = 0
    
    # set N
    n_high = 1
    n_low = 1
    n_bypass = 1
    n_odd = 0
    
    # set C
    c_high = 100
    c_low = 100
    c_bypass = 0
    c_odd = 0
    
    # set MFRAC
    m_frac = 1<<31
    
    return m_high, m_low, m_bypass, m_odd, n_high, n_low, n_bypass, n_odd, c_high, c_low, c_bypass, c_odd, m_frac

        
# set pll parameters for M, N, C, and MFRAC registers
def set_pll( freq, dtcl, c_select ):
    print( "Frequency is set to freq" )
    # pll reconfiguration
    with open( "/dev/mem", "r+" ) as f:
        # memory-map the file, size 0 means whole file
        mem = mmap.mmap( f.fileno(), h2f_lwaxi_master_span, offset = h2f_lwaxi_master_ofst )
        
        # compute pll parameters
        m_high, m_low, m_bypass, m_odd, n_high, n_low, n_bypass, n_odd, c_high, c_low, c_bypass, c_odd, m_frac = compute_pll_param ( freq, dtcl )
        
        # set M registers
        val = ( ( m_high & 0xFF ) << 8 ) | ( m_low & 0xFF ) | ( ( m_bypass & 0x01 ) << 16 ) | ( ( m_odd & 0x01 ) << 17 )
        mem.seek( pll_base_addr + pll_m_cnt_reg )
        mem.write( val.to_bytes( 4, 'little' ) )
        
        # set N registers
        val = ( ( n_high & 0xFF ) << 8 ) | ( n_low & 0xFF ) | ( ( n_bypass & 0x01 ) << 16 ) | ( ( n_odd & 0x01 ) << 17 )
        mem.seek( pll_base_addr + pll_n_cnt_reg )
        mem.write( val.to_bytes( 4, 'little' ) )
        
        # set C registers
        val = ( ( c_high & 0xFF ) << 8 ) | ( c_low & 0xFF ) | ( ( c_bypass & 0x01 ) << 16 ) | ( ( c_odd & 0x01 ) << 17 ) | ( ( c_select & 0x1F ) << 18 )
        mem.seek( pll_base_addr + pll_c_cnt_reg )
        mem.write( val.to_bytes( 4, 'little' ) )
        
        # set MFRAC registers
        mem.seek( pll_base_addr + pll_mfrac_reg )
        mem.write( m_frac.to_bytes( 4, 'little' ) )
        
        mem.close()  # close the map


# starting PLL reconfig and wait until reconfig is done
def submit_pll_reconfig ():
    with open( "/dev/mem", "r+" ) as f:
        # memory-map the file, size 0 means whole file
        mem = mmap.mmap( f.fileno(), h2f_lwaxi_master_span, offset = h2f_lwaxi_master_ofst )
    
        # start reconfig
        val = 1
        mem.seek( pll_base_addr + pll_start_reg )
        mem.write( val.to_bytes( 4, 'little' ) )
        
        # read the status register
        mem.seek( pll_base_addr + pll_status_reg )  # needed to make mm ready
        data = mem.read( 4 )
        dataint = int.from_bytes( data, byteorder = 'little' )
        while dataint == 0:
            print( "submit_pll" )
            mem.seek( pll_base_addr + pll_status_reg )  # needed to make mm ready
            data = mem.read( 4 )
            dataint = int.from_bytes( data, byteorder = 'little' )
        
        mem.close()  # close the map


# reset the PLL and wait until it's locked, it's recommended to be done after any reconfiguration
# resetting the PLL will erase the phase configuration
def reset_pll():
    with open( "/dev/mem", "r+" ) as f:
        # memory-map the file, size 0 means whole file
        mem = mmap.mmap( f.fileno(), h2f_lwaxi_master_span, offset = h2f_lwaxi_master_ofst )
        
        # reset the pll
        val = 0x01
        mem.seek( h2f_cntout_addr )
        mem.write( val.to_bytes( 1, 'little' ) )
        # reset the pll
        val = 0x0
        mem.seek( h2f_cntout_addr )
        mem.write( val.to_bytes( 1, 'little' ) )
        
        # wait until locked
        mem.seek( h2f_cntin_addr )  # needed to make mm ready
        data = mem.read( 4 )
        dataint = int.from_bytes( data, byteorder = 'little' )
        while dataint == 0:
            print( "setpll_cntin" )
            mem.seek( h2f_cntin_addr )  # needed to make mm ready
            data = mem.read( 4 )
            dataint = int.from_bytes( data, byteorder = 'little' )
        
        mem.close()  # close the map

 
# change the phase of the PLL. Do this after reset, as reset erases phase that was written
def set_dps( cnt_sel, phase ):
    with open( "/dev/mem", "r+" ) as f:
        # memory-map the file, size 0 means whole file
        mem = mmap.mmap( f.fileno(), h2f_lwaxi_master_span, offset = h2f_lwaxi_master_ofst )
        
        # read the c counter value, as phase is referenced to VCO, not output clock
        mem.seek( pll_base_addr + pll_c_rd_reg[cnt_sel] ) 
        # print( pll_c_rd_reg[cnt_sel] )
        data = mem.read( 4 )
        dataint = int.from_bytes( data, byteorder = 'little' )
        c_counter = ( dataint & 0xFF ) + ( ( dataint >> 8 ) & 0xFF )
        
        print( c_counter )
        
        dps = c_counter * phase * 8 / 360  # convert input values (degrees) to numbers
        dps_direction = 1
        
        print( int( dps ) )
        
        val = ( ( dps_direction & 0x01 ) << 21 ) | ( ( cnt_sel & 0x1F ) << 16 ) | ( int( dps ) & 0xFFFF )
        mem.seek( pll_base_addr + pll_dps_reg )
        mem.write( val.to_bytes( 4, 'little' ) )
        
        mem.close()  # close the map


# main program
set_pll( 4, 50, 0 )
set_pll( 3, 50, 1 )
submit_pll_reconfig ()
reset_pll()
set_dps( 0, 0 )
submit_pll_reconfig ()
set_dps( 1, 290 )
submit_pll_reconfig ()

