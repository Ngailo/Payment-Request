# -*- coding: utf-8 -*-
from odoo import http

# class PayReq(http.Controller):
#     @http.route('/pay_req/pay_req/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pay_req/pay_req/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pay_req.listing', {
#             'root': '/pay_req/pay_req',
#             'objects': http.request.env['pay_req.pay_req'].search([]),
#         })

#     @http.route('/pay_req/pay_req/objects/<model("pay_req.pay_req"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pay_req.object', {
#             'object': obj
#         })