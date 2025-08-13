document.addEventListener('DOMContentLoaded', () => {
    const numberDisplay = document.getElementById('number-display');
    const chineseCharDisplay = document.getElementById('chinese-char');
    const recordButton = document.getElementById('record-button');
    const stopButton = document.getElementById('stop-button');
    const resultDisplay = document.getElementById('result-display');

    let mediaRecorder;
    let audioChunks = [];
    let currentNumberData = {};

    // Fetch a new number from the backend
    async function fetchNumber() {
        numberDisplay.innerHTML = '<span class="spinner"></span>';
        chineseCharDisplay.textContent = '';
        resultDisplay.textContent = '';

        try {
            const response = await fetch('/api/number');
            if (!response.ok) throw new Error('Network response was not ok');

            currentNumberData = await response.json();
            numberDisplay.textContent = currentNumberData.number;
            chineseCharDisplay.textContent = currentNumberData.chinese;
        } catch (error) {
            numberDisplay.textContent = 'Error';
            console.error('Error fetching number:', error);
        }
    }

    // Start recording audio
    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = sendAudio;

            audioChunks = [];
            mediaRecorder.start();

            recordButton.textContent = 'Recording...';
            recordButton.classList.add('recording');
            stopButton.disabled = false;
            recordButton.disabled = true;
        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Could not access microphone. Please allow microphone permissions.');
        }
    }

    // Stop recording
    function stopRecording() {
        mediaRecorder.stop();
        recordButton.textContent = 'Record';
        recordButton.classList.remove('recording');
        stopButton.disabled = true;
        recordButton.disabled = false;
    }

    // Send audio to the backend for assessment
    async function sendAudio() {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob);
        formData.append('number', currentNumberData.number);
        formData.append('chinese', currentNumberData.chinese);

        resultDisplay.innerHTML = 'Evaluating... <span class="spinner"></span>';

        try {
            const response = await fetch('/api/pronounce', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const result = await response.json();
            displayResult(result);
        } catch (error) {
            resultDisplay.textContent = 'Error evaluating pronunciation.';
            console.error('Error sending audio:', error);
        }
    }

    // Display the pronunciation result
    function displayResult(result) {
        let content = `Accuracy Score: ${result.accuracyScore}%`;
        if (result.errorType && result.errorType !== 'None') {
            content += `<br>Feedback: ${result.errorType}`;
        }
        resultDisplay.innerHTML = content;
        // After showing result, maybe fetch a new number automatically?
        // For now, user can click a "Next" button (to be added) or we can fetch automatically.
        setTimeout(fetchNumber, 3000); // Load a new number after 3 seconds
    }

    // Event listeners
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);

    // Initial load
    fetchNumber();
});
