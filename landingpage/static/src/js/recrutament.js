/** @odoo-module **/

import publicWidget from 'web.public.widget';


publicWidget.registry.recrutamento = publicWidget.Widget.extend({
    selector: '.homepage',

    /**
     * @override
     */
    start() {
       console.log(" This hello for recrutament")
        let greecard = this.el.querySelector('#getlist')

        if(greecard){
            greecard.innerHTML = '<div>-----------------------------</div>'
            this._rpc({
                route:'/recruitment/',
                params:{}
            }).then(array=> {
                 console.log(array)
            })
        }



    },
});

export default publicWidget.registry.recrutamento;
