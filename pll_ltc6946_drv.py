#!/usr/bin/python

# serial port registers
h00 = 0x00      # read only register
h00_UNLOCK  = 5 # out of lock condition
h00_ALCHI   = 4 # ACL too high flag (resonator amplitude too high)  
h00_ALCLO   = 3 # ACL too low flag (resonator amplitude too low)    
h00_LOCK    = 2 # lock condition
h00_THI     = 1 # high voltage clamp flag
h00_TLO     = 0 # low voltage clamp flag

h01 = 0x01           
h01_default = 0x04 
h01_x       = 0     # bit-wise mask for the STAT output of h00 
h01_x_msk   = 0x3F

h02 = 0x02
h02_default = 0x0E
h02_PDALL   = 7     # full chip power down. active high. default: 0
h02_PDPLL   = 6     # powers down REF, REFO, R_DIV, PFD, CPUMP, N_DIV. default: 0
h02_PDVCO   = 5     # powers down VCO, N_DIV. default: 0
h02_PDOUT   = 4     # powers down O_DIV, RF output buffer. default: 0
h02_PDREF0  = 3     # powers down REFO. default: 1
h02_MTCAL   = 2     # mutes output during calibration. default: 1
h02_OMUTE   = 1     # mutes RF output. default: 1
h02_POR     = 0     # for power-on reset. default: 0

h03 = 0x03
h03_default     = 0x30
h03_BD          = 4     # B divider, used to clock digital calibration circuitry. default: 0x03
h03_BD_msk      = 0x0F  
h03_RD_MSB      = 0     # R divider 2-bit MSB. default for only the MSB: 0x00
h03_RD_MSB_msk  = 0x03  

h04 = 0x04
h04_default     = 0x01
h04_RD_LSB      = 0     # R divider 8-bit LSB. default for only the LSB: 0x01
h04_RD_LSB_msk  = 0xFF

h05 = 0x05
h05_default     = 0x00
h05_ND_MSB      = 0     # N divider 8-bit MSB. default for only the MSB: 0x00
h05_ND_MSB_msk  = 0xFF

h06 = 0x06
h06_default     = 0xFA
h06_ND_LSB      = 0     # N divider 8-bit LSB. default for only the LSB: 0xFA
h06_ND_LSB_msk  = 0xFF

h07 = 0x07
h07_default     = 0x21
h07_ALCEN       = 7     # always enable ALC (override). default: 1
h07_ALCMON      = 6     # enable ALC monitor for status flags only. default: 0
h07_ALCCAL      = 5     # auto enable ALC during CAL operation. default: 1
h07_ALCULOK     = 4     # enable ALC when PLL unlocked. default: 0
h07_CAL         = 1     # start VCO calibration (auto clears). default: 0
h07_LKEN        = 0     # PLL lock indicator enable. default: 1

h08 = 0x08
h08_default     = 0xF9
h08_BST         = 8     # REF buffer boost current. default: 1
h08_FILT        = 5     # REF input buffer filter. default: 0x03
h08_FILT_msk    = 0x03
h08_RFO         = 3     # RF output power. default: 0x03
h08_RFO_msk     = 0x03
h08_OD          = 0     # Output divider value. default: 1
h08_OD_msk      = 0x07

h09 = 0x09
h09_default     = 0x9B
h09_LKWIN       = 6     # PLL lock indicator window. default: 0x02
h09_LKWIN_msk   = 0x03
h09_LKCT        = 4     # PLL lock cycle count. default: 0x01
h09_LKCT_msk    = 0x03
h09_CP          = 0     # Charge pump output current. default: 0x0B
h09_CP_msk      = 0x0F

h0A = 0x0A
h0A_default     = 0xE4
h0A_CPCHI       = 7     # Charge pump enable hi voltage output clamp. default: 1
h0A_CPCLO       = 6     # Charge pump enable low voltage output clamp. default: 1
h0A_CPMID       = 5     # Charge pump bias to mid-rail. default: 1
h0A_CPINV       = 4     # Charge pump invert phase. default: 1
h0A_CPWIDE      = 3     # Charge pump extend pulse width. default: 0
h0A_CPRST       = 2     # Charge pump three-state. default: 1
h0A_CPUP        = 1     # Charge pump pump up only. default: 0
h0A_CPDN        = 0     # Charge pump pump down only. default: 0

h0B = 0x0B              # read only register
h0B_REV         = 5     # rev code
h0B_REV_msk     = 0x07
h0B_PART        = 0     # part code. 0x04 for LTC6946-4
h0B_PART_msk    = 0x1F




