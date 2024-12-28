#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# /**
#  * @file print_helper_logger.py
#  * @author Oscar Gomez Fuente <oscargomezf@gmail.com>
#  * @modified Oscar Gomez Fuente <oscargomezf@gmail.com>
#  * @date 2024-12-27 23:21:18 
#  * @version b28bd1e
#  * @section DESCRIPTION
#  *     Class for printing messages to the console and to the system logger,
#  *     with the option to use timestamp, colored messages, and different
#  *     severity levels.
#  */
# -----------------------------------------------------------------------------

import os
import logging
from enum import Enum
from datetime import datetime

# /** Type Severity Level */
class Severity_Level(Enum):
	CRITICAL = 0
	ERROR = 1
	WARNING = 2
	INFO = 3
	DEBUG = 4

class Print_Helper:
	__BLACK_CLR='\033[30m'
	__RED_CLR='\033[31m'
	__GREEN_CLR='\033[32m'
	__YELLOW_CLR='\033[33m'
	__BLUE_CLR='\033[34m'
	__MAGENTA_CLR='\033[35m'
	__CIAN_CLR='\033[36m'
	__GREY_CLR='\033[37m'
	__WHITE_CLR='\033[38m'
	__RESET='\033[0m'

	def __init__(self, severity_level, show_color, show_timestamp, filename_logger):
		self._severity_level = severity_level
		self._show_color = show_color
		self._show_logger = False
		self._show_timestamp = show_timestamp
		self._filename_logger = filename_logger
		# /** Check if the file path exists */
		if self._filename_logger != None:
			if not os.path.exists(os.path.dirname(self._filename_logger)):
				directory = os.path.dirname(self._filename_logger)
				if not os.path.exists(directory): 
					raise FileNotFoundError(f'The file path {directory} doesn\'t exist.')
			else:
				self._show_logger = True

		# /** Set logging level based on severity level */
		level = {
			Severity_Level.CRITICAL: logging.CRITICAL,
			Severity_Level.ERROR: logging.ERROR,
			Severity_Level.WARNING: logging.WARNING,
			Severity_Level.INFO: logging.INFO,
			Severity_Level.DEBUG: logging.DEBUG
		}[self._severity_level]
		# /** Show logger */
		if self._show_logger:
			# /** Show timestamp */
			if self._show_timestamp:
				#logging.basicConfig(level=level, filename=self._filename_logger.replace(':', ''), filemode = 'a', format='[%(asctime)s.%(msecs)03d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
				logging.basicConfig(level=level, filename=self._filename_logger, filemode = 'a', format='[%(asctime)s.%(msecs)03d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
			else:
				#logging.basicConfig(level=level, filename=self._filename_logger.replace(':', ''), filemode = 'a', format='%(message)s')
				logging.basicConfig(level=level, filename=self._filename_logger, filemode = 'a', format='%(message)s')

	# /** Function to print messages with automatic severity level */
	def print(self, data):
		if '<crt>'in data and self._severity_level.value >= Severity_Level.CRITICAL.value:
			try:
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.debug(data.rstrip('\n'))

		if '<err>'in data and self._severity_level.value >= Severity_Level.ERROR.value:
			try:
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.debug(data.rstrip('\n'))

		if '<wrn>'in data and self._severity_level.value >= Severity_Level.WARNING.value:
			try:
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.debug(data.rstrip('\n'))
		if '<inf>'in data and self._severity_level.value >= Severity_Level.INFO.value:
			try:
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.debug(data.rstrip('\n'))

		if '<dbg>'in data and self._severity_level.value >= Severity_Level.DEBUG.value:
			try:
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.debug(data.rstrip('\n'))

	# /** Function to print messages with CRITICAL severity level */
	def print_crt(self, data):
		if self._severity_level.value >= Severity_Level.CRITICAL.value:
			try:
				data = '<crt> ' + data
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.critical(data.rstrip('\n'))

	# /** Function to print messages with ERROR severity level */
	def print_err(self, data):
		if self._severity_level.value >= Severity_Level.ERROR.value:
			try:
				data = '<err> '  + data
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.error(data.rstrip('\n'))

	# /** Function to print messages with WARNING severity level */
	def print_wrn(self, data):
		if self._severity_level.value >= Severity_Level.WARNING.value:
			try:
				data = '<wrn> ' + data
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.warning(data.rstrip('\n'))

	# /** Function to print messages with INFO severity level */
	def print_inf(self, data):
		if self._severity_level.value >= Severity_Level.INFO.value:
			try:
				data = '<inf> ' + data
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.info(data.rstrip('\n'))

	# /** Function to print messages with DEBUG severity level */
	def print_dbg(self, data):
		if self._severity_level.value >= Severity_Level.DEBUG.value:
			try:
				data = '<dbg> ' + data
				data_print = data
				if self._show_timestamp:
					data_print = self.add_timestamp(data_print)
				if self._show_color:
					data_print = self.add_color(data_print)
				print(data_print, end='', flush=True)
			except IOError as err:
				ret = f'(print_helper) {err}'
			finally:
				if self._show_logger:
					logging.debug(data.rstrip('\n'))

	def add_timestamp(self, data):
		now = datetime.now()
		time_format = '%Y-%m-%d %H:%M:%S.%f'
		time = now.strftime(time_format)
		time = time[0:-3]
		data = f'[{time}] {data}'
		return data
	
	def add_color(self, data):
		if '<crt>'in data:
			data = self.__MAGENTA_CLR + data + self.__RESET
		elif '<err>' in data:
			data = self.__RED_CLR + data + self.__RESET
		elif '<wrn>' in data:
			data = self.__YELLOW_CLR + data + self.__RESET
		elif '<inf>' in data:
			data = self.__WHITE_CLR + data + self.__RESET
		elif '<dbg>' in data:
			data = self.__BLUE_CLR + data + self.__RESET
		return data
