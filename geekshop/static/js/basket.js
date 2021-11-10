'use strict'

window.addEventListener("load", function (evt) {
    $('.basket-list').on('click', '.quantity_select', e => {
        clickOnBasketNumbersHandler(e)
    })
    $('.products-row').on('submit', '.add-to-basket-btn', e => {
        clickOnPutToBasketBtnHandler(e)
    })
})

function clickOnBasketNumbersHandler(e) {
    e.preventDefault()
    let t = e.target
    console.log(t)

    $.ajax(
        {
            url: `/basket/edit/${t.id}/${t.value}/`,
            success: data => {
                $('.basket-list').html(data.result)
                $('.basket_total_qty').text(data.basket_total_qty)
            }
        })
}

function clickOnPutToBasketBtnHandler(e) {
    e.preventDefault()
    let id = e.target.id

    $.ajax(
        {
            type: "POST",
            url: `/basket/add_product/${id}/`,
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
            success: data => {
                $('.basket_total_qty').text(data.basket_total_qty)
            },
        })

}
