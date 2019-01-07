// Get references to page elements
const loginForm = document.getElementById("formLoginId");

// Set event listener
$("#btnLoginSubmit").on("click", function () {
    loginError = document.getElementById("loginErrorMessageId");

    loader.classList.add("is-active");

    if (loginError) {
        loginError.classList.add("hidden");
    }

    $.ajax({
			url: '/validateLogin',
			data: $(loginForm).serialize(),
			type: 'POST',
			success: function(data) {
                if(data.result) {
                    window.location.href = data.redirect;
                } else {
                    loginError.classList.remove("hidden");
                    loader.classList.remove("is-active");
                }
			},
			error: function(error) {
				console.log('Ajax Error');
			    console.log(error);

			    loginError.classList.remove("hidden");
			    loader.classList.remove("is-active");
			}
		});
});



