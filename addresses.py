#!/usr/bin/python

# static addresses of the FPGA
h2f_axi_master_span = 0x40000000
h2f_axi_master_ofst = 0xC0000000
h2f_lwaxi_master_span = 0x200000
h2f_lwaxi_master_ofst = 0xff200000

# axi defined addresses
h2f_switch_addr_ofst = 0x4000000

# lwaxi defined addresses
lwaxi_led_addr              = 0x02c0
lwaxi_sw_addr               = 0x02d0
lwaxi_bttn_addr             = 0x02e0
lwaxi_fifo_A_out_addr       = 0x02f8
lwaxi_fifo_A_out_csr_addr   = 0x0240
lwaxi_fifo_A_in_csr_addr    = 0x0280
lwaxi_fifo_B_out_addr       = 0x02f0
lwaxi_fifo_B_out_csr_addr   = 0x0220
lwaxi_fifo_B_in_csr_addr    = 0x0260
lwaxi_plldds_spi_addr       = 0x0200
lwaxi_gnrl_cntout_addr      = 0x02b0
lwaxi_gnrl_cntin_addr       = 0x02a0
lwaxi_pulse_pll_addr        = 0x0000