$('#send-form').submit(function (e) {
	e.preventDefault();
	$.ajax({
		url: '/send',
		dataType: 'json',
		method: 'POST',
		success: function (response) {
			if (response.is_malicious)
				alert("An anomalous message has been blocked, see capture list for details.")
			else
				$('#dashboard').prepend(response.data);
		},
	})
});