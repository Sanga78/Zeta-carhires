document.addEventListener('DOMContentLoaded', () => {
    loadCarsForSale(); // Dynamically loads cars for sale
});
// document.addEventListener('DOMContentLoaded', () => {
//     loadCarouselItems(); // Function to load carousel items if defined
    
// });

// "Cars for Sale"
const carsForSaleData = [
    { src: "../images/car-2.jpg", model: "Mazda demio", price: "30,000", description: "Description for Car Model 1", colors: "Red, Blue, Black", seats: "4", images: ['../images/24_LEG_gallery_int_03.jpg', '../images/JDPA_2021 Subaru Legacy Limited XT Gray Interior Dashboard.webp', '../images/Screenshot-2023-09-03-145752.png']},
    { src: "../images/car-2.jpg", model: "Prado", price: "20,000", description: "Description for Car Model 2", colors: "Red, Blue, Black", seats: "2", images: ['../images/24_LEG_gallery_int_03.jpg', '../images/JDPA_2021 Subaru Legacy Limited XT Gray Interior Dashboard.webp', '../images/Screenshot-2023-09-03-145752.png']},
    { src: "../images/car-3.jpg", model: "Probox", price: "50,000", description: "Description for Car Model 3", colors: "Red, Blue, Black", seats: "5", images: ['../images/24_LEG_gallery_int_03.jpg', '../images/JDPA_2021 Subaru Legacy Limited XT Gray Interior Dashboard.webp', '../images/Screenshot-2023-09-03-145752.png']},
    { src: "../images/car-4.jpg", model: "Harrier", price: "10,000", description: "Description for Car Model 4", colors: "Red, Blue, Black", seats: "1", images: ['../images/24_LEG_gallery_int_03.jpg', '../images/JDPA_2021 Subaru Legacy Limited XT Gray Interior Dashboard.webp', '../images/Screenshot-2023-09-03-145752.png']},
];

function loadCarsForSale() {
    const carsList = document.querySelector(".cars-for-sale .car-list");
    carsForSaleData.forEach((car, index) => {
        const carItem = document.createElement("div");
        carItem.className = "car-item";
        carItem.innerHTML = `
            <div class="gari"><img src="${car.src}" alt="${car.model}"></div>
            <h3>${car.model}</h3>
            <p>$${car.price}</p>
            <button class="btn-buy" onclick="showPhoneNumber()">Buy Now</button>
            <button class="btn-desc" onclick="openModal(${index})">Description</button>
        `;
        carsList.appendChild(carItem);
    });
}

function openModal(index) {
    const car = carsForSaleData[index];
    const modal = document.getElementById('carModal');
    document.getElementById('carColor').textContent = `${car.colors}`;
    document.getElementById('carSeats').textContent = `${car.seats}`;
    const carImages = modal.querySelector('.car-images');
    carImages.innerHTML = car.images.map(image => `<img src="${image}" alt="View">`).join('');
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('carModal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('carModal')) {
        closeModal();
    }
}

function toggleMenu() {
    const navLinks = document.getElementById("navLinks");
    navLinks.style.display = navLinks.style.display === "block" ? "none" : "block";
}
function showPhoneNumber() {
    var phoneNumber = document.getElementById("phoneNumber");
    phoneNumber.style.display = "block";

    setTimeout(function() {
        phoneNumber.style.display = "none";
    },3000);
    window.addEventListener('scroll',function(){
        phoneNumber.style.display = "none";
    },{once:true});
}
