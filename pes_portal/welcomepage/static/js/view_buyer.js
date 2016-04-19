function removeBuyer(target)
{
	target.parentElement.style.display='none';

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


function dealDone(target)
{
	var myParent = target.parentElement;
	var bookName = myParent.getElementsByTagName('h5')[0].innerHTML.split(':')[1]
	var email = myParent.getElementsByTagName('span')[4].innerHTML.split(':')[1]
	var csrftoken = getCookie('csrftoken');
	var xhttp = new XMLHttpRequest();

  // shows the dialog for 9seconds
  waitingDialog.show('Notifying all the buyers. Please Wait...');
  setTimeout(function () {waitingDialog.hide();}, 9000);

  	xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) 
    {
          // alert("success");
          makeToast("Successsss");
          
          window.location.href="/bookexchange/";
          
        }
      };
      xhttp.open("POST","delete_book/",true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var query_string = "book_name=" + bookName +"&email=" + email;
    console.log(query_string)  
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(query_string);

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
