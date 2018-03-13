/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	'use strict';
	
	var $ = window.$;
	var R = window.grecaptcha;
	
	$(document).ready(function () {
	    $('.expandable, .collapsible').each(function (i, e) {
	        var $e = $(e);
	        $e.find('h2').click(function () {
	            $e.toggleClass('expandable');
	            $e.toggleClass('collapsible');
	        });
	    });
	    $('.biblio_summary').each(function (i, e) {
	        var $e = $(e);
	        $e.click(function () {
	            var $ul = $e.parent().find('ul');
	            $e.toggleClass('biblio_expand');
	            $e.toggleClass('biblio_collapse');
	            $ul.toggleClass('biblio_expand');
	            $ul.toggleClass('biblio_collapse');
	        });
	    });
	
	    function revealEmail(name, recaptcha, element) {
	        var data = JSON.stringify({
	            key: recaptcha,
	            name: name
	        });
	        $.ajax('/people/reveal', {
	            type: 'POST',
	            data: data,
	            contentType: 'application/json',
	            success: function success(data) {
	                var text = '<a href="mailto:' + data.email + '">' + data.email + '</a>';
	                $(element).replaceWith(text);
	                $('#recaptcha').empty();
	            }
	        });
	    }
	
	    function displayReCaptcha(element) {
	        var name = $(element).data('name');
	        $('.recaptcha-modal').show();
	        var recaptcha = window.grecaptcha.render('recaptcha', {
	            sitekey: '6LcfPycTAAAAAGVOSeHk1etTkgbwJtHi32Tj6BsH',
	            callback: function callback() {
	                $('.recaptcha-modal').hide();
	                $(element).text('Loading...');
	                var response = window.grecaptcha.getResponse(recaptcha);
	                window.grecaptcha.reset(recaptcha);
	                revealEmail(name, response, element);
	            }
	        });
	    }
	
	    $('.reveal-email').click(function (e) {
	        displayReCaptcha(e.target);
	    });
	});

/***/ }
/******/ ]);
//# sourceMappingURL=person-search.js.map