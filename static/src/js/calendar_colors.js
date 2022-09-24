odoo.define('sale_order_calendar_state.CalendarColors' , function (require) {
"use strict";
var CalendarRenderer = require('web.CalendarRenderer');
var CalendarModel = require('web.CalendarModel');

CalendarModel.include({
    load: function (params) {
        var self = this;
        if (params.modelName == 'sale.order') {
            params.fieldColor = 'color';
        }
        return this._super(params);
    },
});

CalendarRenderer.include({
    getColor: function (key) {
        if (!key) {
            return;
        }
        if (this.color_map[key]) {
            return Math.abs(this.color_map[key]);
        }
        if (typeof key === 'number' && key < 0) {
            return Math.abs(key);
        }
        return this._super(key);
    },
    init: function (parent, state, params) {
        this._super(parent, state, params);
        if (this.model === 'sale.order') {
            this.color_map = {
                'to_process': -301,
                'to_evaluate': -301,
                'to_evaluate_production': -301,
                'to_produce': -302,
                'to_receive': -302,
                'production_planned': -304,
                'production_ready': -308,
                'production_started': -306,
                'to_pack': -307,
                'submanufacture_started': -314,
                'submanufacture_done': -315,
                'test_check': -316,
                'delivery_ready': -317,
                'production_done': -305,
                'partially_delivered': -309,
                'delivery_done':  -305,
                'available' : -312,
                'invoiced': -313,
                'shipped': -312,
            }
        }
    }
});
});