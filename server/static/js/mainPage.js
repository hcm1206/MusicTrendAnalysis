// 메인 페이지 자바스크립트 파일

// 메인 페이지의 버튼 클릭하면 차트 리스트 페이지로 넘어가는 이벤트리스너 설정
document.getElementById("link-btn").addEventListener("click", (e) => {
  location.href = '/chartlist';
});