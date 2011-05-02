registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_4359005584 = _loads('(dp1\n.')
    _attrs_4359005840 = _loads('(dp1\nVname\np2\nV_method\np3\nsVtype\np4\nVhidden\np5\nsVvalue\np6\nVPUT\np7\ns.')
    _attrs_4359006416 = _loads('(dp1\nVclass\np2\nVfa_field\np3\ns.')
    _attrs_4359006672 = _loads('(dp1\nVclass\np2\nVui-widget-header ui-widget-link ui-corner-all\np3\ns.')
    _attrs_4359005008 = _loads('(dp1\nVclass\np2\nVui-icon ui-icon-circle-arrow-w\np3\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4359005968 = _loads('(dp1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4359006544 = _loads('(dp1\nVhref\np2\nV#\nsVclass\np3\nVui-widget-header ui-widget-link ui-widget-button ui-corner-all\np4\ns.')
    _attrs_4359005520 = _loads('(dp1\nVaction\np2\nV\nsVmethod\np3\nVPOST\np4\nsVenctype\np5\nVmultipart/form-data\np6\ns.')
    _attrs_4359006736 = _loads("(dp1\nVtype\np2\nVsubmit\np3\nsVvalue\np4\nV${F_('Save')}\np5\ns.")
    _attrs_4359005776 = _loads('(dp1\n.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u'_init_stream()'
        (_out, _write, ) = _init_stream()
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        u"main.macros['master']"
        _metal = _lookup_attr(econtext['main'], 'macros')['master']
        def _callback_main(econtext, _repeat, _out=_out, _write=_write, _domain=_domain, **_ignored):
            if _repeat:
                repeat.update(_repeat)
            attrs = _attrs_4359005584
            _write(u'<div>\n      ')
            attrs = _attrs_4359005520
            u"''"
            _write(u'<form action="" method="POST" enctype="multipart/form-data">\n        ')
            _default.value = default = ''
            u'fs.render()'
            _content = _lookup_attr(econtext['fs'], 'render')()
            attrs = _attrs_4359005776
            u'_content'
            _write(u'<div>')
            _tmp1 = _content
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = str(_tmp)
                _write(_tmp)
            _write(u'</div>\n        ')
            attrs = _attrs_4359005840
            _write(u'<input type="hidden" name="_method" value="PUT" />\n        ')
            attrs = _attrs_4359005968
            _write(u'<div>\n          ')
            attrs = _attrs_4359006416
            _write(u'<p class="fa_field">\n            ')
            attrs = _attrs_4359006544
            _write(u'<a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all" href="#">\n              ')
            attrs = _attrs_4359006736
            'join(value("F_(\'Save\')"),)'
            _write(u'<input type="submit"')
            _tmp1 = econtext['F_']('Save')
            if (_tmp1 is _default):
                _tmp1 = u"${F_('Save')}"
            if ((_tmp1 is not None) and (_tmp1 is not False)):
                if (_tmp1.__class__ not in (str, unicode, int, float, )):
                    _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp1, unicode):
                        _tmp1 = str(_tmp1)
                if ('&' in _tmp1):
                    if (';' in _tmp1):
                        _tmp1 = _re_amp.sub('&amp;', _tmp1)
                    else:
                        _tmp1 = _tmp1.replace('&', '&amp;')
                if ('<' in _tmp1):
                    _tmp1 = _tmp1.replace('<', '&lt;')
                if ('>' in _tmp1):
                    _tmp1 = _tmp1.replace('>', '&gt;')
                if ('"' in _tmp1):
                    _tmp1 = _tmp1.replace('"', '&quot;')
                _write(((' value="' + _tmp1) + '"'))
            _write(u' />\n            </a>\n            ')
            attrs = _attrs_4359006672
            u'request.fa_url(request.model_name)'
            _write(u'<a class="ui-widget-header ui-widget-link ui-corner-all"')
            _tmp1 = _lookup_attr(econtext['request'], 'fa_url')(_lookup_attr(econtext['request'], 'model_name'))
            if (_tmp1 is _default):
                _tmp1 = None
            if ((_tmp1 is not None) and (_tmp1 is not False)):
                if (_tmp1.__class__ not in (str, unicode, int, float, )):
                    _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp1, unicode):
                        _tmp1 = str(_tmp1)
                if ('&' in _tmp1):
                    if (';' in _tmp1):
                        _tmp1 = _re_amp.sub('&amp;', _tmp1)
                    else:
                        _tmp1 = _tmp1.replace('&', '&amp;')
                if ('<' in _tmp1):
                    _tmp1 = _tmp1.replace('<', '&lt;')
                if ('>' in _tmp1):
                    _tmp1 = _tmp1.replace('>', '&gt;')
                if ('"' in _tmp1):
                    _tmp1 = _tmp1.replace('"', '&quot;')
                _write(((' href="' + _tmp1) + '"'))
            _write(u'>\n              ')
            attrs = _attrs_4359005008
            u"F_('Cancel')"
            _write(u'<span class="ui-icon ui-icon-circle-arrow-w"></span>\n              ')
            _tmp1 = econtext['F_']('Cancel')
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = str(_tmp)
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            _write(u'\n            </a>\n          </p>\n        </div>\n      </form>\n    </div>\n')
        u"{'main': _callback_main}"
        _tmp = {'main': _callback_main, }
        u"main.macros['master']"
        _metal.render(_tmp, _out=_out, _write=_write, _domain=_domain, econtext=econtext)
        return _out.getvalue()
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/pyramid_formalchemy/pyramid_formalchemy/templates/admin/edit.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
