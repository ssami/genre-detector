document.querySelector("#clazz").addEventListener("click", (event) => {
//    console.log("clicked clazz");
    const url = 'http://localhost:8888';
    const Http = new XMLHttpRequest();
    Http.open("POST", url);
    Http.send(JSON.stringify({"data":"sherlock holmes is my favorite detective fiction"}));

    Http.onreadystatechange = (e) => {
      console.log(Http.responseText)
    }
});


//$(document).ready(function() {
////    const url = 'http://localhost:8888';
////    $.ajax({
////        url: url,
////        type: "GET",
////        success: function(result) {
////            console.log(result)
////        }
////        error: function(err) {
////            console.log(`Error: ${err}`)
////        }
////    })
//    $(".clazz").click(function() {
//        console.log("clicked clazz");
//    })
//
//})
