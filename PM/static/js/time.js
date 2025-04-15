// Date Picker
document.addEventListener('DOMContentLoaded', function () {
    const selectors = [
      '#id_task_start_date',    
      '#id_task_due_date'       
    ];
  
    selectors.forEach(selector => {
      flatpickr(selector, {
        dateFormat: "m/d/Y",  
        allowInput: true,
        minDate: new Date(2000, 0, 1)
      });
  
      const input = document.querySelector(selector);
      if (input) {
        input.addEventListener('input', function () {
          const parts = input.value.split('/');
          if (parts[2] && parts[2].length > 4) {
            parts[2] = parts[2].slice(0, 4);
            input.value = parts.join('/');
          }
        });
      }
    });
  });
  