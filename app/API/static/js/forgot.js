$(document).ready(function () {
    $(document).on("click", "#nextforget", function () {
        if($(".must").val() != ""){
            if($("#forgotpassword").val() == $("#forgotpassword-again").val()){
                data_password = {
                    userId:$("#forgotid").val(),
                    userPassword:$("#forgotpassword").val()
                }
                $.ajax({
                    type: "POST",
                    url: "http://163.18.42.222:4000/Fiestadb/Account/changePassword",
                    data: JSON.stringify(data_password),
                    contentType: "application/json",
                    datatype: JSON,
                    async:false,
                    success: function (response) {

                        $(".start").hide()
                        $(".finish").css("display", "flex")
                    }
                });

            }
        }
    });
    $(document).on('click', "#sendforgot", function () {
        location.href = "http://fiesta.nkust.edu.tw/login"
    });
});