const { createApp } = Vue;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

createApp({
    data() {
        return {
            contacts: [],
            form: {
                name: '',
                email: '',
                phone: ''
            },
            loading: false,
            message: '',
            messageType: '',
            csrfToken: getCookie('csrftoken')
        };
    },
    created() {
        this.fetchContacts();
    },
    methods: {
        async fetchContacts() {
            this.loading = true;
            this.message = '';
            try {
                const response = await fetch('/movies/api/contacts/', {
                    headers: this.buildHeaders(),
                    credentials: 'same-origin'
                });
                if (!response.ok) throw new Error('No se pudieron cargar los contactos');
                this.contacts = await response.json();
            } catch (error) {
                this.message = error.message;
                this.messageType = 'error';
            } finally {
                this.loading = false;
            }
        },
        async createContact() {
            if (!this.csrfToken) this.csrfToken = getCookie('csrftoken');
            if (!this.csrfToken) {
                this.message = 'Token CSRF no disponible';
                this.messageType = 'error';
                return;
            }

            this.loading = true;
            this.message = '';
            try {
                const response = await fetch('/movies/api/contacts/', {
                    method: 'POST',
                    headers: this.buildHeaders(true),
                    credentials: 'same-origin',
                    body: JSON.stringify(this.form)
                });
                if (!response.ok) {
                    const text = await response.text();
                    throw new Error(text || 'Error al crear');
                }
                this.message = 'Contacto guardado';
                this.messageType = 'success';
                this.form = { name: '', email: '', phone: '' };
                await this.fetchContacts();
            } catch (error) {
                this.message = error.message;
                this.messageType = 'error';
            } finally {
                this.loading = false;
            }
        },
        async deleteContact(id) {
            if (!confirm('¿Eliminar este contacto?')) return;
            if (!this.csrfToken) this.csrfToken = getCookie('csrftoken');
            if (!this.csrfToken) {
                this.message = 'Token CSRF no disponible';
                this.messageType = 'error';
                return;
            }

            this.loading = true;
            this.message = '';
            try {
                const response = await fetch(`/movies/api/contacts/${id}/`, {
                    method: 'DELETE',
                    headers: this.buildHeaders(),
                    credentials: 'same-origin'
                });
                if (!response.ok) throw new Error('No se pudo eliminar');
                this.message = 'Contacto eliminado';
                this.messageType = 'success';
                await this.fetchContacts();
            } catch (error) {
                this.message = error.message;
                this.messageType = 'error';
            } finally {
                this.loading = false;
            }
        },
        buildHeaders(includeJson = false) {
            const headers = {};
            if (this.csrfToken) {
                headers['X-CSRFToken'] = this.csrfToken;
            }
            if (includeJson) {
                headers['Content-Type'] = 'application/json';
            }
            return headers;
        }
    }
}).mount('#app');
