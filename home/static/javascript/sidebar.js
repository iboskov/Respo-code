$("#sidebarToggle").on("click", function(){
    $(".sidebar").toggleClass("sidebarCollapsed");
    if($("#sidebarToggle").find(".leftA").length==1){
        $("#sidebarToggle").empty();
        $("#sidebarToggle").append('<span class="rightA"><i class="far fa-arrow-alt-circle-right fa-2x"></i></span>');
    }else if($("#sidebarToggle").find(".rightA").length==1){
        $("#sidebarToggle").empty();
        $("#sidebarToggle").append('<span class="leftA"><i class="far fa-arrow-alt-circle-left fa-2x"></i></span>');
    }
});

$("#sidebarToggleTop").on("click", function(){
    $(".sidebar").toggleClass("d-none");
});
