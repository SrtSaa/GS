if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
} else {
    ready();
}


var arr = JSON.parse(localStorage.getItem("ids"));
var qty = JSON.parse(localStorage.getItem("qty"));



function ready() {
    var items = document.getElementsByClassName('quantity');
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        item.value = qty[i];
    }

    updateCartTotal();
    var removeButtons = document.getElementsByClassName('removeItem');
    for (var i = 0; i < removeButtons.length; i++) {
        var button = removeButtons[i];
        button.addEventListener('click', removeItem);
    }
}


function removeItem(event) {
    var button = event.target;
    button.parentElement.parentElement.remove();
    updateCartTotal();
}


function updateCartTotal() {
    var cartRows = document.getElementsByClassName('item');
    var total = 0;
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i];
        var priceElement = cartRow.getElementsByClassName('price')[0];
        var quantityElement = cartRow.getElementsByClassName('quantity')[0];
        var price = parseFloat(priceElement.innerText);
        var quantity = quantityElement.value;
        qty[i] = quantity;
        total = total + (price * quantity);
    }
    total = Math.round(total * 100) / 100;
    if (arr.length == 0) {
        var ndiv = document.createElement('div');
        ndiv.className = "container3";
        var ndiv2 = document.createElement('div');
        ndiv2.className = "box2";
        ndiv2.style = "text-align: center; color: red";
        var h = document.createElement('h3');
        var s = document.createElement('strong');
        s.innerText = 'Cart is Empty';
        h.appendChild(s);
        ndiv2.appendChild(h);
        ndiv.appendChild(ndiv2);

        document.getElementById('middle').innerHTML = '';
        document.getElementById('middle').appendChild(ndiv);
    } else {
        document.getElementsByClassName('totalPrice')[0].innerText = total;
    }
}


function purchase() {
    if (confirm("Do you want to purchase the item?") == true) {
        alert('Thank you for your purchase! Visit again!!');
        document.getElementById("ids").value = arr;
        document.getElementById("qty").value = qty;
        clearStorage();
        return true;
    }
    return false;
}


function deleteItem(item) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] == item) {
            arr.splice(i, 1);
        }
    }
}


function addtoStorage() {
    localStorage.setItem('ids', JSON.stringify(arr));
    localStorage.setItem('qty', JSON.stringify(qty));
}


function clearStorage() {
    localStorage.removeItem('ids');
    localStorage.removeItem('qty');
}


