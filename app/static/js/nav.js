$(function () {
    //Nav active state functionality

    var currentDir = window.location.pathname;

    $(".nav").find(".active").removeClass("active");

    if (currentDir == '/') {
        $('#nav-home').addClass("active");
    }
    else if (currentDir == '/share' || currentDir.indexOf('/share') !== -1) {
        $('#nav-share').addClass("active");
    }
    else if (currentDir == '/about') {
        $('#nav-about').addClass("active");
    }
    else if (currentDir == '/stories' || currentDir.indexOf('/stories') !== -1) {
        $('#nav-catalog').addClass("active");
    }
    else if (currentDir == '/contact') {
        $('#nav-contact').addClass("active");
    }
    else if (currentDir == '/subscribe'){
        $('#nav-contact').addClass("active");
    }
});