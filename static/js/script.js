// Locomotive Scroll Initialization
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

// Force Scroll Top and Container Refresh on Every Page Load
window.addEventListener("load", () => {
    // Top position force reset
    window.scrollTo(0, 0);
    if (scroll) {
        scroll.scrollTo(0, { duration: 0, disableLerp: true });
        scroll.update();
    }
});

// Fix link clicks locking scroll or navigating to hashes
document.addEventListener("DOMContentLoaded", () => {
    if (scroll) {
        scroll.update();
    }
    
    // Auto-update after images load completely
    setTimeout(() => {
        if (scroll) scroll.update();
    }, 1000);
});

// Window Resize Fix
window.addEventListener("resize", () => {
    if (scroll) scroll.update();
});