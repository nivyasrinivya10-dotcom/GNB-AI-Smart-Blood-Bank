 function registerDonor() {

    let name = document.getElementById("name").value;
    let age = document.getElementById("age").value;
    let bloodGroup = document.getElementById("bloodGroup").value;
    let city = document.getElementById("city").value;
    let phone = document.getElementById("phone").value;

    let donors = JSON.parse(localStorage.getItem("donors")) || [];

    donors.push({
        name: name,
        age: age,
        bloodGroup: bloodGroup,
        city: city,
        phone: phone
    });

    localStorage.setItem("donors", JSON.stringify(donors));

    alert("🎉 Registration Successful!");

    window.location.href = "donors.html";
}