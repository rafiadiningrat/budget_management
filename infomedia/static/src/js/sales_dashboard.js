/** @odoo-module **/
import { Component, mount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class SalesDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = {
            totalSales: 0,
            topProducts: [],
        };
        this.loadData();
    }

    async loadData() {
        const totalSales = await this.orm.searchRead("sale.order", [], ["amount_total"]);
        const topProducts = await this.orm.searchRead("product.product", [], ["name", "sales_count"], {
            limit: 5,
            order: "sales_count desc",
        });
        this.state.totalSales = totalSales.reduce((acc, sale) => acc + sale.amount_total, 0);
        this.state.topProducts = topProducts;
    }

    static template = "sales_dashboard.dashboard_main";
}

mount(SalesDashboard, { target: document.getElementById("sales_dashboard_root") });
