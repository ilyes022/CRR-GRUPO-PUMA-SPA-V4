$("#id_région").change(function () {
      var url = $("#RowProduitsForm").attr("data-distributeur-url");
      var régionId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'région_id': régionId
        },
        success: function (data) {

            console.log(data);

            $("#id_distributeur").html(data);
        }
      });

    });