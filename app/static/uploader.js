// Get DOM elements
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const uploadButton = document.getElementById('uploadButton');
const fileCountSpan = document.getElementById('fileCount');
const dropZone = document.getElementById('dropZone');
const form = document.getElementById('uploadForm');
const clearAllButton = document.getElementById('clearAllButton');

// Prevent defaults for drag events
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Add/remove highlight class for drag and drop
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropZone.classList.add('drag-over');
}

function unhighlight(e) {
    dropZone.classList.remove('drag-over');
}

// Handle dropped files
dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = [...dt.files];
    
    // Filter for .srt files
    const srtFiles = files.filter(file => file.name.toLowerCase().endsWith('.srt'));
    
    if (srtFiles.length === 0) {
        alert('Please drop only .srt files');
        return;
    }
    
    // Update file input with dropped files
    const dataTransfer = new DataTransfer();
    srtFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
    
    // Trigger change event to update UI
    fileInput.dispatchEvent(new Event('change'));
}

// Create a variable to store all files
let allFiles = new DataTransfer();

// Update UI when files are selected
fileInput.addEventListener('change', () => {
    // Add new files to existing collection
    Array.from(fileInput.files).forEach(file => {
        // Check for duplicates
        const isDuplicate = Array.from(allFiles.files)
            .some(existing => existing.name === file.name);
        
        if (!isDuplicate) {
            allFiles.items.add(file);
        }
    });
    
    // Update file input with combined files
    fileInput.files = allFiles.files;
    
    // Update UI
    fileList.innerHTML = '';
    const fileCount = allFiles.files.length;
    
    // Update file count text
    fileCountSpan.textContent = fileCount === 0 ? 'No files selected' : 
                               fileCount === 1 ? '1 file selected' :
                               `${fileCount} files selected`;
    
    // Display file list
    for (const file of allFiles.files) {
        const li = document.createElement('li');
        
        const fileName = document.createElement('span');
        fileName.className = 'file-name';
        fileName.textContent = file.name;
        
        const removeButton = document.createElement('span');
        removeButton.className = 'remove-file';
        removeButton.innerHTML = '<i class="fas fa-times"></i>';
        removeButton.addEventListener('click', () => removeFile(file.name));
        
        li.appendChild(fileName);
        li.appendChild(removeButton);
        fileList.appendChild(li);
    }
    
    // Enable/disable upload button
    uploadButton.disabled = fileCount === 0;
    clearAllButton.style.display = fileCount === 0 ? 'none' : 'inline-flex';
});

// Update removeFile function to use allFiles
function removeFile(fileName) {
    const newFiles = new DataTransfer();
    
    Array.from(allFiles.files).forEach(file => {
        if (file.name !== fileName) {
            newFiles.items.add(file);
        }
    });
    
    allFiles = newFiles;
    fileInput.files = allFiles.files;
    fileInput.dispatchEvent(new Event('change'));
}

// Update clearFileList function
function clearFileList() {
    fileList.innerHTML = '';
    fileInput.value = '';
    allFiles = new DataTransfer();
    uploadButton.disabled = true;
    fileCountSpan.textContent = 'No files selected';
    clearAllButton.style.display = 'none';
}

// Update clearAllButton handler
clearAllButton.addEventListener('click', () => {
    allFiles = new DataTransfer();
    fileInput.value = '';
    fileInput.dispatchEvent(new Event('change'));
});

// Update handleDrop function
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = [...dt.files];
    
    // Filter for .srt files
    const srtFiles = files.filter(file => file.name.toLowerCase().endsWith('.srt'));
    
    if (srtFiles.length === 0) {
        alert('Please drop only .srt files');
        return;
    }
    
    // Add dropped files to existing files
    srtFiles.forEach(file => {
        // Check for duplicates
        const isDuplicate = Array.from(allFiles.files)
            .some(existing => existing.name === file.name);
        
        if (!isDuplicate) {
            allFiles.items.add(file);
        }
    });
    
    fileInput.files = allFiles.files;
    fileInput.dispatchEvent(new Event('change'));
}

// Handle form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (fileInput.files.length === 0) return;

    // Disable upload button and show loading state
    uploadButton.disabled = true;
    uploadButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

    try {
        const formData = new FormData();
        for (const file of fileInput.files) {
            formData.append('files[]', file);
        }

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Get the filename from the Content-Disposition header if possible
            const contentDisposition = response.headers.get('Content-Disposition');
            const filename = contentDisposition ? 
                contentDisposition.split('filename=')[1].replace(/"/g, '') : 
                'processed_files.zip';

            // Create a blob from the response
            const blob = await response.blob();
            
            // Create a download link and trigger it
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            document.body.removeChild(a);

            // Clear both the fileInput and allFiles
            allFiles = new DataTransfer(); // Add this line
            clearFileList();
            uploadButton.innerHTML = '<i class="fas fa-upload"></i> Upload & Process';
        } else {
            throw new Error('Upload failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during upload. Please try again.');
        uploadButton.disabled = false;
        uploadButton.innerHTML = '<i class="fas fa-upload"></i> Upload & Process';
    }
});

// Clear file list after form submission
function clearFileList() {
    fileList.innerHTML = '';
    fileInput.value = '';
    uploadButton.disabled = true;
    fileCountSpan.textContent = 'No files selected';
    clearAllButton.style.display = 'none';
}

// Clear all files button handler
clearAllButton.addEventListener('click', () => {
    fileInput.value = '';
    fileInput.dispatchEvent(new Event('change'));
});

// Initialize clear button visibility
clearAllButton.style.display = 'none';