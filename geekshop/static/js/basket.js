'use strict'

window.onload = function () {
    $('.basket-list').on('click', 'input[type="number"]', e => {
        clickOnBasketNumbersHandler(e)
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