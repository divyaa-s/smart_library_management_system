document.addEventListener('DOMContentLoaded', function() {
    // Mock data for recommendations, this should come from the server
    const recommendations = [
        { title: 'Recommended Book 1', author: 'Author A' },
        { title: 'Recommended Book 2', author: 'Author B' },
    ];

    const recommendationsContainer = document.getElementById('recommendations-container');
    
    recommendations.forEach(book => {
        const bookDiv = document.createElement('div');
        bookDiv.classList.add('book');
        bookDiv.innerHTML = `<h3>${book.title}</h3><p>Author: ${book.author}</p>`;
        recommendationsContainer.appendChild(bookDiv);
    });
});

function searchBooks() {
    const query = document.getElementById('search').value;
    // Perform search logic here
    alert('Searching for: ' + query);
}
