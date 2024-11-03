function submitContactForm() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    alert('Submitting contact form\n' +
          'Name: ' + name + '\n' +
          'Email: ' + email + '\n' +
          'Message: ' + message);
    // Implement actual form submission functionality here
}
