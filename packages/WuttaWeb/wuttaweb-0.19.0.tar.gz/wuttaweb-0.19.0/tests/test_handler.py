# -*- coding: utf-8; -*-

from wuttaweb import handler as mod, static
from wuttaweb.forms import Form
from wuttaweb.grids import Grid
from wuttaweb.menus import MenuHandler
from tests.util import WebTestCase


class TestWebHandler(WebTestCase):

    def make_handler(self):
        return mod.WebHandler(self.config)

    def test_get_fanstatic_url(self):
        handler = self.make_handler()

        # default with / root path
        url = handler.get_fanstatic_url(self.request, static.logo)
        self.assertEqual(url, '/fanstatic/wuttaweb_img/logo.png')

        # what about a subpath
        self.request.script_name = '/testing'
        url = handler.get_fanstatic_url(self.request, static.logo)
        self.assertEqual(url, '/testing/fanstatic/wuttaweb_img/logo.png')

    def test_get_favicon_url(self):
        handler = self.make_handler()

        # default
        url = handler.get_favicon_url(self.request)
        self.assertEqual(url, '/fanstatic/wuttaweb_img/favicon.ico')

        # config override
        self.config.setdefault('wuttaweb.favicon_url', '/testing/other.ico')
        url = handler.get_favicon_url(self.request)
        self.assertEqual(url, '/testing/other.ico')

    def test_get_header_logo_url(self):
        handler = self.make_handler()

        # default
        url = handler.get_header_logo_url(self.request)
        self.assertEqual(url, '/fanstatic/wuttaweb_img/favicon.ico')

        # config override
        self.config.setdefault('wuttaweb.header_logo_url', '/testing/header.png')
        url = handler.get_header_logo_url(self.request)
        self.assertEqual(url, '/testing/header.png')

    def test_get_main_logo_url(self):
        handler = self.make_handler()

        # default
        url = handler.get_main_logo_url(self.request)
        self.assertEqual(url, '/fanstatic/wuttaweb_img/logo.png')

        # config override
        self.config.setdefault('wuttaweb.logo_url', '/testing/other.png')
        url = handler.get_main_logo_url(self.request)
        self.assertEqual(url, '/testing/other.png')

    def test_menu_handler_default(self):
        handler = self.make_handler()
        menus = handler.get_menu_handler()
        self.assertIsInstance(menus, MenuHandler)

    def test_make_form(self):
        handler = self.make_handler()
        form = handler.make_form(self.request)
        self.assertIsInstance(form, Form)

    def test_make_grid(self):
        handler = self.make_handler()
        grid = handler.make_grid(self.request)
        self.assertIsInstance(grid, Grid)
