function animateValue(id, target, suffix = " kg") {
    let count = 0;
    let step = Math.max(1, Math.floor(target / 50));

    let interval = setInterval(() => {
        if (count >= target) {
            document.getElementById(id).innerText = target + suffix;
            clearInterval(interval);
        } else {
            count += step;
            document.getElementById(id).innerText = count + suffix;
        }
    }, 30);
}

window.onload = function () {
    animateValue("collected", 100);
    animateValue("recycled", 30);
    document.getElementById("users").innerText = 8;
};
