document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const resultContainer = document.getElementById('result-container');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);

        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function displayResults(data) {
        resultContainer.innerHTML = '';
        const objects = data.objects;

        if (objects.length === 0) {
            resultContainer.innerHTML = '<p>No objects detected.</p>';
            return;
        }

        const resultList = document.createElement('ul');
        objects.forEach(obj => {
            const listItem = document.createElement('li');
            listItem.textContent = `${obj.name}: ${JSON.stringify(obj.features)}`;
            resultList.appendChild(listItem);
        });

        resultContainer.appendChild(resultList);
    }

    document.getElementById('viewJsonBtn').addEventListener('click', function() {
        const jsonContainer = document.getElementById('jsonContainer');
        const jsonContent = document.getElementById('jsonContent');
        
        // Toggle visibility
        if (jsonContainer.classList.contains('hidden')) {
            // Fetch JSON data
            fetch('/view_json')
                .then(response => response.json())
                .then(data => {
                    // Format the JSON with indentation
                    const formattedJson = JSON.stringify(data, null, 2);
                    jsonContent.textContent = formattedJson;
                    jsonContainer.classList.remove('hidden');
                    this.textContent = 'Hide JSON Analysis';
                })
                .catch(error => {
                    jsonContent.textContent = 'Error loading JSON data: ' + error;
                    jsonContainer.classList.remove('hidden');
                });
        } else {
            jsonContainer.classList.add('hidden');
            this.textContent = 'View Complete JSON Analysis';
        }
    });
});