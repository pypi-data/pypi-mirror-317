# BACKUP REPLACE FILE

#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v2.proprietary_files.section import Section, register_section

class SoterSection(Section):
	name = "Soter"
	interfaces = [
		"vendor.microtrust.hardware.soter",
		"vendor.qti.hardware.soter",
	]
	apps = [
		"SoterService",
	]

register_section(SoterSection)
