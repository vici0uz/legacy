# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#    Author Alan David Martínez. Copyright Alan David Martínez -             #
#                       alan.david507@gmail.com                              #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or       #
#    (at your option) any later version.                                     #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU General Public License for more details.                            #
#                                                                            #
#    You should have received a copy of the GNU General Public License       #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
#                                                                            #
##############################################################################

from openerp import http
import simplejson
import time
import os
import StringIO


class Binary_Multi(http.Controller):

    @http.route('/web/binary/multi_picture_upload', type="http", auth="public")
    def multi_picture_upload(self, req, callback, ufile):
        out = """<script language="javascript src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                        </script>"""
        args = []
        for nfile in ufile:
                    data = nfile.read()
                    current_dat_time = time.strftime("%d-%m-%Y-%H_%M_%S")
                    file_name = current_dat_time + "_" + nfile.filename
                    addons_path = http.addons_manifest['web']['addons_path'] +\
                        "/web/static/src/img/image_multi/"
                    if not os.path.isdir(addons_path):
                        os.mkdir(addons_path)
                    addons_path += file_name
                    buff = StringIO.StringIO()
                    buff.write(data)
                    buff.seek(0)
                    file_name = "/web/static/src/img/image_multi/" + file_name
                    file = open(addons_path, 'wb')
                    file.write(buff.read())
                    file.close()
                    args.append([len(data), file_name, nfile.content_type,
                                nfile.filename, time.strftime("%m/%d/%Y %H:%M:%S")])
        return out % (simplejson.dumps(callback), simplejson.dumps(args))
