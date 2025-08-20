* Изучено использование *JavaScript* для динамического изменения контента веб-страниц и взаимодействия с объектной моделью документа *DOM*. Определены основные методы манипуляции элементами HTML, их стилями и обработке событий пользователя.
   * Использование *JavaScript* позволило реализовать такие интерактивные элементы, как появление изображений только при наведении на них, а также изменить фон веб-страницы с помощью кнопки.
   * Исследованы современные возможности языка, включая обработку событий, работу с функциями и взаимодействие со структурой DOM.

* Приложение A - реализация "LAZY LOADING"
```
document.addEventListener("DOMContentLoaded",function (){
 let LazyImages=document.querySelectorAll("img.Lazy");
 let observer=new IntersectionObserver((entries,observer)=>{
 entries.forEach(entry => {
 if(entry.isIntersecting){
 let img=entry.target;
 img.src=img.getAttribute("data-src");
 img.classList.remove("Lazy");
 observer.unobserve(img);
 }
 });
 });
 LazyImages.forEach(img => observer.observe(img));
});
```

* Приложение B - реализация изменения фоновых изображений
```
document.addEventListener("DOMContentLoaded", function () {
const toggleButton = document.getElementById("settings-button");
const body = document.body;
const logo = document.getElementById("logo");
const lightLogo = "assets/dawn.jpg";
const darkLogo = "assets/Pica-enhance-20250301234303.jpg";
function updateLogo() {
 if (body.classList.contains("dark-theme")) {
 logo.src = darkLogo;
 } else {
 logo.src = lightLogo;
 }
}
if (localStorage.getItem("theme") === "dark") {
 body.classList.add("dark-theme");
}
updateLogo();
if (toggleButton) {
 toggleButton.addEventListener("click", function () {
 body.classList.toggle("dark-theme");
 updateLogo();
 if (body.classList.contains("dark-theme")) {
 localStorage.setItem("theme", "dark");
 } else {
 localStorage.setItem("theme", "light");
 }
 });
}
});
```