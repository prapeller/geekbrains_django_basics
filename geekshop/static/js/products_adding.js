'use strict'

window.onload = function () {
    $('.products-row').on('submit', '.add-to-basket-btn', e => {
        clickOnPutToBasketBtnHandler(e)
    })
}

function clickOnPutToBasketBtnHandler(e) {
    e.preventDefault()
    let id = e.target.id


    $.ajax(
        {
            type: "POST",
            url: `/basket/add_product${id}/`,
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
        })
}