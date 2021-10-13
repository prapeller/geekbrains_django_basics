'use strict'

window.onload = function () {
    $('.basket-list').on('click', '.quantity_select', e => {
        clickOnBasketNumbersHandler(e)
    })
    $('.products-row').on('submit', '.add-to-basket-btn', e => {
        clickOnPutToBasketBtnHandler(e)
    })
}

function clickOnBasketNumbersHandler(e) {
    e.preventDefault()
    let t = e.target

    $.ajax({
        url: `/basket/edit/${t.name}/${t.value}/`,
        success: data => {
            $('.basket-list').html(data.result)
        }
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