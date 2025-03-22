// 이벤트 리스너가 DOM이 로드된 후에 실행되도록 합니다
document.addEventListener('DOMContentLoaded', function() {
    // 플레이리스트 선택 요소들과 관련 버튼을 찾습니다
    const playlistSelects = document.querySelectorAll('.playlist-select');
    const addToPlaylistButtons = document.querySelectorAll('.add-to-playlist-btn');
    
    // 각 플레이리스트 선택 요소에 이벤트 리스너를 추가합니다
    if (playlistSelects.length > 0) {
        playlistSelects.forEach((select, index) => {
            select.addEventListener('change', function() {
                const button = addToPlaylistButtons[index];
                // 선택된 값이 있을 때만 버튼을 활성화합니다
                button.disabled = !this.value;
            });
        });
    }
    
    // 플래시 메시지가 있으면 5초 후에 자동으로 사라지게 합니다
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.style.opacity = '0';
                message.style.transition = 'opacity 0.5s';
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 5000);
    }
}); 