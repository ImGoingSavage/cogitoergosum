/**
 * cuentaUI.js — Portada de login y UI de sincronización opcional.
 *
 * Extraído de app.js (oleada 5). Principios que se conservan:
 *  - La cuenta es SIEMPRE opcional (§0.7): configurarLogin() jamás bloquea.
 *  - LocalStorage es la verdad inmediata; el servidor es respaldo.
 *  - despuesDeEntrar() une/adopta el progreso y luego llama al callback
 *    _onEntrado para que app.js repinte las vistas de sesión y fresh start.
 */

import * as Storage from './storage.js';
import * as Api from './api.js';
import * as Sync from './sync.js';
import * as Study from './study.js';

const $ = (id) => document.getElementById(id);

// Callback inyectado por app.js: repinta sesión y fresh start tras login.
let _onEntrado = () => {};

export function iniciar(onEntrado) {
  _onEntrado = onEntrado;
}

/* -------- Portada abierta desde fuera (botón ⏻ del header) ----------- */

let _abrirPortada = () => {};

/** Reabre la portada de login desde cualquier punto de app.js. */
export function abrirPortada() {
  _abrirPortada();
}

/* ====================== Cuenta (tarjeta Dashboard) ==================== */

export function renderizar() {
  const { sesion, pendientes, ultimaSync } = Sync.estado();
  $('cuenta-anonima').hidden = Boolean(sesion);
  $('cuenta-activa').hidden = !sesion;
  $('btn-header-salir').hidden = !sesion; // ⏻ existe solo con sesión activa
  if (sesion) {
    $('sync-usuario').textContent = sesion.email ?? '(cuenta activa)';
    const hora = ultimaSync ? new Date(ultimaSync).toLocaleString() : 'aún no';
    $('sync-estado-linea').textContent =
      `${pendientes} evento(s) pendiente(s) de subir · última sincronización: ${hora}.`;
  }
}

function mensaje(texto) {
  $('sync-mensaje').textContent = texto;
}

/** Tras login/registro: baja o une el estado del servidor y refresca todo. */
export async function despuesDeEntrar() {
  mensaje('Sesión iniciada. Revisando tu progreso en el servidor…');
  try {
    const resultado = await Sync.adoptarOUnir();
    if (resultado === 'adoptado') {
      mensaje('Progreso descargado del servidor: este dispositivo quedó al día.');
    } else if (resultado === 'unido') {
      mensaje('Progreso local y del servidor unidos; las rachas se recalcularon.');
    } else {
      mensaje(
        'Tu cuenta aún no tiene datos en el servidor. Usa «Importar mi progreso local» para subir lo de este dispositivo.'
      );
    }
  } catch {
    mensaje('Sesión iniciada (no se pudo consultar el servidor; se reintentará solo).');
  }
  Sync.sincronizar();
  // Estado pudo cambiar (rachas, historial): repintar lo visible
  Study.actualizarHeaderRachas();
  _onEntrado(); // renderizarSesion() + actualizarFreshStartUI() de app.js
  renderizar();
}

/* ====================== Portada de inicio de sesión =================== */

/**
 * Portada con video (login.mp4) y vidrio líquido. Aparece al abrir la app
 * solo si no hay sesión y el usuario no eligió "continuar sin cuenta".
 * Jamás bloquea: la cuenta es opcional (§0.7).
 */
export function configurarLogin() {
  const pantalla = $('pantalla-login');
  const video = $('login-video');
  const reducido = window.matchMedia('(prefers-reduced-motion: reduce)');

  const ajustarVideo = () => {
    if (pantalla.hidden || reducido.matches || document.visibilityState === 'hidden') {
      video.pause();
      return;
    }
    video.defaultPlaybackRate = 0.3;
    video.playbackRate = 0.3;
    video.play().catch(() => {});
  };
  video.addEventListener('loadedmetadata', () => { video.playbackRate = 0.3; });
  document.addEventListener('visibilitychange', ajustarVideo);
  reducido.addEventListener?.('change', ajustarVideo);

  const msgLogin = (texto) => { $('login-mensaje').textContent = texto; };

  _abrirPortada = () => {
    msgLogin('');
    pantalla.hidden = false;
    ajustarVideo();
  };

  const cerrar = () => {
    pantalla.hidden = true;
    video.pause();
  };

  const creds = () => ({
    email: $('login-email').value.trim(),
    password: $('login-password').value,
  });

  $('btn-login-omitir').addEventListener('click', () => {
    Storage.save('loginOmitido', true);
    cerrar();
  });

  $('btn-login-google').addEventListener('click', () => {
    msgLogin('Redirigiendo a Google…');
    Api.loginConGoogle();
  });

  $('btn-login-entrar').addEventListener('click', async () => {
    const { email, password } = creds();
    if (!email || !password) { msgLogin('Escribe tu correo y contraseña.'); return; }
    msgLogin('Iniciando sesión…');
    try {
      await Api.iniciarSesion(email, password);
      cerrar();
      await despuesDeEntrar();
    } catch (e) {
      msgLogin(`No se pudo iniciar sesión: ${e.message}`);
    }
  });

  $('btn-login-registrar').addEventListener('click', async () => {
    const { email, password } = creds();
    if (!email || password.length < 8) {
      msgLogin('Escribe tu correo y una contraseña de al menos 8 caracteres.');
      return;
    }
    msgLogin('Creando cuenta…');
    try {
      const sesion = await Api.registrar(email, password);
      if (sesion) {
        cerrar();
        await despuesDeEntrar();
      } else {
        msgLogin('Cuenta creada. Revisa tu correo para confirmarla y vuelve a entrar.');
      }
    } catch (e) {
      msgLogin(`No se pudo crear la cuenta: ${e.message}`);
    }
  });

  // Al abrir la app: portada solo si no hay sesión y no se eligió "sin cuenta"
  if (!Api.sesionActual() && !Storage.load('loginOmitido')) abrirPortada();
}

