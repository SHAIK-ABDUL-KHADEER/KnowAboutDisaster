document.addEventListener('DOMContentLoaded', function() {
    // Get location button click event
    const getLocationButton = document.getElementById('get-location');
    if (getLocationButton) {
        getLocationButton.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latitudeInput = document.getElementById('latitude');
                    const longitudeInput = document.getElementById('longitude');
                    if (latitudeInput && longitudeInput) {
                        latitudeInput.value = position.coords.latitude;
                        longitudeInput.value = position.coords.longitude;
                    }
                }, function(error) {
                    alert("Error getting location: " + error.message);
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        });
    }

    // Submit location button click event
    const submitLocationButton = document.getElementById('submit-location');
    if (submitLocationButton) {
        submitLocationButton.addEventListener('click', function() {
            const latitude = document.getElementById('latitude').value;
            const longitude = document.getElementById('longitude').value;
            const disasterName = document.getElementById('disaster-name').value;

            fetch('/upload_location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude,
                    disaster_name: disasterName
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Location and disaster information submitted successfully.');
                    loadNotifications(); // Reload notifications after submission
                } else {
                    alert('Error submitting information.');
                }
            });
        });
    }

    // Disaster click event to open modal
    document.querySelectorAll('.disaster-container').forEach(function(element) {
        element.addEventListener('click', function() {
            const disasterName = this.getAttribute('data-disaster');
            const disasterTitleElement = document.getElementById('disaster-title');
            const disasterDescriptionElement = document.getElementById('disaster-description');
            const disasterModalElement = document.getElementById('disaster-modal');
            if (disasterTitleElement && disasterDescriptionElement && disasterModalElement) {
                disasterTitleElement.textContent = disasterName.charAt(0).toUpperCase() + disasterName.slice(1);
                disasterDescriptionElement.textContent = `Description of ${disasterName.charAt(0).toUpperCase() + disasterName.slice(1)}...`;
                disasterModalElement.style.display = 'block';
            }
        });
    });

    // Close modal
    const closeButton = document.querySelector('.close-button');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            const disasterModalElement = document.getElementById('disaster-modal');
            if (disasterModalElement) {
                disasterModalElement.style.display = 'none';
            }
        });
    }

    // Send message to chat
    const sendMessageButton = document.getElementById('send-message');
    if (sendMessageButton) {
        sendMessageButton.addEventListener('click', function() {
            const message = document.getElementById('chat-input').value;
            const disasterName = document.getElementById('disaster-title').textContent; // Correct ID

            if (message.trim() === '') return;

            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: message, disaster_name: disasterName })
            })
            .then(response => response.json())
            .then(data => {
                const chatBox = document.getElementById('chatBox');
                if (chatBox) {
                    if (data.response) {
                        chatBox.innerHTML += `<p><strong>Response:</strong> ${data.response}</p>`;
                        document.getElementById('chat-input').value = '';
                    } else if (data.error) {
                        alert(data.error);
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Load notifications
    function loadNotifications() {
        fetch('/get_notifications')
            .then(response => response.json())
            .then(data => {
                const notificationsContainer = document.getElementById('notifications-container');
                if (notificationsContainer) {
                    notificationsContainer.innerHTML = '';
                    data.notifications.forEach(notification => {
                        const notificationElement = document.createElement('div');
                        notificationElement.classList.add('notification');
                        notificationElement.innerHTML = `
                            <strong>${notification.username}</strong><br>
                            ${notification.disaster_name}<br>
                            ${notification.latitude}, ${notification.longitude}<br>
                            ${notification.timestamp}
                        `;
                        notificationsContainer.appendChild(notificationElement);
                    });
                }
            });
    }

    loadNotifications(); // Load notifications on page load
});
