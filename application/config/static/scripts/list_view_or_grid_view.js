// Get the elements with class="column"
//var elements = document.getElementsByClassName("col-md-10");
var elements = document.getElementsByClassName("card-container");

// Declare a loop variable
var i;

// List View
function ListView() {
  for (i = 0; i < elements.length; i++) {
    elements[i].style.WebkitColumnCount = 1;
  }
}

// Grid View
function GridView() {
  for (i = 0; i < elements.length; i++) {
    elements[i].style.WebkitColumnCount = 2;
  }
}

/* Optional: Add active class to the current button (highlight it) */
var container = document.getElementById("btnContainer");
var btns = container.getElementsByClassName("btn");

for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}