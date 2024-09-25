// 메인 페이지 자바스크립트 파일
// 추후에 정상화시킬 예정

// ☆★☆ 페이지 배경 정상화 애니메이션 효과 ☆★☆
const colors = ['azure', 'lightskyblue', 'cornsilk'];
let currentIndex = 0;
function changeBackgroundColor() {
  document.getElementById("main-wrapper").style.backgroundColor = colors[currentIndex];
  currentIndex = (currentIndex + 1) % colors.length;
}
setInterval(changeBackgroundColor, 1000);


// 메인 페이지의 버튼 클릭하면 차트 테스트 페이지로 넘어가는 이벤트리스너 설정
document.getElementById("chartbutton").addEventListener("click", (e) => {
  location.href = '/chart';
});