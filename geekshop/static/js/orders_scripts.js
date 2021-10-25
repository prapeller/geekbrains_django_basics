'use strict'

let order_total_quantity_el = document.getElementsByClassName('order_total_quantity')[0]
let order_total_price_el = document.getElementsByClassName('order_total_cost')[0]

let quantity_arr = []
let price_arr = []
let checked_arr = []


window.addEventListener("click", function (e) {
    clickHandler(e)
})

function clickHandler(e) {
    get_data()
    update_totals()
}

function get_data() {
    let _quantity, _price, _checked
    let forms_quantity = parseInt($('input[name=order_products-TOTAL_FORMS]').val())

    for (let i = 0; i < forms_quantity; i++) {
        _quantity = parseInt(document.getElementById(`id_order_products-${i}-quantity`).value) || 0
        _price = parseFloat(document.getElementById(`id_order_products-${i}-price`).value.replace('₽', '').replace(',', '')) || 0
        _checked = document.getElementById(`id_order_products-${i}-DELETE`).checked === true ? 0 : 1

        quantity_arr[i] = _quantity
        price_arr[i] = _price
        checked_arr[i] = _checked
    }
}

function update_totals() {

    let total_qty = 0
    let total_price = 0
    for (let i = 0; i < quantity_arr.length; i++) {
        total_qty = total_qty + (quantity_arr[i] * checked_arr[i])
        total_price = total_price + (price_arr[i] * quantity_arr[i] * checked_arr[i])
    }

    order_total_quantity_el.textContent = total_qty
    order_total_price_el.textContent = total_price
}
