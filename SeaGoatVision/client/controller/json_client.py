#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from SeaGoatVision.commons import log
from SeaGoatVision.commons.param import Param
import jsonrpclib
logger = log.get_logger(__name__)

class Json_client():
    def __init__(self, port, host=""):
        self.rpc = jsonrpclib.Server('http://%s:%s' % (host, port))

    def __getattr__(self, name):
        def cb_rpc():
            return getattr(self.rpc, name)
        return cb_rpc()

    def get_params_media(self, media_name):
        lst_ser_param = self.rpc.get_params_media(media_name)
        lst_param = [Param("temps", None, serialize=param_ser) for param_ser in lst_ser_param]
        return lst_param
