

function getLostDogs(){
    alert("in here!");
    $.get(
        "/lostdog",
        {zipcode : "{{ zipcode }}", breed : '{{ breed }}'},
        function(data) {
            alert(data);
        }
    );
}