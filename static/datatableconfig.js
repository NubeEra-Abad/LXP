$(document).ready(function () {
    $('#dev-table').DataTable({        
      'dom': 'Rlfrtip',
      'colReorder': {
          'allowReorder': false
      },
      // 'autoWidth': true,
      "lengthMenu": [ 5, 10, 20, 50, 100,"All" ],
      "pageLength": 10,
      "search": {
        "search": ""
      }
    });
  });