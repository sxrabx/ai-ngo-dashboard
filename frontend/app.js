document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const reportText = document.getElementById('reportInput').value;
    const loader = document.getElementById('loader');
    const emptyState = document.getElementById('emptyState');
    const resultsData = document.getElementById('resultsData');
    const btn = document.getElementById('analyzeBtn');

    if (!reportText.trim()) {
        alert("Please enter a field report to analyze.");
        return;
    }

    // UI state: loading
    btn.disabled = true;
    loader.classList.remove('hidden');
    emptyState.classList.add('hidden');
    resultsData.classList.add('hidden');

    try {
        // Prepare mock volunteers to send to the FastAPI engine
        const mockVolunteers = [
            { id: "V1", name: "Dr. Sarah Chen", skills: ["Medical", "Trauma"], energy: 95 },
            { id: "V2", name: "Mike Johnson", skills: ["Rescue", "Logistics"], energy: 100 },
            { id: "V3", name: "Emma Davis", skills: ["Medical", "Pediatrics"], energy: 85 }
        ];

        // Call the FastAPI backend running on port 8000
        const response = await fetch('http://localhost:8000/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task: { task_id: `T-${Date.now()}`, description: reportText },
                volunteers: mockVolunteers
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();

        // Populate the UI
        document.getElementById('priorityScore').innerText = data.priority_score || '90';
        document.getElementById('taskCategory').innerText = data.category || 'Emergency';
        
        const frTrans = data.extracted_task?.translations?.fr;
        document.getElementById('frTranslation').innerText = frTrans || 'Traduction non disponible.';

        // Populate squad with cascade animation
        const squadList = document.getElementById('squadList');
        squadList.innerHTML = '';
        
        const members = data.assigned_squad?.members || mockVolunteers;
        members.forEach((m, index) => {
            const li = document.createElement('li');
            li.style.animationDelay = `${index * 0.15}s`;
            li.style.animation = 'fadeInUp 0.5s ease backwards';
            li.innerHTML = `
                <span class="name"><i class="fa-solid fa-user-astronaut"></i> ${m.name}</span>
                <span class="role">${m.role || 'Responder'}</span>
            `;
            squadList.appendChild(li);
        });

        // Hide loader, show results
        loader.classList.add('hidden');
        resultsData.classList.remove('hidden');

    } catch (error) {
        console.error("Error calling AI API:", error);
        alert("Failed to connect to the FastAPI backend. Make sure uvicorn is running on port 8000!");
        loader.classList.add('hidden');
        emptyState.classList.remove('hidden');
    } finally {
        btn.disabled = false;
    }
});
