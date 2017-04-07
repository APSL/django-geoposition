from __future__ import unicode_literals

import json
from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None, None]

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)

        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')

        context = {'id': id_, 'name': name, 'fields': []}
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            context['fields'].append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        context.update(self.get_extra_context())

        return mark_safe(self.format_output(context))

    def get_extra_context(self):
        return {
            'config': {
                'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
                'map_options': json.dumps(settings.MAP_OPTIONS),
                'marker_options': json.dumps(settings.MARKER_OPTIONS),
            }
        }

    def format_output(self, context):
        context.update({
            'latitude': {'html': context['fields'][0], 'label': _("latitude")},
            'longitude': {'html': context['fields'][1], 'label': _("longitude")},
        })
        return render_to_string('geoposition/widgets/geoposition.html', context)

    class Media:
        js = (
            '//maps.google.com/maps/api/js?key=%s' % settings.GOOGLE_MAPS_API_KEY,
            'geoposition/geoposition.js',
        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
