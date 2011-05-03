# -*- coding: utf-8 -*-
from pyramid_formalchemy.utils import TemplateEngine
from pyramidapp import models
from formalchemy import Grid, FieldSet
from formalchemy import fields
from formalchemy import config

config.engine = TemplateEngine()

FieldSet.default_renderers['dropdown'] = fields.SelectFieldRenderer

MyModel = FieldSet(models.MyModel)

GridMyModel = Grid(models.MyModel)
GridMyModelReadOnly = Grid(models.MyModel)
GridMyModelReadOnly.configure(readonly=True)

FooEdit = FieldSet(models.Foo)
FooEdit.configure()
