function init()
{
	saleTable = document.getElementById("table");
	saleTable.addEventListener("click", make_ajax_for_borrow,false);

  searchBar = document.getElementById("searchbar");
  searchbar.addEventListener("change",make_ajax_for_search,false);
}

function make_ajax_for_search(event)
{
    console.log(searchbar.value);
     var xhttp = new XMLHttpRequest();

      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) 
        {
          // alert("success");
          makeToast("Successsss");
          console.log(xhttp.responseText);

          rePopulateTable(xhttp.responseText);
        }
      };
      xhttp.open("GET","search_book?book_name="+searchbar.value,true);
    // xhttp.setRequestHeader("X-CSRFToken", csrftoken);
      xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xhttp.send();
      

}

function rePopulateTable(resp)
{
  var obj = JSON.parse(resp);
  var rows = document.getElementsByTagName('tbody')[0];
  var newData = "";
  for(var i =0;i<obj.data.length;i++)
    newData += "<tr><td>" + obj.data[i].usn + "</td><td>" + obj.data[i].book_name + "</td>" + '<td><button class="w3-btn w3-ripple w3-green">Borrow</button></td></tr>';
  rows.innerHTML  = newData;
}

function make_ajax_for_borrow(event)
{
	if( event.target != event.currentTarget)
	{
		var tr = (event.target.parentNode.parentNode);
		// console.log(tr.childNodes[1].innerHTML);
		// console.log(tr.childNodes[3].innerHTML);

		var seller_id = tr.childNodes[1].innerHTML
		var book_name = tr.childNodes[3].innerHTML

		var csrftoken = getCookie('csrftoken');
		// console.log(csrftoken);


		 var xhttp = new XMLHttpRequest();

  		xhttp.onreadystatechange = function() {
	    	if (xhttp.readyState == 4 && xhttp.status == 200) 
	    	{
          // alert("success");
	    		makeToast("Success");
	    	}
    	};
    	xhttp.open("POST","buy/",true);
		xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    	var query_string = "book_name=" + book_name + "&seller_id=" + seller_id;  
    	xhttp.send(query_string);
    	event.target.disabled=true;
	}
	event.stopPropagation();
}

function makeToast(msg)
{

  toastr["success"]("",msg);

toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}
}

function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = cookies[i];
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
