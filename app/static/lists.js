// window.addEventListener('DOMContentLoaded', (event) => {
//   var btn_width = document.getElementById('button').offsetWidth;
//   var main_width = document.getElementById('main').offsetWidth;
//   var input_field = document.getElementById('input-text');
//   var input_padding = window.getComputedStyle(input_field).padding.split(" ");
//   var one = parseFloat(input_padding[0])
//   var two = parseFloat(input_padding[1])
//   var padding_total = one + two
//   var input_field_length = main_width - btn_width - padding_total;
//   input_field.style.width = input_field_length + "px";
// });

// function toggle() {
//   var new_list_btn = document.getElementById("new-list-btn");
//   var new_list_box = document.getElementById("new-list-box");
//   if (new_list_box.style.display === "none") {
//     new_list_box.style.display = "block";
//     new_list_btn.style.display = "none";
//   } else {
//     new_list_box.style.display = "none";
//     new_list_btn.style.display = "block";
//   }
// }


// function done(list_id, item_id, checked) {
//   console.log(checked)
//   var url = '/list/' + list_id + '/item/' + item_id;
//   if (checked) {
//     url = url + '/complete';
//   }
//   else {
//     url = url + '/uncomplete';
//   }
//   axios.post(url, {})
//   .then(function (response) {
//     location.reload(true);
//   })
//   .catch(function (error) {
//     console.log(error)
//   });
// }

function done(list_id, item_id, checked) {
  var url = '/list/' + list_id + '/item/' + item_id;
  if (checked) {
    url = url + '/complete';
  }
  else {
    url = url + '/uncomplete';
  }
  console.log(url)
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      location.reload(true);
    }
  }
  xhttp.open("GET", url, true);
  xhttp.setRequestHeader('Content-Type', 'application/json');
  xhttp.send();
}

function confirm_del_toggle(id) {
  var row = document.getElementById(id);
  if (row.hidden == true) {
    row.hidden = false;
  }
  else {
    row.hidden = true;
  }
}
