window.addEventListener('load', function() {
    // 민트색 배경을 1초 동안 페이드 아웃
    setTimeout(function() {
        document.getElementById('loading-overlay').style.transition = 'opacity 2s ease';
        document.getElementById('loading-overlay').style.opacity = 0;

        // 1초 후 민트색 배경 제거
        setTimeout(function() {
            document.getElementById('loading-overlay').remove();

            // intro-overlay 페이드 아웃 (기존 동작)
            setTimeout(function() {
                document.getElementById('intro-overlay').classList.add('hidden');
            }, 4000); // 5초 후 intro-overlay 숨김
        }, 2000); // 민트색 배경 페이드 아웃 시간 (2초)

    }, 500); // 페이지 로드 후 0.5초 대기 후 민트색 배경 페이드아웃 시작
});


// 각 글자에 애니메이션 적용 함수
function animateHeader(headerId) {
    const header = document.getElementById(headerId);
    const text = header.textContent;
    header.innerHTML = '';  // 기존 텍스트를 지우고

    // 각 글자를 span 태그로 감싸고 클래스를 적용
    for (let i = 0; i < text.length; i++) {
        const span = document.createElement('span');
        span.classList.add('letter');
        span.textContent = text[i];
        header.appendChild(span);
    }

    // 각 글자에 순차적으로 애니메이션 적용
    const letters = header.querySelectorAll('.letter');
    letters.forEach((letter, index) => {
        setTimeout(() => {
            letter.classList.add('letter-up');
            setTimeout(() => {
                letter.classList.remove('letter-up');
            }, 200);  // 0.2초 후 다시 내려감
        }, index * 400);  // 각 글자는 0.4초 간격으로 애니메이션 실행
    });
}

// 각 헤더 요소에 마우스를 올렸을 때 애니메이션 실행
document.getElementById('rank-header').addEventListener('mouseenter', function() {
    animateHeader('rank-header');
});
document.getElementById('title-header').addEventListener('mouseenter', function() {
    animateHeader('title-header');
});
document.getElementById('artist-header').addEventListener('mouseenter', function() {
    animateHeader('artist-header');
});


 // URL에서 현재 날짜 추출 함수
 function getDateFromURL() {
        const url = window.location.pathname;
        const dateMatch = url.match(/(\d{4}-\d{2}-\d{2})/);
        if (dateMatch) {
            return dateMatch[0];
        }
        // URL에서 날짜가 없으면 기본값을 2024-09-08로 설정
        return '2024-09-08';
    }

    // 선택한 날짜의 첫 번째 일요일을 계산하는 함수
    function getSunday(date) {
        const currentDate = new Date(date);
        const dayOfWeek = currentDate.getDay();  // 0: 일요일, 1: 월요일, ... 6: 토요일
        const diff = currentDate.getDate() - dayOfWeek;  // 일요일까지의 차이 계산
        const sunday = new Date(currentDate.setDate(diff));
        return sunday.toISOString().split('T')[0];  // YYYY-MM-DD 형식으로 반환
    }

    // 날짜를 일주일 단위로 조정하는 함수
    function adjustDate(weeks) {
        const dateInput = document.getElementById('date-calendar-input');
        let currentDate = dateInput.value ? new Date(dateInput.value) : new Date(getDateFromURL());

        // 일주일 단위로 날짜 조정
        currentDate.setDate(currentDate.getDate() + weeks * 7);

        // 해당 주의 첫 번째 일요일을 계산
        const sundayDate = getSunday(currentDate);

        // 입력 필드 업데이트
        dateInput.value = sundayDate;

        // 페이지 이동
        location.href = `/chartlist/${sundayDate}`;  // 새로 계산된 일요일 날짜로 이동
    }

    // 왼쪽 화살표 클릭 시 일주일 전으로 날짜 조정
    document.getElementById('prev-week').addEventListener('click', function() {
        adjustDate(-1);  // 일주일 전
    });

    // 오른쪽 화살표 클릭 시 일주일 후로 날짜 조정
    document.getElementById('next-week').addEventListener('click', function() {
        adjustDate(1);  // 일주일 후
    });

    // 날짜 선택 시 첫 번째 일요일로 변경하여 표시
    document.getElementById('date-calendar-input').addEventListener('change', function(e) {
        const selectedDate = e.target.value;
        const sundayDate = getSunday(selectedDate);  // 선택된 날짜의 일요일 계산
        
        // 일요일 날짜를 페이지의 날짜 라벨에 표시
        const dateLabel = document.getElementById('date-label');
        const sunday = new Date(sundayDate);
        const year = sunday.getFullYear();
        const month = ('0' + (sunday.getMonth() + 1)).slice(-2);  // 월 2자리 형식
        const day = ('0' + sunday.getDate()).slice(-2);  // 일 2자리 형식

        // 페이지 이동
        location.href = `/chartlist/${sundayDate}`;  // 새로 계산된 일요일 날짜로 이동
    });

    // 페이지가 로드될 때 URL에서 현재 날짜를 추출하고 입력 필드를 업데이트
    window.addEventListener('load', function() {
        const dateInput = document.getElementById('date-calendar-input');
        const currentURLDate = getDateFromURL();
        dateInput.value = currentURLDate;
    });









// 스크롤에 따라 배경색을 변경하는 함수
window.addEventListener('scroll', function() {
        // 페이지의 총 스크롤 가능한 높이와 현재 스크롤 위치 계산
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = scrollTop / docHeight;

        // 무지개색을 중간 부분에만 적용 (스크롤 비율이 0.2에서 0.8 사이일 때)
        let hue = 0;
        let lightness = 100; // 기본 흰색 (lightness 100%)
        
        if (scrollPercent >= 0.2 && scrollPercent <= 0.8) {
            // 무지개색을 중간에만 적용
            hue = Math.round((scrollPercent - 0.2) / 0.6 * 360);  // hue 값은 0~360으로 설정
            lightness = 80; // 색이 연하게 보이도록 lightness 값을 80%로 설정
        } else if (scrollPercent > 0.8) {
            // 마지막 부분으로 갈수록 흰색으로 변화
            lightness = Math.round(100 - (scrollPercent - 0.8) / 0.2 * 100);  // 끝에서 흰색으로 변화
        }

        // 배경색을 HSL 모델을 사용하여 설정
        document.body.style.backgroundColor = `hsl(${hue}, 100%, ${lightness}%)`;
    });

document.getElementById("top-btn").addEventListener("click", () => {
    window.scrollTo({top: 0, left: 0, behavior: 'smooth'});
})