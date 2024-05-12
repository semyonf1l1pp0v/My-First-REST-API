function get_row_by_id() {
    document.getElementById('row_number').onsubmit = function get_element_by_id () {
        this.action = "http://127.0.0.1:5000/api/rows/" + document.getElementById('row_id').value;
        document.getElementById('row_id').value = '';
    }
}

function get_hour_num_of_calls(){
    document.getElementById('hour_number').onsubmit = function() {
        this.action = "http://127.0.0.1:5000/api/hours/" + document.getElementById('hour_id').value;
        document.getElementById('hour_id').value = '';
    }
}

function delete_row_by_id() {
    document.getElementById('delete_row_number').onsubmit = function (event) {
        event.preventDefault();
        var xhr = new XMLHttpRequest();
        var row_num = document.getElementById('delete_row_id').value;
        xhr.open('DELETE', 'http://127.0.0.1:5000/api/rows/' + row_num, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert('Запись успешно удалена');
            } else if (xhr.readyState === 4 && xhr.status === 404) {
                alert('Запись с id ' + row_num + ' не найдена');
            }
        };
        xhr.send();
        document.getElementById('delete_row_id').value = '';
    }
}

