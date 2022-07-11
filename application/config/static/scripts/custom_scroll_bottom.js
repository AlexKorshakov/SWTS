$(function(){
	$('#scroll_top').click(function(){
		$('html, body').animate({scrollTop: 0}, 100);
		return false;
	});

	$('#scroll_bottom').click(function(){
		$('html, body').animate({scrollTop: $(document).height() - $(window).height()}, 100);
		return false;
	});
});