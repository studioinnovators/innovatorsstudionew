const pdpcourseList = document.getElementById("pdpcourseclasscardlist");
const pdpcoursenextBtn = document.getElementById("pdpcourseclassnextCard");
const pdpcourseprevBtn = document.getElementById("pdpcourseclassprevCard");
const pdpcourseallcardListItems = document.querySelectorAll(
  ".pdpcourseclasslist"
);
let pdpcourseflag = 0;

pdpcoursenextBtn.addEventListener("click", () => {
  pdpcourseflag = 0;
  const width = pdpcourseallcardListItems[0].offsetWidth;
  pdpcourseList.style.transform = `translateX(${-width}px)`;
  pdpcourseList.style.transition = "transform 0.8s ease";
});

pdpcourseList.addEventListener("transitionend", () => {
  if (pdpcourseflag == 0) {
    const listitemfirst = document.querySelector(".pdpcourseclasslist");
    pdpcourseList.appendChild(listitemfirst);
    pdpcourseList.style.transition = "none";
    pdpcourseList.style.transform = `translateX(0)`;
    setTimeout(() => {
      pdpcourseList.style.transition = "transform 0.8s ease";
    });
  }
  if (pdpcourseflag == 1) {
    const listitemfirst = document.querySelector(".pdpcourseclasslist");
    const listitemnew = document.querySelectorAll(".pdpcourseclasslist")[6];
    pdpcourseList.insertBefore(listitemnew, listitemfirst);
    pdpcourseList.style.transition = "transform 0.8s ease";
    pdpcourseList.style.transform = `translateX(0)`;
    setTimeout(() => {
      pdpcourseList.style.transition = "transform 0.8s ease";
    });
    pdpcourseflag = 2;
  }
});

pdpcourseprevBtn.addEventListener("click", () => {
  pdpcourseflag = 1;
  pdpcourseList.style.transition = "all 0.01s";
  const width = pdpcourseallcardListItems[0].offsetWidth;
  pdpcourseList.style.transform = `translateX(${-width}px)`;
});
