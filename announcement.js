document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');

    if (!id) {
        console.error('No announcement ID found in the URL.');
        return;
    }

    fetch(`http://127.0.0.1:5000/announcements/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(announcement => {
            const detailContainer = document.getElementById('announcement-detail');
            detailContainer.innerHTML = `
                <h2>${announcement.title}</h2>
                <p>${announcement.content}</p>
                <p><strong>Имя:</strong> ${announcement.name || 'Не указано'}</p>
                <p><strong>Контакт:</strong> ${announcement.contact || 'Не указан'}</p>
                    ${announcement.image ? `<img src="${announcement.image}" alt="Image" style="max-width 100%;">` : ''}
            `;
        })
        .catch(error => {
            console.error('Error fetching announcement details:', error);
        });
});
