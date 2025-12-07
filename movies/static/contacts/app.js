const { createApp } = Vue;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

// Convert data-* attributes to Vue directives so HTML stays W3C-valid
function transformDataAttributes(root) {
    const walker = root.querySelectorAll('[data-model], [data-if], [data-else], [data-for], [data-key], [data-onclick], [data-onsubmit], [data-bind-disabled], [data-bind-class], [data-if], [data-else]');
    walker.forEach(el => {
        // v-model
        if (el.hasAttribute('data-model')) {
            el.setAttribute('v-model', el.getAttribute('data-model'));
            el.removeAttribute('data-model');
        }
        // v-if / v-else
        if (el.hasAttribute('data-if')) {
            el.setAttribute('v-if', el.getAttribute('data-if'));
            el.removeAttribute('data-if');
        }
        if (el.hasAttribute('data-else')) {
            el.setAttribute('v-else', '');
            el.removeAttribute('data-else');
        }
        // v-for and v-bind:key
        if (el.hasAttribute('data-for')) {
            el.setAttribute('v-for', el.getAttribute('data-for'));
            el.removeAttribute('data-for');
        }
        if (el.hasAttribute('data-key')) {
            el.setAttribute('v-bind:key', el.getAttribute('data-key'));
            el.removeAttribute('data-key');
        }
        // v-on:click
        if (el.hasAttribute('data-onclick')) {
            el.setAttribute('v-on:click', el.getAttribute('data-onclick'));
            el.removeAttribute('data-onclick');
        }
        // @submit with optional modifier 'prevent'
        if (el.hasAttribute('data-onsubmit')) {
            const handler = el.getAttribute('data-onsubmit');
            const mod = el.getAttribute('data-onsubmit-modifier');
            // Can't set attribute names with a dot ('.') in the DOM
            // so set a normal @submit and, when 'prevent' is requested,
            // use an inline expression that calls $event.preventDefault()
            // before invoking the handler.
            if (mod === 'prevent') {
                el.setAttribute('v-on:submit', "$event.preventDefault(); " + handler + "()");
            } else {
                el.setAttribute('v-on:submit', handler);
            }
            el.removeAttribute('data-onsubmit');
            if (mod) el.removeAttribute('data-onsubmit-modifier');
        }
        // v-bind:disabled and v-bind:class
        if (el.hasAttribute('data-bind-disabled')) {
            el.setAttribute('v-bind:disabled', el.getAttribute('data-bind-disabled'));
            el.removeAttribute('data-bind-disabled');
        }
        if (el.hasAttribute('data-bind-class')) {
            el.setAttribute('v-bind:class', el.getAttribute('data-bind-class'));
            el.removeAttribute('data-bind-class');
        }
    });
}

// Mounting after transforming attributes
document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('app');
    if (root) transformDataAttributes(root);

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
});
