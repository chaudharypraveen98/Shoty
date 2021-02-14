//navbar breakage
$(document).on("scroll", function(){
	if
  ($(document).scrollTop() > 86){
	  $("#banner").addClass("shrink");
	}
	else
	{
	  $("#banner").removeClass("shrink");
	}
});

//Preloader
var overlay = document.getElementById("loader");

window.addEventListener('load', function(){
  overlay.style.display = 'none';
})

//right side navigation
function openNav() {
  var element = document.getElementById("mySidenav");
  element.style.width = "330px";
  element.classList.add("padding-50");
}

function closeNav() {
  var element = document.getElementById("mySidenav");
  element.style.width = "0px";
  element.classList.remove("padding-50");

}


$(document).ready(function(){
  $(".navbar-toggler-icon").click(function(){
    $(".sidenav").addClass("padding-50");
  });
});