
const scroll = new LocomotiveScroll({
    el: document.querySelector("#main"),
    smooth: true,
    multiplier: 0.9,
    smartphone: {
        smooth: true
    },
    tablet: {
        smooth: true
    }
});


window.addEventListener("load", () => {
    
    window.scrollTo(0, 0);
    if (scroll) {
        scroll.scrollTo(0, { duration: 0, disableLerp: true });
        scroll.update();
    }
});


document.addEventListener("DOMContentLoaded", () => {
    if (scroll) {
        scroll.update();
    }
    
   
    setTimeout(() => {
        if (scroll) scroll.update();
    }, 1000);
});


window.addEventListener("resize", () => {
    if (scroll) scroll.update();
});