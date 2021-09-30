'use strict'

window.onload = function () {
    $('.basket-list').on('click', 'input[type="number"]', e => {
        clickOnBasketNumbersHandler(e)
    })
}

function clickOnBasketNumbersHandler(e) {
    // e.preventDefault()
    let t = e.target
    console.log(t.name)
    console.log(t.value)

    $.ajax({
        url: `/basket/edit/${t.name}/${t.value}/`,
        success: data => {
            $('.basket-list').html(data.result)
        }
    })
}