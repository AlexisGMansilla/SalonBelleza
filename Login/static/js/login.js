document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelector('.toggle-password');
    const passwordField = document.querySelector('#id_password');

    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.querySelector('ion-icon').setAttribute('name', type === 'password' ? 'eye-outline' : 'eye-off-outline');
        });
    }
});