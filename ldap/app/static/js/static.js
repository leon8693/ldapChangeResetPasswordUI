$(document).ready(function(){

    $("#alert-change").hide();
    $("#success-change").hide();

    $("#alert-reset").hide();
    $("#success-reset").hide();

	$("#form-reset").hide();
    $("#changeTab").click(function(){
    	$(this).addClass("active");
    	$("#resetTab").removeClass("active");
    	$("#form-reset").hide();
    	$("#form-change").show();
    });

    $("#resetTab").click(function(){
    	$(this).addClass("active");
    	$("#changeTab").removeClass("active");
    	$("#form-change").hide();
    	$("#form-reset").show();
    });

    $("#button-changepass").click(function (){
        var that = $(this); //to reference the button easier
        that.attr('disabled',true);


        var flag = true;
        var username = $("#inputUsername").val();
        var password = $("#inputPassword").val();
        var newpass = $("#inputNewPassword").val();
        var retypenewpass = $("#inputRetypeNewPassword").val();

        if(username == "" || password == "" || newpass == "" || retypenewpass == "") {
            $("#alert-change > strong").replaceWith( "<strong>All fields must not be empty</strong>" );
            flag = false;
        }
   
        if(retypenewpass != newpass) {
            $("#alert-change > strong").replaceWith( "<strong>New password and retype newpassword is not the same</strong>" );
            flag = false;
        }

        if(newpass.length < 8) {
            $("#alert-change > strong").replaceWith( "<strong>New password must be long than 8 character</strong>" );
           // alert("Hic");
            flag = false;
        }

        if(flag == false) {
            $("#alert-change").show();
        }
        if(flag == true) {
            $("#alert-change").hide();
            var data = {
                "username": username,
                "password": password,
                "newpassword": newpass
            };
        

            $.ajax({
                url: "/change",
                type: "POST",
                contentType: "application/json",
                dataType: "json",
                async: false,
                data: JSON.stringify(data),
                success: function(data) {
                    re = data.re;
                    msg = data.msg;
                    console.log(data.re)
                    console.log(data.msg);
                    if (re == "error") {
                        $("#alert-change > strong").replaceWith(msg);
                        $("#alert-change").show();
                        $("#success-change").hide();
                    }
                    if (re == "success") {
                        $("#success-change > strong").replaceWith("Your password changed success");
                        $("#success-change").show();
                        $("#alert-change").hide();
                    }
                    
                    that.attr('disabled',false);
                }
            });

            //     error: function(e) {
            //         //called when there is an error
            //         console.log(e.message);
            //     }
            // });

        } 
        
    });


    $("#ResetSubmit").click(function () {

        var that = $(this); //to reference the button easier
        that.attr('disabled',true);


        var flag = true;
        var username = $("#inputResetUsername").val();
        if(username == "") {
            $("#alert-reset > strong").replaceWith( "<strong>All fields must not be empty</strong>" );
            flag = false;
        }

        if(flag == false) {
            $("#alert-reset").show();
        } else {
            var data = {
                "username": username
            };
        
            
            $.ajax({
                url: "/reset",
                type: "POST",
                contentType: "application/json",
                dataType: "json",
                async: false,
                data: JSON.stringify(data),
                success: function(data) {
                    re = data.re;
                    msg = data.msg;
                    console.log(data);
                    if (re == "error") {
                        $("#alert-reset > strong").replaceWith(msg);
                        $("#alert-reset").show();
                        $("#success-reset").hide();
                    }
                    if (re == "success") {
                        $("#success-reset > strong").replaceWith("Please check your email to confirm your request");
                        $("#success-reset").show();
                        $("#alert-reset").hide();
                    }
                    that.attr('disabled',false);

                }
            });
        }


    });

});
