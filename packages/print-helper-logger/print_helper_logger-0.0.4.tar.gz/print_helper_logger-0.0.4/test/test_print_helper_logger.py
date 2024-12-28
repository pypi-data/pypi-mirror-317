#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# /**
#  * @file test_print_helper_logger.py
#  * @author Oscar Gomez Fuente <oscargomezf@gmail.com>
#  * @modified Oscar Gomez Fuente <oscargomezf@gmail.com>
#  * @date 2024-12-27 23:21:18 
#  * @version b28bd1e
#  * @section DESCRIPTION
#  *     Script to test print_helper_logger package
#  *     Install package: pip install print_helper_logger
#  */
# -----------------------------------------------------------------------------

import os
from print_helper_logger import Print_Helper, Severity_Level

def print_messages(my_print_helper):
	#my_print_helper.printh('<dbg> This is a DEBUG message\n')
	my_print_helper.print_dbg('This is a DEBUG message\n')
	#my_print_helper.printh('<inf> This is a INFO message\n')
	my_print_helper.print_inf('This is a INFO message\n')
	#my_print_helper.printh('<wrn> This is a WARNING message\n')
	my_print_helper.print_wrn('This is a WARNING message\n')
	#my_print_helper.printh('<err> This is a ERROR message\n')
	my_print_helper.print_err('This is a ERROR message\n')
	#my_print_helper.printh('<crt> This is a CRITICAL message\n')
	my_print_helper.print_crt('This is a CRITICAL message\n')

if __name__ == "__main__":
	# /** Test DEBUG messages with timestamp and colors */
	print('Testing DEBUG messages with timestamp and colors')
	ph = Print_Helper(Severity_Level.DEBUG, True, True, None)
	print_messages(ph)

	# /** Test INFO messages with timestamp and colors */
	print('Testing INFO messages with timestamp and colors')
	ph = Print_Helper(Severity_Level.INFO, True, True, None)
	print_messages(ph)

	# /** Test WARNING messages with timestamp and colors */
	print('Testing WARNING messages with timestamp and colors')
	ph = Print_Helper(Severity_Level.WARNING, True, True, None)
	print_messages(ph)

	# /** Test ERROR messages with timestamp and colors */
	print('Testing ERROR messages with timestamp and colors')
	ph = Print_Helper(Severity_Level.ERROR, True, True, None)
	print_messages(ph)

	# /** Test CRITICAL messages with timestamp and colors */
	print('Testing CRITICAL messages with timestamp and colors')
	ph = Print_Helper(Severity_Level.CRITICAL, True, True, None)
	print_messages(ph)

	# /** Test DEBUG messages without timestamp and colors */
	print('Testing DEBUG messages without timestamp and colors')
	ph = Print_Helper(Severity_Level.DEBUG, False, False, None)
	print_messages(ph)

	# /** Test DEBUG messages with timestamp and colors and logger */
	filename_logger = f'{os.path.dirname(os.path.abspath(__file__))}\\log_test.log'
	print(f'Testing DEBUG messages with timestamp and colors and logger: {filename_logger}')
	ph = Print_Helper(Severity_Level.DEBUG, True, True, filename_logger)
	print_messages(ph)
