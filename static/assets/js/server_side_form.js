async function appFormRequest(endpoint, formData, method = 'POST') {
  const url = new URL(window.location)
  url.pathname = endpoint
  console.log(url.toString())
  
  const response = await fetch(url, {
    method,
    body: formData
  })

  try {
    const json = await response.json()
    return json
  } catch (err) {
    showToast('Error', 'Hubo un error', 'danger')
    return { 'status': 'error', 'data': 'Hubo un error' }
  }
}


function formEventListener(endpoint, form, method = 'POST', extraData = {}, afterSubmit) {
  form.addEventListener('submit', e => {
    e.preventDefault()
    const formData = new FormData(e.target)

    Object.entries(extraData).forEach(([key, value]) => {
      formData.append(key, value)
    })

    appFormRequest(endpoint, formData, method, extraData)
      .then(json => {

        switch (json.status) {
          case 'error':
            const fieldsWithError = Object.keys(json.data)
            const inputsInForm = form.querySelectorAll('input')

            for (const input of inputsInForm) {
              if (input.classList.contains('is-invalid')) {
                input.classList.remove('is-invalid')
              }
            
            }
            
            for (const fieldWithError of fieldsWithError) {
              const inputField = form.querySelector(`[name="${fieldWithError}"]`)

              if (!inputField) continue;

              if (inputField.classList.contains('is-valid')) {
                inputField.classList.remove('is-valid')
              }

              if (!inputField.classList.contains('is-invalid')) {
                inputField.classList.add('is-invalid')
              }

              const errorFeedback = inputField.parentNode.querySelector('.invalid-feedback')
              errorFeedback.innerHTML = json.data[fieldWithError][0]


            }

            break;

          case 'success':
            const inputs = form.querySelectorAll('input')

            for (const input of inputs) {
              if (input.classList.contains('is-invalid')) {
                input.classList.remove('is-invalid')
              }
            }

            showToast(json.title, json.message, 'success')

            form.reset()

            const parent = form.parentElement

            if (parent.classList.contains('modal-body')) {
              const modalParent = parent.parentElement

              if (!modalParent) { return }

              const button = modalParent.querySelector('[data-bs-dismiss="modal"]')
              button.click()
            }

            break;
        }

      })
      .catch(err => {
        console.log(err)
        showToast('Error', 'Hubo un error inesperado', 'error')
      })
      .finally(() => {
        afterSubmit && afterSubmit()
      })

  })
}


const createPersonFormContainer = document.getElementById('form-container')

class FieldStrategy {
  createField(name, config) {
      throw new Error("createField method must be implemented");
  }
}

class TimeFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const input = document.createElement('input');
      input.type = 'time';
      input.className = 'form-control';
      input.required = config.required;
      input.placeholder = config.label || name;

      const label = document.createElement('label');
      label.textContent = config.label || name;

      if (config.initial)
        input.value = config.initial;
        

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}

class DateFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const input = document.createElement('input');
      input.type = 'date';
      input.className = 'form-control';
      input.required = config.required;
      input.placeholder = config.label || name;

      const label = document.createElement('label');
      label.textContent = config.label || name;

      if (config.initial)
        input.value = config.initial;

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}

class FileFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'mb-3';

      const input = document.createElement('input');
      input.type = 'file';
      input.className = 'form-control';
      input.required = config.required;

      const label = document.createElement('label');
      label.textContent = config.label || name;
      label.className = 'form-label';

      div.appendChild(label);
      div.appendChild(input);
      return div;
  }
}

class EmailFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const input = document.createElement('input');
      input.type = 'email';
      input.className = 'form-control';
      input.maxLength = config.max_length;
      input.required = config.required;
      input.placeholder = config.label || name;

      const label = document.createElement('label');
      label.textContent = config.label || name;

      if (config.initial)
        input.value = config.initial;
        

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}

class BooleanFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-check mb-3';

      const input = document.createElement('input');
      input.type = 'checkbox';
      input.className = 'form-check-input';
      input.required = config.required;

      const label = document.createElement('label');
      label.className = 'form-check-label';
      label.textContent = config.label || name;

      if (config.initial)
        input.value = config.initial;

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}

class TextFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const input = document.createElement('input');
      input.type = config.type; // Supports "text" or "password"
      input.className = 'form-control';
      if (config.atts.max_length)
        input.maxLength = config.atts.max_length;
      if (config.atts.min_length)
        input.minLength = config.atts.min_length;
      input.required = config.required;
      input.placeholder = config.label || name;

      if (config.initial)
        input.value = config.initial;
        

      const label = document.createElement('label');
      label.textContent = config.label || name;

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}

class PasswordFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const input = document.createElement('input');
      input.type = config.type; // Supports "text" or "password"
      input.className = 'form-control';
      if (config.atts.max_length)
        input.maxLength = config.atts.max_length;
      if (config.atts.min_length)
        input.minLength = config.atts.min_length;
      input.required = config.required;
      input.placeholder = config.label || name;

      const label = document.createElement('label');
      label.textContent = config.label || name;

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}

class TextareaFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const textarea = document.createElement('textarea');
      textarea.className = 'form-control';
      if (config.atts.max_length)
        textarea.maxLength = config.atts.max_length;
      if (config.atts.min_length)
        textarea.minLength = config.atts.min_length;
      textarea.required = config.required;
      textarea.placeholder = config.label || name;

      const label = document.createElement('label');
      label.textContent = config.label || name;

      div.appendChild(textarea);
      div.appendChild(label);
      return div;
  }
}

class NumberFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const input = document.createElement('input');
      input.type = config.type;
      input.className = 'form-control';
      input.min = config.min;
      input.max = config.max;
      input.required = config.required;
      input.placeholder = config.label || name;

      const label = document.createElement('label');
      label.textContent = config.label || name;

      if (config.initial)
        input.value = config.initial;

      div.appendChild(input);
      div.appendChild(label);
      return div;
  }
}



class SelectFieldStrategy extends FieldStrategy {
  createField(name, config) {
      const div = document.createElement('div');
      div.className = 'form-floating mb-3';

      const select = document.createElement('select');
      select.className = 'form-select';
      config.atts.choices.forEach(choice => {
          const option = document.createElement('option');
          option.value = choice[0];
          option.textContent = choice[1];
          select.appendChild(option);

          if (config.initial != null && config.initial == choice[0]){
            option.selected = true;
          }

      });
      select.required = config.required;

      const label = document.createElement('label');
      label.textContent = config.label || name;



      div.appendChild(select);
      div.appendChild(label);
      return div;
  }
}

class FieldContext {
  constructor(strategy) {
      this.strategy = strategy;
  }

  setStrategy(strategy) {
      this.strategy = strategy;
  }

  renderField(name, config) {
      return this.strategy.createField(name, config);
  }
}

function bindServerForm(endpoint, container, afterSubmit, method = 'POST', extraData = {}) {
  const token = getCSRFToken()
  const url = new URL(window.location)
  url.pathname = endpoint
  fetch(url, {
    method: 'GET',
    headers: {
      'X-CSRFToken': token,
      ...extraData
    }
  })
      .then(response => response.json())
      .then(data => {
          const form = document.createElement('form');

          const token = data.token

          if (token){
            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'csrfmiddlewaretoken';
            tokenInput.value = token;
            form.appendChild(tokenInput);
          }

          form.className = 'needs-validation';
          form.noValidate = true;

          const context = new FieldContext();

          Object.entries(data.form).forEach(([name, config]) => {
              let strategy;

              switch (config.type) {
                case 'password':
                    strategy = new PasswordFieldStrategy();
                    break;
                case 'text':
                    strategy = new TextFieldStrategy();
                    break;
                case 'textarea':
                    strategy = new TextareaFieldStrategy();
                    break;
                case 'number':
                    strategy = new NumberFieldStrategy();
                    break;
                case 'select':
                    strategy = new SelectFieldStrategy();
                    break;
                case 'time':
                    strategy = new TimeFieldStrategy();
                    break;
                case 'date':
                    strategy = new DateFieldStrategy();
                    break;
                case 'file':
                    strategy = new FileFieldStrategy();
                    break;
                case 'email':
                    strategy = new EmailFieldStrategy();
                    break;
                case 'checkbox':
                    strategy = new BooleanFieldStrategy();
                    break;
                default:
                    return;
            }

              context.setStrategy(strategy);
              const field = context.renderField(name, config);
              const invalidFeedback = document.createElement('div')
              invalidFeedback.classList.add('invalid-feedback')
              field.appendChild(invalidFeedback)

              field.querySelector('input, textarea, select').name = name;
              form.appendChild(field);
          });
          
          if(container)
            container.appendChild(form);

          const submitButton = document.createElement('button');
          submitButton.type = 'submit';
          submitButton.className = 'btn btn-primary';
          submitButton.textContent = 'Guardar';
          
          form.appendChild(submitButton);

          formEventListener(endpoint, form, method, extraData, afterSubmit)

          return form;
      })
      .catch(console.error);
}
