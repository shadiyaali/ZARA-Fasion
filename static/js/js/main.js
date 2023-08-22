
(function ($) {
    "use strict";

    // ADD TO WISHLIST

    $('.plus-wishlist').click(function() { 

        var id=$(this).attr("pid").toString();
        console.log(id)
        $.ajax({
            type:"GET",
            url:"/wishlist/add_wishlist/",
            data:{
                prod_id:id
            },
            success:function(data) {
                alert(data.message)
                
            }
        })
        
    });


    $('.minus-wishlist').click(function() { 
        var id=$(this).attr("pid").toString();
        $.ajax({
            type:"GET",
            url:"/wishlist/remove_wishlist",
            data:{
                prod_id:id
            },
            success:function(data) {
                alert("wish list removed")
                
            }
        })
        
    });




})(jQuery);