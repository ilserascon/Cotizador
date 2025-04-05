async function getUsers(page=1, search=''){
  const response = await fetch(`/auth/get-users?page=${page}&search=${search}`)

  try {
    const json = await response.json()
    return json
  } catch(err){
    showToast('Error', err.message | 'Hubo un error inesperado', 'error')
  }
}