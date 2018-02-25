$(document).ready(function() {
    var coinData = $.getJSON( "https://coincap.io/front", function() {
        // console.log(coinData.responseJSON);
        for(i = 0; i < 100; i++) {
            if(coinData.responseJSON[i].perc > 0) {
                $("#ticker").append("<p class='positive'>" + coinData.responseJSON[i].short + "/USD: " + coinData.responseJSON[i].price + "</p>");
                $("#ticker").append("<p>|</p>");
            } else {
                $("#ticker").append("<p class='negative'>" + coinData.responseJSON[i].short + "/USD: " + coinData.responseJSON[i].price + "</p>");
                $("#ticker").append("<p>|</p>");
            }
        }
    });
    
    var individualCoinData = $.getJSON( "https://coincap.io/page/" + $("#coinName1").text(), function() {
        $(".coin_price_container").append("<p>$" + individualCoinData.responseJSON.price + "</p>");
        if(individualCoinData.responseJSON.cap24hrChange > 0) {
            $(".coin_price_container").append("<div class='coin_price_percentage_container coin_percentage_change_green'></div>");
        } else {
            $(".coin_price_container").append("<div class='coin_price_percentage_container coin_percentage_change_red'></div>");
        }
        $(".coin_price_percentage_container").append("<p>" + individualCoinData.responseJSON.cap24hrChange + "%</p>");
        $(".coin_mktcap_container").append("<p>$" + individualCoinData.responseJSON.market_cap + "</p>");
        $(".coin_volume_container").append("<p>$" + individualCoinData.responseJSON.volume + "</p>");
    });
    
    var individualCoinData2 = $.getJSON( "https://coincap.io/page/" + $("#coinName2").text(), function() {
        $(".coin_price_container2").append("<p>$" + individualCoinData2.responseJSON.price + "</p>");
        if(individualCoinData2.responseJSON.cap24hrChange > 0) {
            $(".coin_price_container2").append("<div class='coin_price_percentage_container coin_percentage_change_green'></div>");
        } else {
            $(".coin_price_container2").append("<div class='coin_price_percentage_container coin_percentage_change_red'></div>");
        }
        $(".coin_price_percentage_container2").append("<p>" + individualCoinData2.responseJSON.cap24hrChange + "%</p>");
        $(".coin_mktcap_container2").append("<p>$" + individualCoinData2.responseJSON.market_cap + "</p>");
        $(".coin_volume_container2").append("<p>$" + individualCoinData2.responseJSON.volume + "</p>");
    });
});


$(window).scroll(function() {
    if($(window).scrollTop() >= 28) {
        $('#mainNavBar').css("position", "fixed");
        $('.ticker-wrap').css("margin-bottom", "82px")
    } else {
        $('#mainNavBar').css("position", "static");
        $('.ticker-wrap').css("margin-bottom", "0")
    }
});

$(".ico_button1").click(function(){
    if($(this).hasClass("ico_button_active") == false) {
        $(".ico_button1").removeClass("ico_button_active");
        $(this).addClass("ico_button_active");
        $("#ACTIVE-PRE").hide();
        $("#UPCOMING-PRE").hide();
        $("#CONCLUDED-PRE").hide();
        $("#ACTIVE-POST").hide();
        $("#UPCOMING-POST").hide();
        $("#CONCLUDED-POST").hide();
        if($(this).attr('id') == "icoButtonPost") {
            if($("#icoButtonActive").hasClass("ico_button_active")) {
                $("#ACTIVE-POST").css("display", "flex");
            } else if($("#icoButtonUpcoming").hasClass("ico_button_active")) {
                $("#UPCOMING-POST").css("display", "flex");
            } else {
                $("#CONCLUDED-POST").css("display", "flex");
            }
        } else {
            if($("#icoButtonActive").hasClass("ico_button_active")) {
                $("#ACTIVE-PRE").css("display", "flex");
            } else if($("#icoButtonUpcoming").hasClass("ico_button_active")) {
                $("#UPCOMING-PRE").css("display", "flex");
            } else {
                $("#CONCLUDED-PRE").css("display", "flex");
            }
        }
    }
});

$(".ico_button2").click(function(){
    if($(this).hasClass("ico_button_active") == false) {
        $(".ico_button2").removeClass("ico_button_active");
        $(this).addClass("ico_button_active");
        $("#ACTIVE-PRE").hide();
        $("#UPCOMING-PRE").hide();
        $("#CONCLUDED-PRE").hide();
        $("#ACTIVE-POST").hide();
        $("#UPCOMING-POST").hide();
        $("#CONCLUDED-POST").hide();
        if($("#icoButtonPre").hasClass("ico_button_active") == false) {
            if($(this).attr('id') == "icoButtonActive") {
                $("#ACTIVE-POST").css("display", "flex");
            } else if($(this).attr('id') == "icoButtonUpcoming") {
                $("#UPCOMING-POST").css("display", "flex");
            } else {
                $("#CONCLUDED-POST").css("display", "flex");
            }
        } else {
            if($(this).attr('id') == "icoButtonActive") {
                $("#ACTIVE-PRE").css("display", "flex");
            } else if($(this).attr('id') == "icoButtonUpcoming") {
                $("#UPCOMING-PRE").css("display", "flex");
            } else {
                $("#CONCLUDED-PRE").css("display", "flex");
            }
        }
    }
});