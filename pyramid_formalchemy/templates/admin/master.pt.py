registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_4358968400 = _loads('(dp1\n.')
    _attrs_4358849552 = _loads('(dp1\n.')
    _attrs_4358967760 = _loads('(dp1\nVid\np2\nVheader\np3\nsVclass\np4\nVui-widget-header ui-corner-all\np5\ns.')
    _attrs_4358720592 = _loads('(dp1\nVrel\np2\nVstylesheet\np3\ns.')
    _attrs_4358967504 = _loads('(dp1\nVid\np2\nVcontent\np3\nsVclass\np4\nVui-admin ui-widget\np5\ns.')
    _attrs_4358967888 = _loads('(dp1\nVclass\np2\nVbreadcrumb\np3\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4358968272 = _loads('(dp1\n.')
    _attrs_4358721104 = _loads('(dp1\n.')
    _attrs_4358721040 = _loads('(dp1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4358721232 = _loads('(dp1\n.')
    _attrs_4358967696 = _loads('(dp1\n.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_4358967952 = _loads('(dp1\n.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u"%(scope)s['%(out)s'], %(scope)s['%(write)s']"
        (_out, _write, ) = (econtext['_out'], econtext['_write'], )
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        attrs = _attrs_4358849552
        _write(u'<html>\n    ')
        attrs = _attrs_4358721040
        u"''"
        _write(u'<head>\n      ')
        _default.value = default = ''
        u"request.model_name or 'root'"
        _content = (_lookup_attr(econtext['request'], 'model_name') or 'root')
        attrs = _attrs_4358721104
        u'_content'
        _write(u'<title>')
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
        _write(u'</title>\n      ')
        attrs = _attrs_4358720592
        u"request.static_url('pyramid_formalchemy:static/admin.css')"
        _write(u'<link rel="stylesheet"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('pyramid_formalchemy:static/admin.css')
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
        _write(u'></link>\n    </head>\n    ')
        attrs = _attrs_4358721232
        _write(u'<body>\n      ')
        attrs = _attrs_4358967504
        _write(u'<div id="content" class="ui-admin ui-widget">\n        ')
        attrs = _attrs_4358967760
        _write(u'<h1 id="header" class="ui-widget-header ui-corner-all">\n          ')
        attrs = _attrs_4358967888
        u'breadcrumb'
        _write(u'<div class="breadcrumb">\n            ')
        _tmp1 = econtext['breadcrumb']
        item = None
        (_tmp1, _tmp2, ) = repeat.insert('item', _tmp1)
        for item in _tmp1:
            _tmp2 = (_tmp2 - 1)
            u"''"
            _write(u'')
            _default.value = default = ''
            u'item[1]'
            _content = item[1]
            attrs = _attrs_4358968400
            u'item[0]'
            _write(u'<a')
            _tmp3 = item[0]
            if (_tmp3 is _default):
                _tmp3 = None
            if ((_tmp3 is not None) and (_tmp3 is not False)):
                if (_tmp3.__class__ not in (str, unicode, int, float, )):
                    _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp3, unicode):
                        _tmp3 = str(_tmp3)
                if ('&' in _tmp3):
                    if (';' in _tmp3):
                        _tmp3 = _re_amp.sub('&amp;', _tmp3)
                    else:
                        _tmp3 = _tmp3.replace('&', '&amp;')
                if ('<' in _tmp3):
                    _tmp3 = _tmp3.replace('<', '&lt;')
                if ('>' in _tmp3):
                    _tmp3 = _tmp3.replace('>', '&gt;')
                if ('"' in _tmp3):
                    _tmp3 = _tmp3.replace('"', '&quot;')
                _write(((' href="' + _tmp3) + '"'))
            u'_content'
            _write('>')
            _tmp3 = _content
            _tmp = _tmp3
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
            u'not repeat.item.end'
            _write(u'</a>\n                ')
            _tmp3 = not _lookup_attr(repeat.item, 'end')
            if _tmp3:
                pass
                attrs = _attrs_4358968272
                _write(u'<span>/</span>')
            _write(u'\n            ')
            if (_tmp2 == 0):
                break
            _write(' ')
        u"''"
        _write(u'\n          </div>\n          ')
        _default.value = default = ''
        u"request.model_name or 'root'"
        _content = (_lookup_attr(econtext['request'], 'model_name') or 'root')
        attrs = _attrs_4358967952
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
        u"%(slots)s.get(u'main')"
        _write(u'</div>\n        </h1>\n        ')
        _tmp = _slots.get(u'main')
        u'%(tmp)s is not None'
        _tmp1 = (_tmp is not None)
        if _tmp1:
            pass
            u'isinstance(%(tmp)s, basestring)'
            _tmp2 = isinstance(_tmp, basestring)
            if not _tmp2:
                pass
                econtext.update(dict(rcontext=rcontext, _domain=_domain))
                _tmp(econtext, repeat)
            else:
                pass
                u'%(tmp)s'
                _tmp2 = _tmp
                _tmp = _tmp2
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
        else:
            pass
            attrs = _attrs_4358967696
            _write(u'<div>\n        </div>')
        _write(u'\n      </div>\n    </body>\n</html>')
        return
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/pyramid_formalchemy/pyramid_formalchemy/templates/admin/master.pt'
registry[('master', False, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
