$('#slider1,#slider2,#slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 4,
            nav: true,
            autoplay: true,
            loop: true,
        }
    }
});

$('.minus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    // console.log(this);
    var eml = this.parentNode.children[2];
    $.ajax({
        url: '/minuscart',
        type: 'GET',
        data: {
            id: id
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;



        }
    });
});

$('.plus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    // console.log(this);
    var eml = this.parentNode.children[2];
    $.ajax({
        url: '/pluscart',
        type: 'GET',
        data: {
            id: id
        },
        success: function(data) {


            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;



        }
    });
});


$('.removecart').click(function() {

    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.parentNode.parentNode.parentNode.parentNode;

    $.ajax({
        url: '/removecart',
        type: 'GET',
        data: {
            id: id
        },
        success: function(data) {
            $('.total_product').html(data.total_product);
            if (data.total_product == 0) {
                var empty_cart = " <p class='alert alert-warning '>Sorry ! You have left no Product in your Cart !!<\p>\
                <div class='text-center'>\
                    <img src='/static/app/images/emptycart.png' class=' ' style='height: 200px; ' alt=''>\
                </div>\ ";
                $('#empty_cart').html(empty_cart);

            }
            eml.remove();
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;



        }
    });
});