$(function () {
    //Nav active state functionality

    var currentDir = window.location.pathname;
        console.log(currentDir);

    $(".nav").find(".active").removeClass("active");

    if (currentDir == '/') {
        $('#nav-home').addClass("active");
    } else if (currentDir == '/share') {
        $('#nav-share').addClass("active");
    } else if (currentDir == '/about') {
        $('#nav-about').addClass("active");
    } else if (currentDir == '/stories' || currentDir.indexOf('/stories') !== -1) {
        $('#nav-catalog').addClass("active");
    } else if (currentDir == '/contact') {
        $('#nav-contact').addClass("active");
    }
});