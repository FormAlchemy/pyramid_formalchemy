registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_4355399760 = _loads('(dp1\n.')
    _attrs_4355400208 = _loads('(dp1\nVclass\np2\nVfa_instructions ui-corner-all\np3\ns.')
    _attrs_4355399888 = _loads('(dp1\n.')
    _attrs_4355400144 = _loads('(dp1\nVclass\np2\nVlabel\np3\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4355400400 = _loads('(dp1\nVclass\np2\nVui-state-error ui-corner-all\np3\ns.')
    _attrs_4355400080 = _loads('(dp1\n.')
    _attrs_4355400464 = _loads('(dp1\nVclass\np2\nVfield_input\np3\ns.')
    _attrs_4355400528 = _loads('(dp1\n.')
    _attrs_4355400016 = _loads('(dp1\nVclass\np2\nVfa_field ui-widget\np3\ns.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_4355400272 = _loads('(dp1\n.')
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
        u'False'
        focus_rendered = False
        u'fieldset.errors.get(None, False)'
        _write(u'\n')
        _tmp1 = _lookup_attr(_lookup_attr(econtext['fieldset'], 'errors'), 'get')(None, False)
        if _tmp1:
            pass
            attrs = _attrs_4355399760
            u"''"
            _write(u'<div>\n  ')
            _default.value = default = ''
            u'fieldset.error.get(None)'
            _tmp1 = _lookup_attr(_lookup_attr(econtext['fieldset'], 'error'), 'get')(None)
            error = None
            (_tmp1, _tmp2, ) = repeat.insert('error', _tmp1)
            for error in _tmp1:
                _tmp2 = (_tmp2 - 1)
                u'error'
                _content = error
                attrs = _attrs_4355399888
                u'_content'
                _write(u'<div>')
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
                _write(u'</div>')
                if (_tmp2 == 0):
                    break
                _write(' ')
            _write(u'\n</div>')
        u'fieldset.render_fields.itervalues()'
        _write(u'\n\n')
        _tmp1 = _lookup_attr(_lookup_attr(econtext['fieldset'], 'render_fields'), 'itervalues')()
        field = None
        (_tmp1, _tmp2, ) = repeat.insert('field', _tmp1)
        for field in _tmp1:
            _tmp2 = (_tmp2 - 1)
            _write(u'\n  ')
            attrs = _attrs_4355400016
            u'field.requires_label'
            _write(u'<div class="fa_field ui-widget">\n    ')
            _tmp3 = _lookup_attr(field, 'requires_label')
            if _tmp3:
                pass
                attrs = _attrs_4355400144
                u"''"
                _write(u'<div class="label">\n      ')
                _default.value = default = ''
                u'isinstance(field.type, fatypes.Boolean)'
                _tmp3 = isinstance(_lookup_attr(field, 'type'), _lookup_attr(econtext['fatypes'], 'Boolean'))
                if _tmp3:
                    pass
                    u'field.render()'
                    _content = _lookup_attr(field, 'render')()
                    attrs = _attrs_4355400272
                    u'_content'
                    _write(u'<div>')
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
                    _write(u'</div>')
                u"''"
                _write(u'\n      ')
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
                _write(u'\n    </div>')
            u"u'\\n    '"
            _write(u'\n    ')
            _default.value = default = u'\n    '
            u"'instructions' in field.metadata"
            _tmp3 = ('instructions' in _lookup_attr(field, 'metadata'))
            if _tmp3:
                pass
                u"field.metadata['instructions']"
                _content = _lookup_attr(field, 'metadata')['instructions']
                attrs = _attrs_4355400208
                u'_content'
                _write(u'<div class="fa_instructions ui-corner-all">')
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
                _write(u'</div>')
            u'field.errors'
            _write(u'\n    ')
            _tmp3 = _lookup_attr(field, 'errors')
            if _tmp3:
                pass
                attrs = _attrs_4355400400
                u"''"
                _write(u'<div class="ui-state-error ui-corner-all">\n      ')
                _default.value = default = ''
                u'field.errors'
                _tmp3 = _lookup_attr(field, 'errors')
                error = None
                (_tmp3, _tmp4, ) = repeat.insert('error', _tmp3)
                for error in _tmp3:
                    _tmp4 = (_tmp4 - 1)
                    u'error'
                    _content = error
                    attrs = _attrs_4355400528
                    u'_content'
                    _write(u'<div>')
                    _tmp5 = _content
                    _tmp = _tmp5
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
                    _write(u'</div>')
                    if (_tmp4 == 0):
                        break
                    _write(' ')
                _write(u'\n    </div>')
            u"''"
            _write(u'\n    ')
            _default.value = default = ''
            u'not isinstance(field.type, fatypes.Boolean)'
            _tmp3 = not isinstance(_lookup_attr(field, 'type'), _lookup_attr(econtext['fatypes'], 'Boolean'))
            if _tmp3:
                pass
                u'field.render()'
                _content = _lookup_attr(field, 'render')()
                attrs = _attrs_4355400464
                u'_content'
                _write(u'<div class="field_input">')
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
                _write(u'</div>')
            u'not field.is_readonly() and (fieldset.focus == field or fieldset.focus is True) and not focus_rendered'
            _write(u'\n  </div>\n  ')
            _tmp3 = (not _lookup_attr(field, 'is_readonly')() and ((_lookup_attr(econtext['fieldset'], 'focus') == field) or (_lookup_attr(econtext['fieldset'], 'focus') is True)) and not focus_rendered)
            if _tmp3:
                pass
                attrs = _attrs_4355400080
                u'True'
                _write(u'<script>\n    ')
                focus_rendered = True
                u'field.renderer.name'
                _write(u'\n    jQuery(document).ready(function(){jQuery("[name=\'')
                _tmp3 = _lookup_attr(_lookup_attr(field, 'renderer'), 'name')
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
                _write(u'\']").focus();});\n  </script>')
            _write(u'\n')
            if (_tmp2 == 0):
                break
            _write(' ')
        _write(u'')
        return _out.getvalue()
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/pyramid_formalchemy/pyramid_formalchemy/templates/forms/fieldset.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
