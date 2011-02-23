# -*- coding: utf-8 -*-
from pyramid_formalchemy.utils import TemplateEngine
from pyramidapp import models
from formalchemy import Grid, FieldSet
from formalchemy import config

config.engine = TemplateEngine()

MyModel = FieldSet(models.MyModel)

GridMyModel = Grid(models.MyModel)

