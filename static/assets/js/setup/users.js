
const editUserFormContainer = document.getElementById('edit-user-form-container')
const usersTable = document.getElementById('users-table')
const usersTablePagination = document.getElementById('users-table-pagination')
const createUserFormContainer = document.getElementById('create-user-form-container')
const deleteUserModal = document.getElementById('delete-user-modal')
const acceptDeleteUserBtn = document.getElementById('accept-delete-user')

const deleteBootstrapModal = new bootstrap.Modal(deleteUserModal)

acceptDeleteUserBtn.addEventListener('click', e => {
  e.preventDefault()
  const id = deleteUserModal.getAttribute('data-id')
  deleteUser(id)
    .then(response => {
      if (response.status == 'success') {
        deleteBootstrapModal.hide()
        showToast('Éxito', response.message, 'success')
        deleteUserModal.removeAttribute('data-id')
      } else {
        showToast('Error', response.message, 'error')
      }
      refreshUsersTable()
    })
    

})

function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

if (createUserFormContainer)
  bindServerForm('/auth/create-user', createUserFormContainer, refreshUsersTable)

else
  showToast('Error', 'Hubo un error al cargar la página.', 'error')

let page = 1
let search = ''

const searchUser = document.getElementById('search-user')
let timeoutId = 0
searchUser.addEventListener('keyup', (e) => {
  clearTimeout(timeoutId)
  console.log('Changing')

  search = e.target.value

  timeoutId = setTimeout(() => {
    refreshUsersTable()
  }, 500)
})

function createPaginationItem(content, number, active, disabled) {
  const li = document.createElement('li')
  li.classList.add('page-item')
  const a = document.createElement('a')
  a.classList.add('page-link')
  if (active && !disabled) {
    li.classList.add('active')
  } else if (disabled) {
    li.classList.add('disabled')
  }
  a.innerHTML = content

  a.addEventListener('click', e => {
    e.preventDefault()
    page = number
    refreshUsersTable()
  })
  
  li.appendChild(a)
  return li
}

function createPaginationList() {
  const ul = document.createElement('ul')
  ul.classList.add('pagination')
  ul.classList.add('justify-content-end')
  ul.classList.add('mb-0')
  return ul
}
const actionsDropdown = (id) => {
  const dropdownDiv = document.createElement('div');
  dropdownDiv.classList.add('dropdown');

  const button = document.createElement('button');
  button.classList.add('btn', 'bg-brand-color-2', 'text-light', 'dropdown-toggle');
  button.setAttribute('type', 'button');
  button.setAttribute('data-bs-toggle', 'dropdown');
  button.setAttribute('aria-expanded', 'false');
  button.textContent = 'Acciones';

  const dropdownMenu = document.createElement('ul');
  dropdownMenu.classList.add('dropdown-menu');

  const editItem = document.createElement('li');
  const editButton = document.createElement('button');
  editButton.classList.add('dropdown-item');
  editButton.setAttribute('data-bs-toggle', 'modal');
  editButton.setAttribute('data-bs-target', '#edit-user-modal');
  editButton.innerHTML = `
    <span class="text-warning">Editar
      <span class="pc-micon text-light"><i data-feather="user-plus"></i></span>
    </span>`;

  editButton.addEventListener('click', e => {
    e.preventDefault()
    editUserFormContainer.innerHTML = ''
    bindServerForm(`auth/edit-user/${id}`,editUserFormContainer, refreshUsersTable, 'PUT')

  })
  editItem.appendChild(editButton);

  const deleteItem = document.createElement('li');
  const deleteButton = document.createElement('button');
  deleteButton.classList.add('dropdown-item');



  deleteButton.addEventListener('click', e => {
    e.preventDefault()
    deleteBootstrapModal.show()
    deleteUserModal.setAttribute('data-id', id)
  })

  deleteButton.innerHTML = `
    <span class="text-danger">Eliminar</span>
    <span class="pc-micon"><i data-feather="user-plus"></i></span>`;
  deleteItem.appendChild(deleteButton);

  dropdownMenu.appendChild(editItem);
  dropdownMenu.appendChild(deleteItem);

  dropdownDiv.appendChild(button);
  dropdownDiv.appendChild(dropdownMenu);

  return dropdownDiv;
};



function refreshUsersTable(){
  usersTable.innerHTML = ''
  usersTablePagination.innerHTML = ''
  getUsers(page, search)
  .then(response => {
    const headers = response.headers
    const data = response.data 

    if (usersTable) {
      // Create table headers
      const thead = document.createElement('thead');
      const headerRow = document.createElement('tr');
      Object.keys(headers).forEach(key => {
        const th = document.createElement('th');
        th.textContent = headers[key];
        headerRow.appendChild(th);
      });
      const rowActions = document.createElement('th')
      rowActions.textContent = 'Acciones'
      headerRow.appendChild(rowActions)
      thead.appendChild(headerRow);
      usersTable.appendChild(thead);

      // Create table body
      const tbody = document.createElement('tbody');
      data.forEach(row => {
        const tr = document.createElement('tr');
        Object.keys(headers).forEach(key => {
          const td = document.createElement('td');
          const value = row[key]

          if (typeof value == "string") {
            const date = new Date(value);
            if (!isNaN(date.getTime())) {
              td.textContent = date.toLocaleString(); // Format the date if valid
            } else {
              td.textContent = value; // Keep the original value if not a valid date
            }
          }
          else {
            td.textContent = value? value : '--'; // Use empty string if key is missing
          }

          tr.appendChild(td);
        });
        const rowActions = document.createElement('td')
        rowActions.appendChild(actionsDropdown(row.id))
        tr.appendChild(rowActions)
        tbody.appendChild(tr);
      });
      
      usersTable.appendChild(tbody);

      const pagination = response.pagination
      const paginationList = createPaginationList()
      usersTablePagination.appendChild(paginationList)

      const maxPagesToDisplay = 5
      const currentPage = pagination.current_page
      
      let remainingPages = pagination.num_pages - 1
      let remainingPagesToDisplay = maxPagesToDisplay - 1
      
      const pagesToDisplay = [currentPage]
      
      for (let i = 1; remainingPages > 0 && remainingPagesToDisplay > 0; i++) {
        const left = currentPage - i
        const right = currentPage + i
        
        if (left > 0) {
          pagesToDisplay.unshift(left)
          remainingPages--
          remainingPagesToDisplay--
        }
        
        if (right <= pagination.num_pages) {
          pagesToDisplay.push(right)
          remainingPages--
          remainingPagesToDisplay--
        }
      }


      const goToFirst = createPaginationItem(`<<`, 1, false, currentPage == 1)
      paginationList.appendChild(goToFirst)
      
      
      pagesToDisplay.forEach((pageNum) => {
        const li = createPaginationItem(pageNum, pageNum, pageNum == pagination.current_page)
        paginationList.appendChild(li)
      })
      const goToLast = createPaginationItem('>>', pagination.num_pages, false, currentPage == pagination.num_pages)
      paginationList.appendChild(goToLast)


      
    } else {
      showToast('Error', 'No se pudo encontrar la tabla de usuarios.', 'error');
    }
    


  })
}



refreshUsersTable(1)
