registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_4356178128 = _loads('(dp1\n.')
    _attrs_4356132752 = _loads('(dp1\n.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4356178000 = _loads('(dp1\nVmethod\np2\nVPOST\np3\nsVenctype\np4\nVmultipart/form-data\np5\ns.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4356178192 = _loads('(dp1\nVclass\np2\nVfa_field\np3\ns.')
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
            attrs = _attrs_4356132752
            _write(u'<div>\n      ')
            attrs = _attrs_4356178000
            u'request.fa_url(request.model_name)'
            _write(u'<form method="POST" enctype="multipart/form-data"')
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
                _write(((' action="' + _tmp1) + '"'))
            u"''"
            _write(u'>\n        ')
            _default.value = default = ''
            u'fs.render()'
            _content = _lookup_attr(econtext['fs'], 'render')()
            attrs = _attrs_4356178128
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
            u"u'\\n        '"
            _write(u'</div>\n        ')
            _default.value = default = u'\n        '
            u'actions.buttons(request)'
            _content = _lookup_attr(econtext['actions'], 'buttons')(econtext['request'])
            attrs = _attrs_4356178192
            u'_content'
            _write(u'<p class="fa_field">')
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
            _write(u'</p>\n      </form>\n    </div>\n')
        u"{'main': _callback_main}"
        _tmp = {'main': _callback_main, }
        u"main.macros['master']"
        _metal.render(_tmp, _out=_out, _write=_write, _domain=_domain, econtext=econtext)
        return _out.getvalue()
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/pyramid_formalchemy/pyramid_formalchemy/templates/admin/new.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
