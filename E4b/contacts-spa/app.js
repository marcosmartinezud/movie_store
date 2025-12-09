import { createApp, ref, computed, onMounted } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
import { VueFire, VueFireFirestoreOptionsAPI, useCollection } from 'https://unpkg.com/vuefire@3.2.2/dist/index.mjs';
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.3.1/firebase-app.js';
import { getFirestore, collection, addDoc, deleteDoc, doc, serverTimestamp, query, orderBy } from 'https://www.gstatic.com/firebasejs/11.3.1/firebase-firestore.js';
import { firebaseConfig, hasFirebaseConfig } from './firebase-config.js';

// Convierte atributos data-* en directivas Vue (HTML válido W3C)
function transformDataAttributes(root) {
  const walker = root.querySelectorAll('[data-model], [data-if], [data-else], [data-for], [data-key], [data-onclick], [data-onsubmit], [data-bind-disabled], [data-bind-class]');
  walker.forEach(el => {
    if (el.hasAttribute('data-model')) {
      el.setAttribute('v-model', el.getAttribute('data-model'));
      el.removeAttribute('data-model');
    }
    if (el.hasAttribute('data-if')) {
      el.setAttribute('v-if', el.getAttribute('data-if'));
      el.removeAttribute('data-if');
    }
    if (el.hasAttribute('data-else')) {
      el.setAttribute('v-else', '');
      el.removeAttribute('data-else');
    }
    if (el.hasAttribute('data-for')) {
      el.setAttribute('v-for', el.getAttribute('data-for'));
      el.removeAttribute('data-for');
    }
    if (el.hasAttribute('data-key')) {
      el.setAttribute('v-bind:key', el.getAttribute('data-key'));
      el.removeAttribute('data-key');
    }
    if (el.hasAttribute('data-onclick')) {
      el.setAttribute('v-on:click', el.getAttribute('data-onclick'));
      el.removeAttribute('data-onclick');
    }
    if (el.hasAttribute('data-onsubmit')) {
      const handler = el.getAttribute('data-onsubmit');
      const mod = el.getAttribute('data-onsubmit-modifier');
      const expr = mod === 'prevent' ? `$event.preventDefault(); ${handler}()` : handler;
      el.setAttribute('v-on:submit', expr);
      el.removeAttribute('data-onsubmit');
      if (mod) el.removeAttribute('data-onsubmit-modifier');
    }
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

// Inicializa Firebase solo si el archivo de configuracion tiene datos
function setupFirebase() {
  if (!hasFirebaseConfig()) {
    return { ready: false, reason: 'Config de Firebase incompleta' };
  }
  try {
    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);
    return { ready: true, app, db, reason: '' };
  } catch (error) {
    return { ready: false, reason: error.message };
  }
}

const firebaseState = setupFirebase();

document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('app');
  if (root) transformDataAttributes(root);

  const app = createApp({
    setup() {
      const usingFirebase = firebaseState.ready;
      // Estado reactivo basico para el formulario y mensajes
      const form = ref({ name: '', email: '', phone: '' });
      const loading = ref(false);
      const message = ref('');
      const messageType = ref('');

      const collectionRef = usingFirebase ? collection(firebaseState.db, 'contacts') : null;
      const contacts = usingFirebase ? useCollection(query(collectionRef, orderBy('createdAt', 'desc'))) : ref([]);

      const contactsList = computed(() => (contacts.value ? contacts.value : []));
      const persistenceLabel = computed(() => (usingFirebase ? 'Firebase (Vuefire)' : 'Firebase no configurado'));

      const createContact = async () => {
        // Valida campos y guarda el nuevo contacto en la coleccion
        if (!form.value.name || !form.value.email || !form.value.phone) {
          message.value = 'Completa todos los campos';
          messageType.value = 'error';
          return;
        }
        if (!usingFirebase) {
          message.value = 'Configura firebase-config.js para usar Firestore';
          messageType.value = 'error';
          return;
        }
        loading.value = true;
        message.value = '';
        try {
          await addDoc(collectionRef, {
            name: form.value.name,
            email: form.value.email,
            phone: form.value.phone,
            createdAt: serverTimestamp(),
          });
          message.value = 'Contacto guardado';
          messageType.value = 'success';
          form.value = { name: '', email: '', phone: '' };
        } catch (error) {
          message.value = error.message;
          messageType.value = 'error';
        } finally {
          loading.value = false;
        }
      };

      const deleteContact = async (id) => {
        // Borra un documento por id despues de confirmarlo con el usuario
        if (!id) return;
        if (!confirm('¿Eliminar este contacto?')) return;
        if (!usingFirebase) {
          message.value = 'Configura firebase-config.js para usar Firestore';
          messageType.value = 'error';
          return;
        }
        loading.value = true;
        message.value = '';
        try {
          await deleteDoc(doc(collectionRef, id));
          message.value = 'Contacto eliminado';
          messageType.value = 'success';
        } catch (error) {
          message.value = error.message;
          messageType.value = 'error';
        } finally {
          loading.value = false;
        }
      };

      onMounted(() => {
        if (!usingFirebase && firebaseState.reason) {
          message.value = 'Firebase deshabilitado: ' + firebaseState.reason;
          messageType.value = 'error';
        }
      });

      const refresh = async () => {
        // Solo muestra un aviso porque Vuefire ya mantiene la suscripcion activa
        if (!usingFirebase) {
          message.value = 'Configura firebase-config.js para usar Firestore';
          messageType.value = 'error';
          return;
        }
        message.value = 'Sincronizado con Firebase';
        messageType.value = 'success';
      };

      return {
        form,
        loading,
        message,
        messageType,
        contacts: contactsList,
        createContact,
        deleteContact,
        fetchContacts: refresh,
        persistenceLabel,
        usingFirebase,
      };
    },
  });

  if (firebaseState.ready) {
    app.use(VueFire, {
      firebaseApp: firebaseState.app,
      modules: [VueFireFirestoreOptionsAPI()],
    });
  }

  app.mount('#app');
});
