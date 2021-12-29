
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal

class MyController(portal.CustomerPortal):

    # @http.route('/estate/index', auth='public')
    # def index(self, **kw):
    #     return "Hello World"


    # @http.route('/estate/index', auth='public')
    # def index(self, **kw):
    #     return http.request.render('estate.index', {
    #         'names':['abc', 'def', 'ghi']
    #         })

    @http.route('/estate/property', auth ='user', website=True)
    def index(self, **kw):
        estate = http.request.env['estate.property']
        return http.request.render('estate.index' ,{
            'properties':estate.search([])
        })

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        properties = request.env['estate.property']
        values['total_properties'] = properties.search_count([]) or 0
        return values

    @http.route('/my/properties', auth='user', website=True)
    def my_properties(self, **kw):
        estate = request.env['estate.property'].search([])
        values = self._prepare_portal_layout_values()
        values.update({
            'properties':estate,
            'page_name':"my_properties",
        })

        return http.request.render('estate.portal_my_properties', values)

    @http.route('/my/properties/<int:id>', auth='user', website=True)
    def my_property(self, id, **kw):
        estate = request.env['estate.property'].search(['id','=',id])
        values = self._prepare_portal_layout_values()
        values.update({
            'property':estate,
            'page_name': "llalallallal",
        })

        return http.request.render('estate.portal_my_properties', values)