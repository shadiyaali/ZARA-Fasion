$(document).ready(function () {
    $('#payWithRazorpay').click(function (e) { 
        e.preventDefault();
        console.log('im here') 



        var first_name = $("[name='first_name']").val();
        var last_name = $("[name='last_name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (first_name == "" || last_name == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || pincode == "")
        {
             
             
            swal("alert", "All fields are mandatory", "error");
            return false;
        }
       else{ 
        
        $.ajax({
            method: "GET",
            url: "/orders/proceed-to-pay/",
            contentType: 'application/json',
            success: function (response) {
                console.log(412243)
                console.log(response.total_price);
                var options = {
                    "key": "rzp_test_uVqaAuxQYg0gWu", // Enter the Key ID generated from the Dashboard
                    "amount": response.total_price*100,//response.total_price *100 , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Zara",
                    "description": "Thank you",
                    "image": "https://example.com/your_logo",
                    // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (responseb){
                        // alert(responseb.razorpay_payment_id);
                        // alert(response.razorpay_order_id);
                        // alert(responseb.razorpay_payment_id);
                        data ={ 
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "phone": phone,
                            "address": address,
                            "city": city,
                            "state": state,
                            "country": country,
                            "pincode": pincode,
                            "payment_mode":"Paid by Razorpay",
                            "payment_id": responseb.razorpay_payment_id,
                            csrfmiddlewaretoken : token

                        }
                    
                        $.ajax({
                            method: "POST",
                            url: "/orders/placeorder/",
                            data: data,
                            success: function (responsec) {
                          
                                swal(
                                   "Congratulations!",responsec.status,"success"
                                  ).then(value => { 
                                    window.location.href ='/orders/order-complete/'+'?payment_id='+data.payment_id
                                  })
                                
                            }
                        });
                    },
                    "prefill": {
                        "name": first_name +" "+last_name,
                        "email": email,
                        "contact": phone
                    },
                    "notes": {
                        "address": "zara shopping site"
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
        
                
            }
        }); 
        
          }

       
        
        
    });
}); 