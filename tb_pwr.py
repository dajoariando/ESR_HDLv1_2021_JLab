#!/usr/bin/python

# author: David Ariando
# description: avalon-memory mapped interface for DE0-Nano-SoC
# date: 2020/09/22

import qsys_ctrl
import time

qsys_ctrl.assert_cnt(qsys_ctrl.EN_PWR_msk|qsys_ctrl.EN_PWR2_msk)
time.sleep( 5 )
qsys_ctrl.deassert_cnt(qsys_ctrl.EN_PWR_msk|qsys_ctrl.EN_PWR2_msk)
