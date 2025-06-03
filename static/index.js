document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    const fileNameDisplay = document.getElementById('file-name');

    dropArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            previewImage(file);
            fileNameDisplay.textContent = `Selected file: ${file.name}`;
        }
    });

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.style.border = '2px dashed #023047';
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.style.border = 'none';
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.style.border = 'none';
        const file = event.dataTransfer.files[0];
        if (file) {
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;

            previewImage(file);
            fileNameDisplay.textContent = `Selected file: ${file.name}`;
        }
    });

    document.addEventListener('paste', (event) => {
        const items = (event.clipboardData || event.originalEvent.clipboardData).items;
        for (const item of items) {
            if (item.kind === 'file') {
                const file = item.getAsFile();
                const dt = new DataTransfer();
                dt.items.add(file);
                fileInput.files = dt.files;

                previewImage(file);
                fileNameDisplay.textContent = `Selected file: ${file.name}`;
                break;
            }
        }
    });

    function previewImage(file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            preview.src = event.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});
