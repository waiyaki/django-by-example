(function() {
  var jquery_version = '2.1.4';
  var site_url = 'http://127.0.0.1:8000/';
  var static_url = site_url + 'static/';
  var min_width = 100;
  var min_height = 100;

  function bookmarklet(msg) {
    // load css
    var css = jQuery('<link>');
    css.attr({
      rel: 'stylesheet',
      type: 'text/css',
      href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random() * 9999999999)
    });
    jQuery('head').append(css);

    // Load HTML
    var box_html = `
      <div id="bookmarklet">
        <div class="bookmarklet-header">
          <a href="#" id="close">&times;</a>
          <h1>Select an image to bookmark:</h1>
        </div>
        <div class="images"></div>
      </div>
    `
    jQuery('body').append(box_html);

    // Close event
    jQuery('#bookmarklet #close').click(function() {
      jQuery('#bookmarklet').remove();
    });

    // Find images and display them.
    jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
      if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height) {
        image_url = jQuery(image).attr('src');
        jQuery('#bookmarklet .images').append('<a href="#"><img src="' + image_url + '" /></a>');
      }
    });

    // when an image is selected open URL with it
    jQuery('#bookmarklet .images a').click(function(e) {
      selected_image = jQuery(this).children('img').attr('src');
      // hide bookmarklet
      jQuery('#bookmarklet').hide();
      // open new window to submit the image
      window.open(site_url + 'images/create/?url='
        + encodeURIComponent(selected_image)
        + '&title='
        + encodeURIComponent(jQuery('title').text()),
        '_blank'
      );
    });
  }

  // Check if jQuery is loaded
  if (window.jQuery) {
    bookmarklet();
  } else {
    // Check for conflicts
    var conflict = typeof window.$ !== 'undefined';
    // Create a script and point it to Google API
    var script = document.createElement('script');
    script.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' + jquery_version + '/jquery.min.js');

    // Append the script to the html head
    document.getElementsByTagName('head')[0].appendChild(script);

    // Wait until the script loads
    var attempts = 15;
    (function() {
      if (!window.jQuery) {
        if (--attempts > 0) {
          window.setTimeout(arguments.callee, 250); // Leak??
        } else {
          alert('An error occurred while loading jQuery');
        }
      } else {
        bookmarklet();
      }
    })();
  }
})();
