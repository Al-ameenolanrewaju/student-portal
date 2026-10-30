$(document).ready(function() {

    // ===== LGA Dropdown based on selected State =====
    $('#state').change(function() {
        let state = $(this).val();
        let lgaSelect = $('#lga');

        // Reset LGA dropdown
        lgaSelect.html('');
        lgaSelect.prop('disabled', true);

        if (state) {
            $.ajax({
                url: '/get_lgas',
                type: 'GET',
                data: { state: state },
                success: function(data) {
                    if (data.length > 0) {
                        lgaSelect.prop('disabled', false);
                        lgaSelect.append('<option value="">--Select LGA--</option>');
                        $.each(data, function(index, lga) {
                            lgaSelect.append(
                                $('<option></option>').val(lga).text(lga)
                            );
                        });
                    }
                }
            });
        }
    });

    // ===== Dynamic AJAX Search for Students =====
    function fetch_students() {
        let name = $('#search_name').val();
        let admission = $('#search_admission').val();
        let gender = $('#search_gender').val();
        let jamb = $('#search_jamb').val();

        $.ajax({
            url: '/search_students',
            method: 'GET',
            data: {
                search_name: name,
                search_admission: admission,
                search_gender: gender,
                search_jamb: jamb
            },
            success: function(response){
                let tbody = '';
                if(response.length > 0){
                    $('#no_records_msg').hide(); // hide "No records" message
                    $.each(response, function(i, student){
                        tbody += `<tr>
                            <td>${student.first_name} ${student.last_name}</td>
                            <td>${student.email}</td>
                            <td><a href="/profile/${student.id}" class="btn btn-info btn-sm">View</a></td>
                        </tr>`;
                    });
                } else {
                    tbody = '';
                    $('#no_records_msg').show(); // show "No records" message
                }
                $('#students_table tbody').html(tbody);
            }
        });
    }

    // Trigger search on button click
    $('#search_btn').click(function(e){
        e.preventDefault();
        fetch_students();
    });

    // Trigger search on typing or selection change
    $('#search_name, #search_admission, #search_gender, #search_jamb').on('keyup change', function(){
        fetch_students();
    });

});