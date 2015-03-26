jQuery(document).ready(function () {
	// Unbind on document ready so it will still at least try
	// to be functional while the page may still be loading
	wp_gallery_custom_links_setup();
	
	// Do unbinding, etc. again in window.onload to help reduce
	// the number of conflicting lightboxes etc. without
	// making the user have to declare js dependencies
	function addLoadEvent(func) {
		var oldOnload = window.onload;
		if(typeof window.onload != 'function') {
			window.onload = func;
		} else {
			window.onload = function() {
				oldOnload();
				func();
			}
		}
	}
	addLoadEvent(wp_gallery_custom_links_setup);
});

function wp_gallery_custom_links_setup() {
	if(jQuery.fn.off) {
		// jQuery 1.7+
		jQuery('.no-lightbox, .no-lightbox img').off('click');
	} else {
		// < jQuery 1.7
		jQuery('.no-lightbox, .no-lightbox img').unbind('click');
	}
	jQuery('a.no-lightbox').click(wp_gallery_custom_links_click);
	
	if(jQuery.fn.off) {
		// jQuery 1.7+
		jQuery('a.set-target').off('click');
	} else {
		// < jQuery 1.7
		jQuery('a.set-target').unbind('click');
	}
	jQuery('a.set-target').click(wp_gallery_custom_links_click);
}

function wp_gallery_custom_links_click() {
	if(!this.target || this.target == '' || this.target == '_self')
		window.location = this.href;
	else
		window.open(this.href,this.target);
	return false;
}
