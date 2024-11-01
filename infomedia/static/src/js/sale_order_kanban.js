odoo.define('sale_order_kanban.kanban', function (require) {
    "use strict";

    var KanbanView = require('web.KanbanView');
    var KanbanController = require('web.KanbanController');
    var view_registry = require('web.view_registry');

    var SaleOrderKanbanController = KanbanController.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.isSearched = false;
            console.log("Kanban Controller initialized");
        },

        _onSearch: function (searchQuery) {
            console.log("Search query: ", searchQuery);
            this.isSearched = true;
            this._super.apply(this, arguments);
            
            if (searchQuery.length > 0) {
                this.model.domain = this.model.domain.filter(item => item[0] !== 'id');
            } else {
                this.model.domain.push(['id', '=', false]);
            }
            
            this.reload();
        },
    });

    var SaleOrderKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: SaleOrderKanbanController,
        }),
    });

    view_registry.add('sale_order_kanban', SaleOrderKanbanView);

    return SaleOrderKanbanView;
});
