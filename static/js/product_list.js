// product_list.js
document.addEventListener('DOMContentLoaded', () => {
  new Swiper('.omi-hero-slider', {
    loop: true,

    // autoplay every 4 seconds
    autoplay: {
      delay: 4000,
      disableOnInteraction: false
    },

    // enable bullet clicks
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },

    // your nav arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    },

    // fade between slides
    effect: 'fade',
    fadeEffect: {
      crossFade: true
    }
  });
});
