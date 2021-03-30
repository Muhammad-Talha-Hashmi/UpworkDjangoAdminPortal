function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var EditableTable = function () {

    return {

        //main function to initiate the module
        init: function () {
            function restoreRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);

                for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                    oTable.fnUpdate(aData[i], nRow, i, false);
                }

                oTable.fnDraw();
            }

            function editRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                for (i = 0; i < 5; i++) {
                    jqTds[i].innerHTML = '<input type="text" class="form-control small" value="' + aData[i] + '">';
                }

                jqTds[5].innerHTML = '<a class="edit" href="">Save</a><br><a class="cancel" href="">Cancel</a>';
            }

            function saveRow(oTable, nRow) {
                var jqInputs = $('input', nRow);
                for (i = 0; i < 5; i++) {
                    oTable.fnUpdate(jqInputs[i].value, nRow, i, false);
                }
                oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 5, false);
                oTable.fnDraw();
            }



            var oTable = $('#editable-sample').dataTable({
                "aLengthMenu": [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"] // change per page values here
                ],
                // set the initial value
                "iDisplayLength": 5,
                "sDom": "<'row'<'col-lg-6'l><'col-lg-6'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>",
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "_MENU_ records per page",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
                "aoColumnDefs": [{
                    'bSortable': false,
                    'aTargets': [0]
                }
                ]
            });

            jQuery('#editable-sample_wrapper .dataTables_filter input').addClass("form-control medium"); // modify table search input
            jQuery('#editable-sample_wrapper .dataTables_length select').addClass("form-control xsmall"); // modify table per page dropdown

            var nEditing = null;

            $('#editable-sample_new').click(function (e) {
                e.preventDefault();
                var row = ['', '','', '', 'Waiting','<a class="edit" data-mode="new" href="">Save</a><br><a class="cancel" data-mode="new" href="">Cancel</a>', ''];
                console.log(row);
                var aiNew = oTable.fnAddData(row);
                var nRow = oTable.fnGetNodes(aiNew[0]);

                var jqTds = $('>td', nRow);
                for (i = 0; i < 5; i++) {
                    if (jqTds[i].innerText == '') {
                        console.log(jqTds[i].innerText);
                        jqTds[i].innerHTML = '<input type="text" class="form-control small" value="">';
                    } else {
                        jqTds[i].innerHTML = '<input type="text" class="form-control small" value="' + jqTds[i].innerText + '">';

                    }
                }

                nEditing = nRow;
            });

            $('#editable-sample a.delete').live('click', function (e) {
                e.preventDefault();

                if (confirm("Are you sure to delete this row ?") == false) {
                    return;
                }

                var nRow = $(this).parents('tr')[0];
                console.log(nRow);
                oTable.fnDeleteRow(nRow);
                console.log( nRow.dataset.journal);
                data = {
                    "type": "delete",
                    "journal_name": nRow.dataset.journal
                }
                $.ajax({
                    "url": "/journals/management",
                    "type": "POST",
                    "contentType": 'application/json; charset=utf-8',
                    "beforeSend": function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    "data": JSON.stringify(data),
                    "success": function (resp) {
                        alert("Deleted!");
                    }
                });
            });

            $('#editable-sample a.cancel').live('click', function (e) {
                e.preventDefault();
                console.log($(this));
                if ($(this).attr("data-mode") == "new") {
                    var nRow = $(this).parents('tr')[0];
                    console.log(nRow);
                    oTable.fnDeleteRow(nRow);
                } else {
                    restoreRow(oTable, nEditing);
                    nEditing = null;
                }
            });

            $('#editable-sample a.edit').live('click', function (e) {
                e.preventDefault();

                /* Get the row as a parent of the link that was clicked on */
                var nRow = $(this).parents('tr')[0];

                if ($(this).attr("data-mode") == "new") {
                    // Create a new user
                    saveRow(oTable, nEditing);

                    var jqTds = $('>td', nRow);
                    journal = {
                        "journal_name": jqTds[0].innerText,
                        "publisher": jqTds[1].innerText,
                        "main_category": jqTds[2].innerText,
                        "quartile_rank": jqTds[3].innerText,
                        "status": jqTds[4].innerText,
                    }
                    data = {
                        "type": "create",
                        "data": journal
                    }
                    $.ajax({
                        "url": "/journals/management",
                        "type": "POST",
                        "contentType": 'application/json; charset=utf-8',
                        "beforeSend": function (request) {
                            request.setRequestHeader("X-CSRFToken", csrftoken);
                        },
                        "data": JSON.stringify(data),
                        "success": function (resp) {
                            alert("Created!");
                        },
                        "error": function (XMLHttpRequest, textStatus, errorThrown) {
                            oTable.fnDeleteRow(nRow);
                            alert("Error saving.." + XMLHttpRequest.responseText);
                        }
                    });
                    nEditing = null;
                }
                else if (nEditing !== null && nEditing != nRow) {
                    /* Currently editing - but not this row - restore the old before continuing to edit mode */
                    restoreRow(oTable, nEditing);
                    editRow(oTable, nRow);
                    nEditing = nRow;
                } else if (nEditing == nRow && this.innerHTML == "Save") {
                    /* Editing this row and want to save it */
                    saveRow(oTable, nEditing);
                    var jqTds = $('>td', nRow);
                    journal = {
                        "journal_name": jqTds[0].innerText,
                        "publisher": jqTds[1].innerText,
                        "main_category": jqTds[2].innerText,
                        "quartile_rank": jqTds[3].innerText,
                        "status": jqTds[4].innerText,
                    }
                    data = {
                        "type": "update",
                        "journal_name": nRow.dataset.journal,
                        "data": journal
                    }
                    $.ajax({
                        "url": "/journals/management",
                        "type": "POST",
                        "contentType": 'application/json; charset=utf-8',
                        "beforeSend": function (request) {
                            request.setRequestHeader("X-CSRFToken", csrftoken);
                        },
                        "data": JSON.stringify(data),
                        "success": function (resp) {
                            alert("Updated!");
                        },
                        "error": function (XMLHttpRequest, textStatus, errorThrown) {
                            oTable.fnDeleteRow(nRow);
                            alert("Error saving.." + XMLHttpRequest.responseText);
                        }
                    });
                    nEditing = null;
                } else {
                    /* No edit in progress - let's start one */
                    editRow(oTable, nRow);
                    nEditing = nRow;
                }
            });
        }

    };

}();