$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            try {
                reader.onload = function (e) {
                    $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                    $('#imagePreview').hide();
                    $('#imagePreview').fadeIn(650);
                }
                reader.readAsDataURL(input.files[0]);
            } catch (error) {
                alert("Error reading file. Please try again.");
                console.error("FileReader error:", error);
            }
        }
    }

    $("#imageUpload").change(function () {
        var file = this.files[0];
        var fileType = file.type;
        var validTypes = ["image/jpeg", "image/png", "image/jpg"];
        if (!validTypes.includes(fileType)) {
            alert("Invalid file type. Please upload a JPG or PNG image.");
            $(this).val('');
            return;
        }
        if (file.size > 2 * 1024 * 1024) { // Limit size to 2MB
            alert("File size too large. Please upload an image less than 2MB.");
            $(this).val('');
            return;
        }
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        if ($('#upload-file').length === 0) {
            alert("Form not found!");
            return;
        }
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict?_=' + new Date().getTime(),
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },
            error: function (xhr, status, error) {
                $('.loader').hide();
                alert("An error occurred: " + error);
                $('#btn-predict').show();
                console.error('Error:', error);
            }
        });
    });

});
