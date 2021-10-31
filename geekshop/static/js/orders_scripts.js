'use strict'

let order_total_quantity_el = $('.order_total_quantity')[0]
let order_total_price_el = $('.order_total_cost')[0]

$(window).on('load', e => {
    $('.formset_row').formset({
        prefix: 'formset',
        removed: update,
        added: update
    });
})

$('.table').on('click', e => {
    update()
})

function update() {
    let total_qty = 0
    let total_price = 0
    let forms_el_arr = $('.formset_row').toArray().filter(el => el.style[0] !== 'display')

    for (let i = 0; i < forms_el_arr.length; i++) {
        let form_el = forms_el_arr[i]

        let product_select = form_el.getElementsByClassName('td1')[0].children[2]
        let id
        id = parseInt(product_select.value)

        let qty_input = form_el.getElementsByClassName('td2')[0].children[0]
        let qty = parseInt(qty_input.value) || 0
        qty_input.value = qty
        total_qty = total_qty + qty


        if (!isNaN(id)) {
            $.ajax({
                url: `/products/price/${id}/`,
                success: data => {
                    let price_input = form_el.getElementsByClassName('td3')[0].children[0]
                    total_price = total_price + (qty * data.price)
                    price_input.innerText = data.price
                    order_total_price_el.textContent = total_price.toFixed(2)
                }
            })
        }
    }

    order_total_quantity_el.textContent = total_qty
}


