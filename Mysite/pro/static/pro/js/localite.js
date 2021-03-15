  $("#id_wilaya").change(function () {
      var url = $("#RowProduitsForm").attr("data-localité-url");
      var wilayaId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'wilaya_id': wilayaId
        },
        success: function (data) {

            console.log(data);

            $("#id_localité").html(data);
        }
      });

    });