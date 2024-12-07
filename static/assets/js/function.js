console.log("hello");
const monthsNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();
    let dt = new Date();
    let time =dt.getDate() +' '+ monthsNames[dt.getUTCMonth()] + ', ' + dt.getFullYear();
    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response){
            console.log("Comment saved to DB..");

            if (response.bool ==true){
                $("#review-res").html("Review added successfully.")   
                $(".hide-comment-form").hide()
                $(".add-review").hide()


                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="data:image/jpeg;base64,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" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">' + response.context.user +'</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">'+ time +'</span>'
                    _html += '</div>'

                    

                    for (let i = 1; i<= response.context.rating; i++) {
                        _html += '<i class="fas fa-star text-warning"></i>';
                    }

                    _html += '</div>'
                    _html += '<p class="mb-10">'+ response.context.review +'</p>'

                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".comment-list").prepend(_html)
                }
                
        }
        
        
        
    })
})
    

$(document).ready(function(){
    $(".filter-checkbox,#price-filter-btn").on("click",function(){
        console.log("A checkbox has been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val();
            let filter_key =$(this).data("filter");

            //console.log("Filter value is " + filter_value);
            //console.log("Filter key is " + filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
                return element.value
            })


        })
        console.log("Filter Object is:",filter_object);
        $.ajax({
            url: "/filter-products/",
            data: filter_object,
            dataType: "json",
            beforeSend: function(){
                console.log("Sending Data...");
            },
            success: function(response){
                console.log(response);
                console.log("Data filtered");
                $("#filtered-product").html(response.data);
              
            }
        })    
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        console.log("Current Price is:", current_price);
        console.log("Min Price is:", min_price);
        console.log("Max Price is:", max_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            console.log("Price is out of range");

            min_price = Math.round(min_price * 100)/100
            max_price = Math.round(max_price * 100)/100

            //console.log("Min Price is:",min_Price);
            //console.log("Max Price is:",max_Price);

            alert("Price must be between KSh." +min_price +" and KSh."+ max_price);
            $(this).val(min_price);
            $("#range").val(min);


            $(this).focus();

            return false;
            
        
        }
    })

    $(".add-to-cart-btn").on("click",function(){
        let this_val = $(this);
        let index = this_val.attr("data-index");
    
    
        let quantity = $(".product-quantity-"+index).val();
        let product_title = $(".product-title-"+index).val();
        let product_id =$(".product-id-"+index).val();
        let product_price = $(".current-product-price-"+index).text();
        let product_pid = $(".product-pid-"+index).val();
        let product_image = $(".product-image-"+index).val();
            
    
    
        console.log("Quantity is:", quantity);
        console.log("Product Title is:", product_title);
        console.log("Product Price is:", product_price);
        console.log("Product ID is:", product_id);
        console.log("Product PID is:", product_pid);
        console.log("Product IMAGE is:", product_image);
        console.log("Product INDEX is:", index);
        console.log("Current Element:", this_val);
    
        $.ajax({
            url: "/add-to-cart",
            data: {
                "id": product_id,
                "pid": product_pid,
                "image": product_image,
                "qty": quantity,
                "title": product_title,
                "price": product_price
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding product to cart");
    
            },
            success: function(response){
                this_val.html("&#x2714;");
                console.log("Product added to cart");
                $(".cart-items-count").text(response.totalcartitems);
            }
        })
    })
    
    $(document).on("click",".delete-product",function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product ID is:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data)
            }
        })

        
    })
    $(document).on("click",".update-product",function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()

    
        console.log("Product ID is:", product_id);
        console.log("Product QTY is:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data)
            }
        })

        
    })

    //adding to wishlist
    $(document).on("click",".add-to-wishlist",function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product ID is:", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding product to wishlist");
            },
            success: function(response){
                this_val.html("&#x2714;")
                if (response.bool === true){
                    console.log("Added to wishlist....");
                }
                
            }
            
        })
        
    })

    
})



//add to cart functionality


// add to cart functionality
// $(".add-to-cart-btn").on("click",function(){
//     let quantity = $("#product-quantity").val();
//     let product_title = $(".product-title").val();
//     let product_id =$(".product-id").val();
//     let product_price = $("#current-product-price").text();
//     let this_val = $(this);


//     console.log("Quantity is:", quantity);
//     console.log("Product Title is:", product_title);
//     console.log("Product ID is:", product_id);
//     console.log("Product Price is:", product_price);
//     console.log("Current Element:", this_val);

//     $.ajax({
//         url: "/add-to-cart",
//         data: {
//             "id": product_id,
//             "qty": quantity,
//             "title": product_title,
//             "price": product_price
//         },
//         dataType: "json",
//         beforeSend: function(){
//             console.log("Adding product to cart");

//         },
//         success: function(response){
//             this_val.html("Item added to cart");
//             console.log("Product added to cart");
//             $(".cart-items-count").text(response.totalcartitems);
//         }
//     })
// })

