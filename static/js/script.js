document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const predictionForm = document.getElementById('prediction-form');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(event) {
            const inputs = predictionForm.querySelectorAll('input[type="number"]');
            let isValid = true;
            
            inputs.forEach(input => {
                // Reset previous validation
                input.classList.remove('error');
                const errorMsg = input.parentElement.querySelector('.error-message');
                if (errorMsg) {
                    errorMsg.remove();
                }
                
                // Check if input is empty or not a number
                if (input.value === '' || isNaN(parseFloat(input.value))) {
                    isValid = false;
                    input.classList.add('error');
                    
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'error-message';
                    errorMessage.textContent = 'Mohon masukkan nilai yang valid';
                    input.parentElement.appendChild(errorMessage);
                }
                
                // Check if value is in the expected range
                const value = parseFloat(input.value);
                if (value < 0 || value > 100) {
                    isValid = false;
                    input.classList.add('error');
                    
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'error-message';
                    errorMessage.textContent = 'Nilai harus antara 0 dan 100';
                    input.parentElement.appendChild(errorMessage);
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Quick fill feature (for demo purposes)
    const quickFillButton = document.getElementById('quick-fill');
    
    if (quickFillButton) {
        quickFillButton.addEventListener('click', function() {
            // Example values for a "Layak" prediction
            const demoValues = {
                'Makhraj': 85,
                'BTQ': 85,
                'Tayamum': 85,
                'Wudhu': 85,
                'Bacaan': 85,
                'Gerakan': 85,
                'S. Jenazah': 85,
                'shalat': 85,
                'Total': 85
            };
            
            // Fill form with demo values
            for (const [field, value] of Object.entries(demoValues)) {
                const input = document.getElementById(field);
                if (input) {
                    input.value = value;
                }
            }
        });
    }
    
    // Result page - copy results
    const copyResultButton = document.getElementById('copy-result');
    
    if (copyResultButton) {
        copyResultButton.addEventListener('click', function() {
            const resultText = document.getElementById('result-text').textContent;
            const confidenceText = document.getElementById('confidence-text').textContent;
            
            const textToCopy = `Hasil Prediksi: ${resultText}\n${confidenceText}`;
            
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    // Show copy success message
                    const copyMsg = document.createElement('div');
                    copyMsg.className = 'copy-success';
                    copyMsg.textContent = 'Hasil berhasil disalin!';
                    copyResultButton.parentElement.appendChild(copyMsg);
                    
                    // Remove message after 2 seconds
                    setTimeout(() => {
                        copyMsg.remove();
                    }, 2000);
                })
                .catch(err => {
                    console.error('Gagal menyalin teks:', err);
                });
        });
    }
});