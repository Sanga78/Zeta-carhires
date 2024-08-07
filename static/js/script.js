

document.addEventListener('DOMContentLoaded', () => {
    "use strict";
    const mobileNavShow = document.querySelector('.mobile-nav-show');
    const mobileNavHide = document.querySelector('.mobile-nav-hide');
  
    document.querySelectorAll('.mobile-nav-toggle').forEach(el => {
      el.addEventListener('click', function(event) {
        event.preventDefault();
        mobileNavToogle();
      })
    });
  
    function mobileNavToogle() {
      document.querySelector('body').classList.toggle('mobile-nav-active');
      mobileNavShow.classList.toggle('d-none');
      mobileNavHide.classList.toggle('d-none');
    }
  
    /**
     * Hide mobile nav on same-page/hash links
     */
    document.querySelectorAll('#navbar a').forEach(navbarlink => {
  
      if (!navbarlink.hash) return;
  
      let section = document.querySelector(navbarlink.hash);
      if (!section) return;
  
      navbarlink.addEventListener('click', () => {
        if (document.querySelector('.mobile-nav-active')) {
          mobileNavToogle();
        }
      });
  
    });
});
  // let currentIndex = 0;
  // const images = document.querySelectorAll('.carousel-image');
  // const changeImage = () => {
  //     images[currentIndex].classList.add('hidden');
  //     currentIndex = (currentIndex + 1) % images.length;
  //     images[currentIndex].classList.remove('hidden');
  // }
  // setInterval(changeImage, 3000); // Change image every 3 seconds

  const slider = document.querySelector('.slider');
  const items = document.querySelectorAll('.item');
  const btns = document.querySelectorAll('.slider-btn');
  let newIndex = 0; // Tracks the current slide
  const intervalTime = 5000; // Time between slides in milliseconds
  let autoSlideInterval; // Holds the interval ID for automatic sliding
  
  function reset() {
    for (let i = 0; i < items.length; i++) {
      btns[i].classList.remove('expand');
      items[i].classList.remove('animation');
    }
  }
  
  function animate(i) {
    btns[i].classList.add('expand');
    items[i].classList.add('animation');
  }
  
  function scrollTo(i) {
    slider.style.transform = `translateX(${-i * slider.offsetWidth}px)`;
    reset();
    animate(i);
  }

  function startAutoSlide() {
    clearInterval(autoSlideInterval); // Clear the existing interval
    autoSlideInterval = setInterval(() => {
      newIndex = (newIndex + 1) % items.length;
      scrollTo(newIndex);
    }, intervalTime);
  }
  function pauseAutoSlide() {
    clearInterval(autoSlideInterval);
  }
  
  const activate = (e) => e.target.matches('.slider-btn') && scrollTo(e.target.dataset.index);
  
  const init = () => {
    animate(0); // Start with the first slide
    startAutoSlide(); // Initiate automatic sliding
  };
  
  // Pause on hover
  slider.addEventListener('mouseover', pauseAutoSlide);
  slider.addEventListener('mouseout', startAutoSlide);
  
  // Swipe gestures for touch devices
  let touchstartX = 0;
  let touchendX = 0;
  
  function handleGesture() {
    if (touchendX < touchstartX) {
      newIndex = (newIndex + 1) % items.length;
    } else if (touchendX > touchstartX) {
      newIndex = (newIndex - 1 + items.length) % items.length; // Ensure the index stays within bounds
    }
    scrollTo(newIndex);
  }
  
  slider.addEventListener('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX;
  });
  
  slider.addEventListener('touchend', e => {
    touchendX = e.changedTouches[0].screenX;
    handleGesture();
  });
  
  window.addEventListener('load', init, false);
  window.addEventListener('click', activate, false);
  
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
      currentIndex = (currentIndex + 1) % items.length;
      scrollTo(currentIndex);
      pauseAutoSlide(); // Ensure we pause the slider if the user is manually navigating
      startAutoSlide(); // Resume automatic sliding after a delay
    } else if (e.key === 'ArrowLeft') {
      currentIndex = (currentIndex - 1 + items.length) % items.length;
      scrollTo(currentIndex);
      pauseAutoSlide(); // Pause automatic sliding
      startAutoSlide(); // Resume automatic sliding
    }
  });
 
// Debounce function to prevent rapid keyboard inputs
function debounce(func, wait) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}

// Enhanced keyboard navigation with debounce
const handleKeyNavigation = debounce((e) => {
  if (e.key === 'ArrowRight') {
    newIndex = (newIndex + 1) % items.length;
  } else if (e.key === 'ArrowLeft') {
    newIndex = (newIndex - 1 + items.length) % items.length;
  }
  scrollTo(newIndex);
  pauseAutoSlide(); // Pause the automatic sliding
  startAutoSlide(); // Reset and start the automatic sliding timer
}, 250); // 250 milliseconds debounce period

document.addEventListener('keydown', handleKeyNavigation);

function openModal() {
  var modal = document.getElementById("carModal");
  var number = document.getElementById("number");

  number.textContent = +254714710947;
  modal.style.display = "block";
}

function closeModal() {
  var modal = document.getElementById("carModal");
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == document.getElementById('carModal')) {
      closeModal();
  }
}
function showPhoneNumber() {
  var phoneNumber = document.getElementById("phoneNumber");
  phoneNumber.style.display = "block";

  setTimeout(function() {
      phoneNumber.style.display = "none";
  },10000);
  window.addEventListener('scroll',function(){
      phoneNumber.style.display = "none";
  },{once:true});
}

// var signupEmailIn = document.getElementById("email");
// var firstname = document.getElementById("first_name");
// var lastname = document.getElementById("last_name");
// var username = document.getElementById("username");
// var signupPasswordIn = document.getElementById("password");
// var confirmSignupPasswordIn = document.getElementById("password2");
// var registerButton = document.getElementById("Register_btn");

// var email,
//     username,
//     firstname,
//     lastname,
//     signupEmail,
//     signupPassword,
//     confirmSignupPassword;

// registerButton.addEventListener("click", function() {
//     var isVarified = true;

//     signupEmail = signupEmailIn.value;
//     username = username.value;
//     firstname = firstname.value;
//     lastname = lastname.value;

//     signupPassword = signupPasswordIn.value;
//     confirmSignupPassword = confirmSignupPasswordIn.value;

//     if (signupPassword != confirmSignupPassword) {
//         window.alert("Passwords does not match");
//         isVarified = false;
//     }

//     if (signupEmail == null ||
//         username == null ||
//         firstname == null ||
//         lastname == null ||
//         signupPassword == null ||
//         confirmSignupPassword == null) {
//         window.alert("Please fill all the required fields");
//     }

//     if (isVarified) {
//         window.alert("Acount Created Successfully");
//         window.location.href = "{{ 'loginpage' }}";
//     }
// });