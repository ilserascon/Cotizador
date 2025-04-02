const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
const toastContainer = document.getElementById('toast-container')

function showToast(title, content, type) {
  const id = `toast-${new Date().getTime()}`

  let classNames = ""

  switch (type) {
    case "success":
      classNames = "text-bg-success"
      break

    case "error":
      classNames = "text-bg-danger"
      break
  }

  const toast = `
<div id="${id}" class="toast ${classNames}" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
      <strong class="me-auto">${title}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
     ${content}
    </div>
  </div>
`
  toastContainer.innerHTML += toast
  const toastElement = document.getElementById(id)
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastElement)
  toastBootstrap.show()
}


