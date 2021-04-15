#!/usr/bin/python

from drv_pll_ltc6946 import rd_chip
import qsys_ctrl
import time

qsys_ctrl.assert_cnt(qsys_ctrl.EN_PWR_msk|qsys_ctrl.EN_PWR2_msk)
time.sleep( 2 )

rev,part = rd_chip()
print(rev)
print(part)

time.sleep( 2 )
qsys_ctrl.deassert_cnt(qsys_ctrl.EN_PWR_msk|qsys_ctrl.EN_PWR2_msk)
