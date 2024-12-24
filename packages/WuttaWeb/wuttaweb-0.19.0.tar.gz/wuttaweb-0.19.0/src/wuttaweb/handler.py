# -*- coding: utf-8; -*-
################################################################################
#
#  wuttaweb -- Web App for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Web Handler
"""

from wuttjamaican.app import GenericHandler

from wuttaweb import static, forms, grids


class WebHandler(GenericHandler):
    """
    Base class and default implementation for the :term:`web handler`.

    This is responsible for determining the :term:`menu handler` and
    various other customizations.
    """

    def get_fanstatic_url(self, request, resource):
        """
        Returns the full URL to the given Fanstatic resource.

        :param request: Current :term:`request` object.

        :param resource: :class:`fanstatic:fanstatic.Resource`
           instance representing an image file or other resource.
        """
        needed = request.environ['fanstatic.needed']
        url = needed.library_url(resource.library) + '/'
        if request.script_name:
            url = request.script_name + url
        return url + resource.relpath

    def get_favicon_url(self, request):
        """
        Returns the canonical app favicon image URL.

        This will return the fallback favicon from WuttaWeb unless
        config specifies an override:

        .. code-block:: ini

           [wuttaweb]
           favicon_url = http://example.com/favicon.ico
        """
        url = self.config.get('wuttaweb.favicon_url')
        if url:
            return url
        return self.get_fanstatic_url(request, static.favicon)

    def get_header_logo_url(self, request):
        """
        Returns the canonical app header image URL.

        This will return the value from config if specified (as shown
        below); otherwise it will just call :meth:`get_favicon_url()`
        and return that.

        .. code-block:: ini

           [wuttaweb]
           header_logo_url = http://example.com/logo.png
        """
        url = self.config.get('wuttaweb.header_logo_url')
        if url:
            return url
        return self.get_favicon_url(request)

    def get_main_logo_url(self, request):
        """
        Returns the canonical app logo image URL.

        This will return the fallback logo from WuttaWeb unless config
        specifies an override:

        .. code-block:: ini

           [wuttaweb]
           logo_url = http://example.com/logo.png
        """
        url = self.config.get('wuttaweb.logo_url')
        if url:
            return url
        return self.get_fanstatic_url(request, static.logo)

    def get_menu_handler(self, **kwargs):
        """
        Get the configured "menu" handler for the web app.

        Specify a custom handler in your config file like this:

        .. code-block:: ini

           [wutta.web]
           menus.handler_spec = poser.web.menus:PoserMenuHandler

        :returns: Instance of :class:`~wuttaweb.menus.MenuHandler`.
        """
        if not hasattr(self, 'menu_handler'):
            spec = self.config.get(f'{self.appname}.web.menus.handler_spec',
                                   default='wuttaweb.menus:MenuHandler')
            self.menu_handler = self.app.load_object(spec)(self.config)
        return self.menu_handler

    def make_form(self, request, **kwargs):
        """
        Make and return a new :class:`~wuttaweb.forms.base.Form`
        instance, per the given ``kwargs``.

        This is the "base" factory which merely invokes the
        constructor.
        """
        return forms.Form(request, **kwargs)

    def make_grid(self, request, **kwargs):
        """
        Make and return a new :class:`~wuttaweb.grids.base.Grid`
        instance, per the given ``kwargs``.

        This is the "base" factory which merely invokes the
        constructor.
        """
        return grids.Grid(request, **kwargs)
