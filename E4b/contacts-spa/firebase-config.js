export const firebaseConfig = {
  apiKey: "AIzaSyBp-KgGuT1h0qaqE7OaQG5quc7-vKUqEJM",
  authDomain: "agenda-spa-9544c.firebaseapp.com",
  projectId: "agenda-spa-9544c",
  storageBucket: "agenda-spa-9544c.firebasestorage.app",
  messagingSenderId: "419946805766",
  appId: "1:419946805766:web:624cc61ef95bb81bb5e187"
};

export function hasFirebaseConfig() {
  // Solo devuelve true si hay datos minimos para inicializar Firebase
  return Boolean(
    firebaseConfig.apiKey &&
    firebaseConfig.appId &&
    firebaseConfig.projectId &&
    firebaseConfig.messagingSenderId
  );
}
