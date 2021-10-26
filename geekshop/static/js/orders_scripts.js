'use strict'

let order_total_quantity_el = $('.order_total_quantity')[0]
let order_total_price_el = $('.order_total_cost')[0]

let quantity_arr = []
let price_arr = []
let checked_arr = []


window.addEventListener("load", function (e) {

    $('.formset_row').formset({
        prefix: 'formset',
        removed: updateTotals
    });

    $(document).on('click', e => {updateTotals(e)})
})

function updateTotals(e) {
    getData()
    updateData()
}

function getData() {
    let forms_quantity = parseInt($('input[name=order_products-TOTAL_FORMS]').val())
    let qty, price, checked
    for (let i = 0; i < forms_quantity; i++) {
        qty = parseInt($(`#id_order_products-${i}-quantity`).val()) || 0
        price = parseFloat($(`#id_order_products-${i}-price`)[0].textContent.replace('₽', '').replace(',', '')) || 0
        checked = $(`#id_order_products-${i}-product`).parent().parent()[0].style[0] === 'display' ? 0 : 1
        quantity_arr[i] = qty
        price_arr[i] = price
        checked_arr[i] = checked
    }
}

function updateData() {
    let total_qty = 0
    let total_price = 0

    for (let i = 0; i < quantity_arr.length; i++) {
        total_qty = total_qty + (quantity_arr[i] * checked_arr[i])
        total_price = total_price + (price_arr[i] * quantity_arr[i] * checked_arr[i])
    }

    order_total_quantity_el.textContent = total_qty
    order_total_price_el.textContent = total_price.toFixed(2)
}
