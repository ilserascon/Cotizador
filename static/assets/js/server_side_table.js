async function appTableRequest(endpoint) {
  const response = await fetch(endpoint)
  const json = await response.json()

  return json
}

async function bindServerTable(endpoint, container){
  try {
    const json = await appTableRequest(endpoint)
    const data = json.data
    
    const tableContainer = document.createElement('div')
    tableContainer.className = 'table-responsive'

    const table = document.createElement('table')
    table.className = 'table'

    const thead = document.createElement('thead')

    


  }
  catch(err) {
    showToast(err.name || 'Error', err.message || 'Hubo un error', 'error')
  }

}