function handleLogin(event) {
    event.preventDefault();

    const role = document.getElementById("role").value;

    // Future: Django authentication logic here

    if (role === "user") {
        window.location.href = "/submit-ewaste/";
    } 
    else if (role === "recycler") {
        window.location.href = "/accept-ewaste/";
    } 
    else if (role === "admin") {
        window.location.href = "/portal-admin/";
    } 
    else {
        alert("Please select a role");
    }
}
