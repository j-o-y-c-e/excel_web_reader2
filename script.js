document.getElementById('category').addEventListener('change', function() {
    const category = this.value;
    const itemsList = document.getElementById('items-list');
    
    if (!category) {
        itemsList.innerHTML = '';
        return;
    }
    
    // Show loading state
    itemsList.innerHTML = '<li>Loading...</li>';
    
    // Make AJAX request to backend
    const formData = new FormData();
    formData.append('category', category);
    formData.append('file', new File([""], "dummy.xlsx"));
    (async () => {
        try{
    
            const response = await fetch('/get_items/', {
            method: 'POST',
            body: formData
    });
    const data = await response.json();
        if (data.success) {
            // Display items
            itemsList.innerHTML = '';
            data.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                itemsList.appendChild(li);
            });
        } else {
            itemsList.innerHTML = `<li>Error: ${data.error}</li>`;
        }
    } catch(error ) {
        itemsList.innerHTML = `<li>Error: ${error.message}</li>`;
        }
    })();
});