document.addEventListener('DOMContentLoaded', () => {
  const editModal = document.getElementById('edit-modal-overlay');
  const editForm = document.getElementById('edit-task-form');
  const editTitle = document.getElementById('edit-title');
  const editDueDate = document.getElementById('edit-due-date');
  const editCancel = document.getElementById('edit-modal-cancel');

  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', () => {
      const taskId = btn.dataset.taskId;
      const title = btn.dataset.taskTitle;
      const dueDate = btn.dataset.taskDueDate;

      editForm.action = `/tasks/${taskId}/edit`;
      editTitle.value = title;
      editDueDate.value = dueDate || '';

      editModal.classList.add('open');
    });
  });

  if (editCancel) {
    editCancel.addEventListener('click', () => editModal.classList.remove('open'));
  }

  if (editModal) {
    editModal.addEventListener('click', (e) => {
      if (e.target === editModal) editModal.classList.remove('open');
    });
  }
});
