const loading = document.querySelector("#loading");
const content = document.querySelector("#content");
const inputimage = document.querySelector("#role-form");

console.log(inputimage);


function modal(){
    $('.modal').modal('show');
 }

inputimage.addEventListener('submit', (e) => {
    modal();
});

