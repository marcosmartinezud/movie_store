const { createApp } = Vue;

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
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
            messageType: ''
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
            this.loading = true;
            this.message = '';
            try {
                const response = await fetch('/movies/api/contacts/', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(this.form)
                });
                if (!response.ok) {
                    const json = await response.json().catch(() => null);
                    const detail = json?.error || json?.detail || 'Error al crear';
                    throw new Error(detail);
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
            this.loading = true;
            this.message = '';
            try {
                const response = await fetch(`/movies/api/contacts/${id}/`, {
                    method: 'DELETE',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
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
        }
    }
}).mount('#app');
