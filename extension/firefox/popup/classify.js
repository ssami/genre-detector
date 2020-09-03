document.querySelector("#clazz").addEventListener("click", (event) => {
//    console.log("clicked clazz");
    const url = 'http://localhost:8888';
    const Http = new XMLHttpRequest();
    Http.open("POST", url);
    console.log(document.getElementById("words").value);
    Http.send(JSON.stringify({"data":document.getElementById("words").value}));


    Http.onreadystatechange = (e) => {
        var resp = Http.responseText;
        console.log(Http.json);
        var predictions = JSON.parse(Http.json);

        document.getElementById('classification').value = Http.json;
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
