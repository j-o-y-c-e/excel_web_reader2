document.addEventListener('DOMContentLoaded', function() {
    // Get HTML elements by their IDs
    const categorySelect = document.getElementById('category');
    const columnSelect = document.getElementById('column');
    const itemsList = document.getElementById('items-list');
    
    // Check if all required elements exist
    if (!categorySelect || !columnSelect || !itemsList) {
        console.error('HTML elements not found:', {
            category: !!categorySelect,
            column: !!columnSelect,
            itemsList: !!itemsList
        });
        return;
    }
    
    // Load available categories from server
    fetch('/get_categories')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear and populate category dropdown
                categorySelect.innerHTML = '<option value="">-- Choose an option --</option>';
                data.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category;
                    option.textContent = category;
                    categorySelect.appendChild(option);
                });
            } else {
                console.error('Error loading categories:', data.error);
            }
        })
        .catch(error => console.error('Network error:', error));
    
    // Handle category selection change
    categorySelect.addEventListener('change', function() {
        const selectedCategory = this.value;
        columnSelect.innerHTML = '<option value="">-- Select a column --</option>';
        itemsList.innerHTML = '';
        
        if (!selectedCategory) return;
        
        // Load columns for selected category
        const formData = new FormData();
        formData.append('category', selectedCategory);
        
        fetch('/get_columns', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                columnSelect.disabled = false;
                data.columns.forEach(column => {
                    const option = document.createElement('option');
                    option.value = column;
                    option.textContent = column;
                    columnSelect.appendChild(option);
                });
            } else {
                console.error('Error loading columns:', data.error);
            }
        })
        .catch(error => console.error('Network error:', error));
    });
    
    // Handle column selection change
    columnSelect.addEventListener('change', function() {
        const selectedCategory = categorySelect.value;
        const selectedColumn = this.value;
        itemsList.innerHTML = '';
        
        if (!selectedCategory || !selectedColumn) return;
        
        // Load items from selected column
        const formData = new FormData();
        formData.append('category', selectedCategory);
        formData.append('column_name', selectedColumn);
        
        fetch('/get_items', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display items in the list
                data.items.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.textContent = item;
                    itemsList.appendChild(listItem);
                });
            } else {
                const errorItem = document.createElement('li');
                errorItem.textContent = 'Error: ' + data.error;
                itemsList.appendChild(errorItem);
            }
        })
        .catch(error => {
            console.error('Network error:', error);
            itemsList.innerHTML = '<li>Error loading data</li>';
        });
    });
});
