document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#btn').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let form = this.closest('form');
            let formData = new FormData(form);
            fetch(form.getAttribute('action'), {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(function(response) {
                if (response.ok) {
                    alert('Product added to order details!');
                } else {
                    alert('There was an issue adding the product. Please try again.');
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

