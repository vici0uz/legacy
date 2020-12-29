# -*- coding: utf-8 -*-

import logging
import itertools
import operator

import werkzeug.utils

import openerp
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import WebClient
from clint.textui import colored

_logger = logging.getLogger(__name__)

class TranslationX(http.Controller):
    @http.route('/web/webclient/translations', type="json", auth="none")
    def translations(self, mods=None, lang=None):
        request.disable_db = False
        uid = openerp.SUPERUSER_ID
        print colored.cyan("HOLAAAAA")
        if mods is None:
            m = request.registry.get('ir.module.module')
            mods = [x['name'] for x in m.search_read(request.cr, uid,
                [('state','=','installed')], ['name'])]
        if lang is None:
            lang = request.context["lang"]
        res_lang = request.registry.get('res.lang')
        ids = res_lang.search(request.cr, uid, [("code", "=", lang)])
        lang_params = None
        if ids:
            lang_params = res_lang.read(request.cr, uid, ids[0], ["direction", "date_format", "time_format",
                            "grouping", "decimal_point", "thousands_sep", "view_decimal"])

        # Regional languages (ll_CC) must inherit/override their parent lang (ll), but this is
        # done server-side when the language is loaded, so we only need to load the user's lang.
        ir_translation = request.registry.get('ir.translation')
        translations_per_module = {}
        messages = ir_translation.search_read(request.cr, uid, [('module','in',mods),('lang','=',lang),
                            ('comments','like','openerp-web'),('value','!=',False),
                            ('value','!=','')],
                            ['module','src','value','lang'], order='module')
        for mod, msg_group in itertools.groupby(messages, key=operator.itemgetter('module')):
            translations_per_module.setdefault(mod,{'messages':[]})
            translations_per_module[mod]['messages'].extend({'id': m['src'],
                                                                'string': m['value']} \
                                                                for m in msg_group)
        return {"modules": translations_per_module,
                "lang_parameters": lang_params}

    WebClient.translations = translations
