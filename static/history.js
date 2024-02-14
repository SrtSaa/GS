if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', updateTotal);
} else {
    updateTotal();
}

function updateTotal() {
    var cartRows = document.getElementsByClassName('table');
    for (var i = 0; i < cartRows.length; i++) {
        var total = 0;
        var cartRow = cartRows[i];
        var priceElement = cartRow.getElementsByClassName('price');
        for (var j = 0; j < priceElement.length; j++) {
            var price = parseFloat(priceElement[j].innerText);
            total = total + price;
        }
        total = Math.round(total * 100) / 100;
        cartRow.getElementsByClassName('totalPrice')[0].innerText = total;
    }
}
