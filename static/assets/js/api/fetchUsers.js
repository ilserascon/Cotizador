async function getUsers(page){
  const response = await fetch(`/auth/get-users?page=${page}`)

  try {
    const json = await response.json()
    return json
  } catch(err){
    showToast('Error', err.message | 'Hubo un error inesperado', 'error')
  }
}