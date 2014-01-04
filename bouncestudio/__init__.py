# -*- coding: utf-8 -*-
# bouncestudio is a wrapper around the BoogieTools BounceStudio library
# (http://www.boogietools.com/Products/Linux/). While this wrapper is
# provided freely BoogieTools BounceStudio is not.
#
# Copyright (c) 2013 Dan Nielsen (dnielsen@reacmail.com) 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import ctypes.util
import collections

from ctypes import CDLL, c_char_p, pointer

BOUNCE_MAP = {0: "NON BOUNCE", 10:"HARD BOUNCE", 20:"SOFT BOUNCE GENERAL",
        21:"SOFT BOUNCE DNS FAILURE", 22:"SOFT BOUNCE MAILBOX FULL",
        23:"SOFT BOUNCE MESSAGE SIZE TOO LARGE", 
        30:"BOUNCE WITH NO EMAIL ADDRESS", 40:"GENERAL BOUNCE",
        50:"MAIL BLOCK GENERAL", 51:"MAIL BLOCK KNOWN SPAMMER",
        52:"MAIL BLOCK SPAM DETECTED", 53:"MAIL BLOCK ATTACHMENT DETECTED",
        54:"MAIL BLOCK RELAY DENIED", 60:"AUTO REPLY",
        70:"TRANSIENT BOUNCE", 80:"SUBSCRIBE REQUEST",
        90:"UNSUBSCRIBE REQUEST", 100:"CHALLENGE RESPONSE"}

DSNDetails = collections.namedtuple("DNSDetails", "bs_code bs_type email") 

class Bounce(object):


    def __init__(self, license=None, dsn=None):

        # Try to load the BounceStudio library. First try the 64 bit
        # library and failing that, fall back to the 32 bit version.
        # If nothing loads raise up a runtime error
        try:
            self.libbounce = CDLL(ctypes.util.find_library("BounceStudio64"))
            if not self.libbounce:
                self.libbounce = CDLL(
                        ctypes.util.find_library("BounceStudio32"))
            if not self.libbounce:
                raise RuntimeError("Could not find BounceStudio library")
        except:
            raise RuntimeError("Could not find BounceStudio library")

        self.license = license
        self.dsn = dsn 
        self.libbounce.bsBounceStudio_init()

    def _get_pointer(self, size=100):
        var = c_char_p(size)
        ptr = pointer(var)
        return ptr

    def bounce_check(self):
        ptr = self._get_pointer(100)
        dsn_type = self.libbounce.bsBounceCheck(self.dsn, ptr, "",
                self.license)
        return DSNDetails(dsn_type, BOUNCE_MAP[dsn_type], ptr[0])

    def get_body(self):
        ptr = self._get_pointer(500)
        self.libbounce(self.dsn, ptr)
        return ptr[0]

    def get_from_address(self):
        ptr = self._get_pointer(100)
        self.libbounce.bsGetFromAddress(self.dsn, ptr)
        return ptr[0]

    def get_from_friendly_name(self):
        ptr = self._get_pointer(100)
        self.libbounce.bsGetFromFriendlyName(self.dsn, ptr)
        return ptr[0]

    def get_header(self):
        ptr = self._get_pointer(500)
        self.libbounce.bsGetHeader(self.dsn, ptr)
        return ptr[0]

    def get_reply_to_address(self):
        ptr = self._get_pointer(100)
        self.libbounce.bsGetReplyToAddress(self.dsn, ptr)
        return ptr[0]

    def get_reply_to_friendly_name(self):
        ptr = self._get_pointer(100)
        self.libbounce.bsGetReplyToFriendlyName(self.dsn, ptr)
        return ptr[0]

    def get_subject(self):
        ptr = self._get_pointer(200)
        self.libbounce.bsGetSubject(self.dsn, ptr)
        return ptr[0]

    def get_to_address(self):
        ptr = self._get_pointer(100)
        self.libbounce.bsGetToAddress(self.dsn, ptr)
        return ptr[0]

    def get_to_friendly_name(self):
        ptr = self._get_pointer(100)
        self.libbounce.bsGetToFriendlyName(self.dsn, ptr)
        return ptr[0]

    def get_custom_header(self, header):
        ptr = self._get_pointer(100)
        header = c_char_p(header)
        self.libbounce.bsGetCustomHeader(self.dsn, ptr, header)
        return ptr[0]

    def get_orig_custom_header(self, header):
        ptr = self._get_pointer(200)
        header = c_char_p(header)
        self.libbounce.bsGetOrigCustomHeader(self.dsn, ptr, header)
        return ptr[0]
