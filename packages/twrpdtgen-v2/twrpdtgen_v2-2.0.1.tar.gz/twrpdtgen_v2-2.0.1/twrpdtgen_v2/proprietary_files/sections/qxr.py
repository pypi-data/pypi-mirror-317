# BACKUP REPLACE FILE

#
# Copyright (C) 2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v2.proprietary_files.section import Section, register_section

class QxrSection(Section):
	name = "QXR"
	interfaces = [
		"vendor.qti.hardware.qxr",
	]

register_section(QxrSection)
