export function registerServiceWorker() {
  if (!import.meta.env.PROD) return

  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault()
    window.deferredPwaInstallPrompt = event
    window.dispatchEvent(new Event('pwa-installable'))
  })

  if (!('serviceWorker' in navigator)) return

  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js').catch((error) => {
      console.error('Unable to register the service worker.', error)
    })
  })
}
