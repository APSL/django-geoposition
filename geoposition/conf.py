# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf


class GeopositionConf(AppConf):
    MAP_WIDGET_HEIGHT = 480
    MAP_OPTIONS = {}
    MARKER_OPTIONS = {}
    GEOPOSITION_GOOGLE_MAPS_API_KEY = ''

    class Meta:
        prefix = 'geoposition'
