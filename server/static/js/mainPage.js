// 메인 페이지 자바스크립트 파일
// 추후에 정상화시킬 예정

const colors = ['azure', 'lightskyblue', 'cornsilk'];
let currentIndex = 0;

function changeBackgroundColor() {
  let mainpage = document.getElementById("main-wrapper")
  mainpage.style.backgroundColor = colors[currentIndex];
  currentIndex = (currentIndex + 1) % colors.length;
}

setInterval(changeBackgroundColor, 1000);