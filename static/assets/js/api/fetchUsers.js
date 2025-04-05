async function getUsers(page=1, search=''){
  const response = await fetch(`/auth/get-users?page=${page}&search=${search}`)

  try {
    const json = await response.json()
    return json
  } catch(err){
    showToast('Error', err.message | 'Hubo un error inesperado', 'error')
  }
}

async function deleteUser(id){
  const response = await fetch(`/auth/delete-user/${id}`, {
    method: 'DELETE',
    headers: {
      'X-CSRF-TOKEN': getCSRFToken()
    }
  })

  try {
    const json = await response.json()
    return json
  } catch(err){
    showToast('Error', err.message | 'Hubo un error inesperado', 'error')
  }
}