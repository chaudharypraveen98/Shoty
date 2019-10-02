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
  document.getElementById("mySidenav").style.width = "330px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}


$(document).ready(function(){
  $(".navbar-toggler-icon").click(function(){
    $(".sidenav").addClass("padding-50");
  });
});