/* ====================== Tarjeta "Mi cuenta" (Dashboard) =============== */

export function configurarCuenta() {
  renderizar();
  Sync.alCambiarEstado(renderizar);

  const creds = () => ({
    email: $('sync-email').value.trim(),
    password: $('sync-password').value,
  });

  $('btn-sync-registrar').addEventListener('click', async () => {
    const { email, password } = creds();
    if (!email || password.length < 8) {
      mensaje('Escribe tu correo y una contraseña de al menos 8 caracteres.');
      return;
    }
    mensaje('Creando cuenta…');
    try {
      const sesion = await Api.registrar(email, password);
      if (sesion) {
        await despuesDeEntrar();
      } else {
        mensaje('Cuenta creada. Revisa tu correo para confirmarla y luego inicia sesión.');
      }
    } catch (e) {
      mensaje(`No se pudo crear la cuenta: ${e.message}`);
    }
  });

  $('btn-sync-entrar').addEventListener('click', async () => {
    const { email, password } = creds();
    if (!email || !password) { mensaje('Escribe tu correo y contraseña.'); return; }
    mensaje('Iniciando sesión…');
    try {
      await Api.iniciarSesion(email, password);
      await despuesDeEntrar();
    } catch (e) {
      mensaje(`No se pudo iniciar sesión: ${e.message}`);
    }
  });

  $('btn-sync-ahora').addEventListener('click', async () => {
    mensaje('Sincronizando…');
    await Sync.sincronizar();
    const { pendientes } = Sync.estado();
    mensaje(pendientes === 0 ? 'Todo sincronizado.' : `Quedaron ${pendientes} evento(s) en cola; se reintentará solo.`);
  });

  $('btn-sync-importar').addEventListener('click', async () => {
    mensaje('Subiendo tu progreso local…');
    const { pendientes } = await Sync.migrarProgresoLocal();
    mensaje(
      pendientes === 0
        ? 'Progreso importado a tu cuenta: rachas, historial, fichas e insignias ya están respaldados.'
        : 'El progreso quedó en cola (sin conexión ahora); se subirá solo al volver la red.'
    );
  });

  $('btn-sync-salir').addEventListener('click', async () => {
    await Api.cerrarSesion();
    mensaje('Sesión cerrada. Tus datos locales siguen intactos en este dispositivo.');
    renderizar();
  });

  // ⏻ del header: cierra sesión y vuelve a la portada
  $('btn-header-salir').addEventListener('click', async () => {
    await Api.cerrarSesion();
    mensaje('Sesión cerrada. Tus datos locales siguen intactos en este dispositivo.');
    renderizar();
    abrirPortada();
  });

  // Borrar cuenta: exactamente 2 clics, sin súplicas (§0.1)
  $('btn-sync-borrar').addEventListener('click', async () => {
    const seguro = window.confirm(
      'Esto borra tu cuenta y TODOS tus datos del servidor (no los de este dispositivo). ¿Continuar?'
    );
    if (!seguro) return;
    try {
      await Api.borrarCuenta();
      mensaje('Cuenta borrada del servidor. Tus datos locales siguen en este dispositivo.');
    } catch (e) {
      mensaje(`No se pudo borrar: ${e.message}`);
    }
    renderizar();
  });

  // Exportar funciona con o sin cuenta: es 100% local (§0.1, 2 clics)
  $('btn-exportar-datos').addEventListener('click', () => {
    const datos = {};
    Storage.CLAVES_SYNC.forEach((k) => { datos[k] = Storage.load(k); });
    const blob = new Blob([JSON.stringify(datos, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `cogitoergosum-datos-${Storage.hoy()}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    mensaje('Datos exportados (las API keys de Claude no se incluyen: viven solo en este dispositivo).');
  });
}
