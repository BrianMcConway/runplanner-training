(function ($) {
    // Initialize field names and types
    window.fnames = new Array();
    window.ftypes = new Array();
    
    fnames[0] = 'EMAIL';
    ftypes[0] = 'email';
    fnames[1] = 'FNAME';
    ftypes[1] = 'text';
    fnames[2] = 'LNAME';
    ftypes[2] = 'text';
    fnames[3] = 'ADDRESS';
    ftypes[3] = 'address';
    fnames[4] = 'PHONE';
    ftypes[4] = 'phone';
    fnames[5] = 'BIRTHDAY';
    ftypes[5] = 'birthday';
    fnames[6] = 'COMPANY';
    ftypes[6] = 'text';
})(jQuery);

// Avoid conflicts with other jQuery versions
var $mcj = jQuery.noConflict(true);
