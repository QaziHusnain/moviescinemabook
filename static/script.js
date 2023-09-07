 // Get references to the dropdown and the selected movie ID input field
    const movieSelect = document.getElementById('movie-select');
    const selectedMovieIdInput = document.getElementById('selected-movie-id');
    const bookForm = document.getElementById('book-form');
    const bookButton = document.getElementById('book-button');

    // Add an event listener to the dropdown
    movieSelect.addEventListener('change', function() {
        const selectedMovieId = movieSelect.value;

        if (selectedMovieId) {
            // Set the selected movie ID in the hidden input field
            selectedMovieIdInput.value = selectedMovieId;
            // Enable the "Book Now" button
            bookButton.removeAttribute('disabled');
        } else {
            // No movie selected, so clear the selected movie ID and disable the button
            selectedMovieIdInput.value = '';
            bookButton.setAttribute('disabled', 'true');
        }
    });


