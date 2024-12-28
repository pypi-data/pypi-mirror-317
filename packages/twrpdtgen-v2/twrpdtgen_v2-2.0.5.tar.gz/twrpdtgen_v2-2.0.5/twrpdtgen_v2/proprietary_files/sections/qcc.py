# BACKUP REPLACE FILE

#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v2.proprietary_files.section import Section, register_section

class QccSection(Section):
	name = "QCC"
	interfaces = [
		"vendor.qti.hardware.qccsyshal",
		"vendor.qti.hardware.qccvndhal",
		"vendor.qti.qccvndhal_aidl",
	]
	binaries = [
		"qcc-vendor",
	]

register_section(QccSection)
