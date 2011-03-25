registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4355418576 = _loads('(dp1\nVstyle\np2\nVdisplay:none\np3\ns.')
    _attrs_4355401296 = _loads('(dp1\n.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4355399952 = _loads('(dp1\n.')
    _attrs_4355441232 = _loads('(dp1\n.')
    _attrs_4355400784 = _loads('(dp1\n.')
    _attrs_4355400912 = _loads('(dp1\nVclass\np2\nVfield_readonly\np3\ns.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_4355400848 = _loads('(dp1\n.')
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
        attrs = _attrs_4355441232
        u'fieldset.render_fields.itervalues()'
        _write(u'<tbody>\n  ')
        _tmp1 = _lookup_attr(_lookup_attr(econtext['fieldset'], 'render_fields'), 'itervalues')()
        field = None
        (_tmp1, _tmp2, ) = repeat.insert('field', _tmp1)
        for field in _tmp1:
            _tmp2 = (_tmp2 - 1)
            u'field.requires_label'
            _write(u'')
            _tmp3 = _lookup_attr(field, 'requires_label')
            if _tmp3:
                pass
                attrs = _attrs_4355401296
                _write(u'<tr>\n      ')
                attrs = _attrs_4355400912
                u"''"
                _write(u'<td class="field_readonly">\n        ')
                _default.value = default = ''
                u'field.label_tag()'
                _content = _lookup_attr(field, 'label_tag')()
                u'_content'
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
                    _write(_tmp)
                u"''"
                _write(u'\n      </td>\n      ')
                _default.value = default = ''
                u'field.render_readonly()'
                _content = _lookup_attr(field, 'render_readonly')()
                attrs = _attrs_4355400848
                u'_content'
                _write(u'<td>')
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
                    _write(_tmp)
                _write(u'</td>\n    </tr>')
            _write(u'\n  ')
            if (_tmp2 == 0):
                break
            _write(' ')
        _write(u'\n  ')
        attrs = _attrs_4355418576
        _write(u'<tr style="display:none">')
        attrs = _attrs_4355400784
        _write(u'<td>&nbsp;</td>')
        attrs = _attrs_4355399952
        u'fieldset.render_fields.itervalues()'
        _write(u'<td>\n    ')
        _tmp1 = _lookup_attr(_lookup_attr(econtext['fieldset'], 'render_fields'), 'itervalues')()
        field = None
        (_tmp1, _tmp2, ) = repeat.insert('field', _tmp1)
        for field in _tmp1:
            _tmp2 = (_tmp2 - 1)
            u"''"
            _write(u'')
            _default.value = default = ''
            u'not field.requires_label'
            _tmp3 = not _lookup_attr(field, 'requires_label')
            if _tmp3:
                pass
                u'field.render_readonly()'
                _content = _lookup_attr(field, 'render_readonly')()
                u'_content'
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
                    _write(_tmp)
            _write(u'\n    ')
            if (_tmp2 == 0):
                break
            _write(' ')
        _write(u'\n  </td>\n  </tr>\n</tbody>')
        return _out.getvalue()
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/pyramid_formalchemy/pyramid_formalchemy/templates/forms/fieldset_readonly.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
