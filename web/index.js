const btn = document.getElementById("themeToggle");
btn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  document.body.classList.toggle("light-mode");
  if (document.body.classList.contains("dark-mode")) {
    btn.textContent = "ساطع ☀️";
  } else {
    btn.textContent = "داكن 🌙";
  }
});

// افتراضي الوضع الداكن
document.body.classList.add("dark-mode");


// المينيو بتاع الموبايل
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('mobile-menu');
  const navLinks = document.getElementById('nav-links');
  const divider = document.getElementById('divider'); // بدل الـ span.a

  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
    if (divider) divider.style.display = 'none';
  });
});


// دالة عشان نقرأ الكوكيز
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

const username = getCookie("username");
const session = getCookie("session");
const ad1 = document.getElementById("admin");
const ad2 = document.getElementById("admin2");
const ad3 = document.getElementById("admin3");
const v = document.getElementById('main2');
const v2 = document.getElementById('main3');
const authArea = document.getElementById("auth-area");
const user = document.getElementById('user');
if (session == "logged" && username === "admin") {
  if (v2) v2.style.display = "none";
  authArea.innerHTML = `
    <button class="sign"><a href="/logout">تسجيل خروج</a></button>
  `;
} else if (session === "logged" && username){
  if (ad1) ad1.style.display = "none";
  if (ad2) ad2.style.display = "none";
  if (ad3) ad3.style.display = "none";
  if (v2) v2.style.display = "none";
  authArea.innerHTML = `
    <button class="sign"><a href="/logout">تسجيل خروج</a></button>
  `;
} else {
  if (ad1) ad1.style.display = "none";
  if (ad2) ad2.style.display = "none";
  if (ad3) ad3.style.display = "none";
  if (v) v.style.display = "none";
  if (user) user.style.display = "none";
  authArea.innerHTML = `
    <a href="/lo"><button>سجل دخولك</button></a>
    <span class="a">|</span> 
    <a href="/si"><button class="sign">اعمل حساب جديد</button></a>
  `;
}

