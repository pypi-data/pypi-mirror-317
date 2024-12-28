# BACKUP REPLACE FILE

#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v2.proprietary_files.section import Section, register_section

class FingerprintSection(Section):
	name = "Fingerprint"
	interfaces = [
		"android.hardware.biometrics.fingerprint",
		"vendor.goodix.hardware.biometrics.fingerprint",
		"vendor.oplus.hardware.biometrics.fingerprint",
		"vendor.qti.hardware.fingerprint",
		"vendor.xiaomi.hardware.fingerprintextension",
	]
	hardware_modules = [
		"fingerprint",
		"gf_fingerprint",
	]
	binaries = [
		"qfp-daemon",
	]
	properties_prefixes = {
		"persist.vendor.qfp": True,
	}

register_section(FingerprintSection)
