openerp.petstore = function(instance, local){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    // QWeb.render("petstore.HomePageTemplate", {name: "Klaus"});
    local.HomePage = instance.Widget.extend({
        // className: 'petstore_homepage',
        // template: "HomePageTemplate",
        // start: function(){
        //     QWeb.render("HomePageTemplate", {name: "Klaus"});
        //     // this.$el.append(QWeb.render("HomePageTemplate"));
        //     // this.$el.append("<div>Hello dear Odoo user!</div>");
        //     // var greeting = new local.GreetingsWidget(this);
        //     // return greeting.appendTo(this.$el);
        //     // this.$el.append("<div>Riko, Sabrosongo, Zuculento, Zabrontosaurio, Exquisito</div>");
        //     // this.$el.append("<div>Hello dear Hijo de mil putas!</div>");
        //     // console.log("pet store home page loaded");
        // },
        // init: function(parent) {
        //     this._super(parent);
        //     this.name = "Mordecai";
        // },
        start: function(){
            var products = new local.ProductsWidget(
                this, ["cpu", "mouse", "keyboard", "graphic card", "screen"], "#00FF00");
            products.appendTo(this.$el);
        },
    });
    local.ProductsWidget = instance.Widget.extend({
        template: "ProductsWidget",
        init: function(parent, products, color){
            this._super(parent);
            this.products = products;
            this.color = color;
        },
    });
    // local.GreetingsWidget = instance.Widget.extend({
    //     className: 'oe_petstore_greetings',
    //     start: function() {
    //         this.$el.append("<div>We are so happy to see you again in this menu!</div>");
    //     },
    // });

    instance.web.client_actions.add('petstore.homepage', 'instance.petstore.HomePage');
}
