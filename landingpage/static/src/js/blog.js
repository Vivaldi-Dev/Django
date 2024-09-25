/** @odoo-module **/

import publicWidget from 'web.public.widget';
import {generateGMapLink, generateGMapIframe} from 'website.utils';

publicWidget.registry.blog = publicWidget.Widget.extend({
    selector: '.blog',

    /**
     * @override
     */
    start() {
        console.log("Hello word ")
//        console.log(this.el.querySelector('#cards'))
        let card = this.el.querySelector('#liSt')

        if(card){
//            card.innerHTML='Hello word'
            let html =``
            this._rpc({
                route:'/get-blog/',
                params:{}

            }).then(data=> {

                console.log(data)

                data.forEach(entry => {
                console.log(entry)
                const postLink = `/teste/${entry.id}`;

                html += `

                         <div class="Item">

                                <div class="COnTent">
                                <a href="${postLink}">
                                    <img src="data:image/png;base64,${entry.featured_image_url}" alt="" loading="lazy"/>
                                </a>
                                         alt="" loading="lazy"/>
                                    <div class="pintura" ">
                                        <p style="color: white">${entry.post_title}</p>

                                    </div>
                                </div>
                            </div>

                         `

                })
                           card.innerHTML = html

            })

        }
    },
});

export default publicWidget.registry.blog;
