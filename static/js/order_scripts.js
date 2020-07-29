"use strict"
let quantity, price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
let quantityArr = [];
let priceArr = [];
let $orderTotalQuantityDom;

let totalForms;
let orderTotalQuantity;
let orderTotalCost;
let $orderForm;

function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
        quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = quantity;
        priceArr[i] = (price) ? price : 0;
    }
}

function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
    deltaCost = orderitemPrice * deltaQuantity;
    orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
    orderTotalQuantity = orderTotalQuantity + deltaQuantity;

    $('.order_total_cost').html(orderTotalCost.toString());
    $orderTotalQuantityDom.html(orderTotalQuantity.toString());
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type = "number"]').name;
    orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderitemNum]
    orderSummaryUpdate(priceArr[orderitemNum],deltaQuantity);
}

function updateTotalQuantity() {
    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $orderTotalQuantityDom.html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
}

window.onload = function () {
    $orderTotalQuantityDom = $('.order_totalquantity');
    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    orderTotalQuantity = parseInt($orderTotalQuantityDom.text()) || 0;
    orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    $orderForm = $('.order_form');

    parseOrderForm()

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm.on('change', 'input[type = "number"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''))
        if (priceArr[orderitemNum]) {
            orderitemQuantity = parseInt(event.target.value);
            deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
            quantityArr[orderitemNum] = orderitemQuantity;
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type = "checkbox"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''))
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderitemNum];
        } else {
            deltaQuantity = quantityArr[orderitemNum];
        }
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

}



