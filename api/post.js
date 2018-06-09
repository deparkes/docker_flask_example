xhr = new XMLHttpRequest();
var url = "http://127.0.0.1:5000/api/add_message";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-type", "application/json");
xhr.onreadystatechange = function () { 
    if (xhr.readyState == 4 && xhr.status == 200) {
        var json = JSON.parse(xhr.responseText);
        alert(json.age + ", " + json.password)
    }
}
var data = JSON.stringify({"age":"21","password":"xyz"});
xhr.send(data);