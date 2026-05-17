const menuBtn = document.getElementById("menuBtn");
const navbar = document.getElementById("navbar");
const searchInput = document.getElementById("searchInput");
const postCards = document.querySelectorAll(".post-card");

menuBtn.addEventListener("click", () => {
  navbar.classList.toggle("active");
});

searchInput.addEventListener("keyup", () => {
  const searchValue = searchInput.value.toLowerCase();

  postCards.forEach((card) => {
    const title = card.querySelector("h3").textContent.toLowerCase();
    const text = card.querySelector("p").textContent.toLowerCase();
    const category = card.querySelector(".category").textContent.toLowerCase();

    if (
      title.includes(searchValue) ||
      text.includes(searchValue) ||
      category.includes(searchValue)
    ) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
});