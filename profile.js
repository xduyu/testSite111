document.addEventListener('DOMContentLoaded', function() {
    // Получение данных пользователя из localStorage
    const loggedInUser = localStorage.getItem('loggedInUser');
    
    if (!loggedInUser) {
        alert('Вы не авторизованы');
        window.location.href = 'login.html'; // Перенаправление на страницу входа
        return;
    }
    
    const user = JSON.parse(loggedInUser);

    // Заполнение информации о пользователе
    document.getElementById('username').textContent = user.username;
    document.getElementById('password').textContent = '********'; // Не отображаем реальный пароль

    // Загрузка и отображение объявлений пользователя
    fetch(`http://127.0.0.1:5000/announcements?username=${user.username}`)
        .then(response => response.json())
        .then(data => {
            const announcementsList = document.getElementById('announcements-list');
            if (!announcementsList) {
                console.error('Element with id "announcements-list" not found');
                return;
            }

            announcementsList.innerHTML = '';

            if (data.length === 0) {
                announcementsList.innerHTML = '<p>У вас нет объявлений.</p>';
                return;
            }

            data.forEach(announcement => {
                const announcementElement = document.createElement('div');
                announcementElement.className = 'announcement';
                announcementElement.innerHTML = `
                    <h3><a href="announcement.html?id=${announcement.id}">${announcement.title}</a></h3>
                    <p>${announcement.content}</p>
                    <p><strong>Контакт:</strong> ${announcement.contact || 'Не указан'}</p>
                    ${announcement.image ? `<img src="${announcement.image}" alt="Image" style="max-width: 100%; max-height: 200px; border-radius: 8px;">` : ''}
                `;
                announcementsList.appendChild(announcementElement);
            });
        })
        .catch(error => {
            console.error('Error fetching user announcements:', error);
        });

    // Обработка формы смены пароля
    const changePasswordForm = document.getElementById('change-password-form');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const currentPassword = document.getElementById('current-password').value;
            const newPassword = document.getElementById('new-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (newPassword !== confirmPassword) {
                alert('Новый пароль и подтверждение не совпадают');
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/users/${user.username}/change-password`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        currentPassword: currentPassword,
                        newPassword: newPassword
                    })
                });

                if (response.ok) {
                    alert('Пароль успешно изменен');
                    localStorage.removeItem('loggedInUser');
                    window.location.href = 'login.html'; // Перенаправление на страницу входа
                } else {
                    const errorData = await response.json();
                    alert(`Ошибка при смене пароля: ${errorData.error || 'Неизвестная ошибка'}`);
                }
            } catch (error) {
                console.error('Error changing password:', error);
                alert('Произошла ошибка при смене пароля');
            }
        });
    }
});
