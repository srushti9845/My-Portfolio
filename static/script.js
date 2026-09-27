// Dark / Light mode

const themeButton =
    document.getElementById("themeButton");

themeButton.addEventListener("click", function () {

    document.body.classList.toggle("dark");

    if (document.body.classList.contains("dark")) {

        themeButton.textContent = "☀️";

        localStorage.setItem(
            "theme",
            "dark"
        );

    } else {

        themeButton.textContent = "🌙";

        localStorage.setItem(
            "theme",
            "light"
        );
    }

});


// Remember selected theme

const savedTheme =
    localStorage.getItem("theme");

if (savedTheme === "dark") {

    document.body.classList.add("dark");

    themeButton.textContent = "☀️";

}


// Current year

document.getElementById("year").textContent =
    new Date().getFullYear();