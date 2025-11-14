// Amélioration de l'expérience utilisateur pour les formulaires

document.addEventListener('DOMContentLoaded', function() {
    
    // 0. FORCE IMMEDIATE DE LA COULEUR NOIRE POUR TOUS LES INPUTS
    function forceBlackTextColor() {
        const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="password"], input[type="number"], input[type="url"], textarea, select');
        
        inputs.forEach(input => {
            // Force la couleur via JavaScript avec priorité maximale
            input.style.setProperty('color', '#000000', 'important');
            input.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
            input.style.setProperty('-moz-text-fill-color', '#000000', 'important');
            
            // Observer les changements de valeur pour maintenir la couleur
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' && (mutation.attributeName === 'style' || mutation.attributeName === 'class')) {
                        input.style.setProperty('color', '#000000', 'important');
                        input.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
                    }
                });
            });
            
            observer.observe(input, {
                attributes: true,
                attributeFilter: ['style', 'class']
            });
            
            // Force la couleur à chaque interaction
            ['input', 'change', 'focus', 'blur', 'keyup'].forEach(eventType => {
                input.addEventListener(eventType, function() {
                    setTimeout(() => {
                        this.style.setProperty('color', '#000000', 'important');
                        this.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
                    }, 10);
                });
            });
        });
    }
    
    // Exécuter immédiatement
    forceBlackTextColor();
    
    // Re-exécuter après un court délai pour s'assurer que Tailwind est chargé
    setTimeout(forceBlackTextColor, 100);
    setTimeout(forceBlackTextColor, 500);
    setTimeout(forceBlackTextColor, 1000);
    
    // 1. Animation progressive des éléments du formulaire
    function animateFormElements() {
        const formGroups = document.querySelectorAll('.form-group');
        
        formGroups.forEach((group, index) => {
            group.style.opacity = '0';
            group.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                group.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                group.style.opacity = '1';
                group.style.transform = 'translateY(0)';
            }, index * 150); // Délai progressif
        });
    }
    
    // 2. Validation en temps réel
    function setupRealTimeValidation() {
        const inputs = document.querySelectorAll('.form-input, .form-select, .form-textarea');
        
        inputs.forEach(input => {
            // Validation au focus out
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            // Validation pendant la frappe (avec délai)
            let timeoutId;
            input.addEventListener('input', function() {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    validateField(this);
                }, 500);
            });
        });
    }
    
    function validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';
        
        // Validation selon le type de champ
        switch(fieldName) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (value && !emailRegex.test(value)) {
                    isValid = false;
                    errorMessage = 'Format d\'email invalide';
                }
                break;
                
            case 'phone':
                const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
                if (value && !phoneRegex.test(value)) {
                    isValid = false;
                    errorMessage = 'Format de téléphone invalide';
                }
                break;
                
            case 'complaint_name':
                if (value.length < 2) {
                    isValid = false;
                    errorMessage = 'Le nom doit contenir au moins 2 caractères';
                }
                break;
                
            case 'description':
                if (value.length < 10) {
                    isValid = false;
                    errorMessage = 'La description doit contenir au moins 10 caractères';
                }
                break;
        }
        
        // Appliquer les styles de validation
        showFieldValidation(field, isValid, errorMessage);
        return isValid;
    }
    
    function showFieldValidation(field, isValid, errorMessage) {
        const formGroup = field.closest('.form-group');
        let errorElement = formGroup.querySelector('.field-error');
        
        // Supprimer les classes d'erreur existantes
        field.classList.remove('border-red-500', 'border-green-500');
        
        if (!isValid && errorMessage) {
            // Ajouter styles d'erreur
            field.classList.add('border-red-500');
            
            // Créer ou mettre à jour le message d'erreur
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'field-error text-red-500 text-sm mt-1';
                formGroup.appendChild(errorElement);
            }
            errorElement.textContent = errorMessage;
            
        } else if (isValid && field.value.trim()) {
            // Ajouter styles de succès
            field.classList.add('border-green-500');
            
            // Supprimer le message d'erreur
            if (errorElement) {
                errorElement.remove();
            }
        } else {
            // Supprimer le message d'erreur pour champ vide
            if (errorElement) {
                errorElement.remove();
            }
        }
    }
    
    // 3. Géolocalisation améliorée avec auto-fill de l'adresse
    function setupGeolocation() {
        // Connecter au bouton existant dans le template
        const useLocationBtn = document.getElementById('locationBtn');
        if (useLocationBtn) {
            // Supprimer l'ancien event listener s'il existe
            useLocationBtn.onclick = null;
            useLocationBtn.addEventListener('click', function(e) {
                e.preventDefault();
                getCurrentLocationAndFillAddress();
            });
        }
        
        // Aussi connecter si le bouton a un ID différent
        const useLocationBtn2 = document.getElementById('useLocationBtn');
        if (useLocationBtn2) {
            useLocationBtn2.addEventListener('click', function(e) {
                e.preventDefault();
                getCurrentLocationAndFillAddress();
            });
        }
        
        // Auto-géolocalisation discrète si disponible
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    // Remplir les champs cachés
                    const latField = document.getElementById('latitude');
                    const lngField = document.getElementById('longitude');
                    
                    if (latField && lngField) {
                        latField.value = latitude;
                        lngField.value = longitude;
                    }
                    
                    console.log('Position auto-détectée:', latitude, longitude);
                },
                function(error) {
                    console.log('Auto-géolocalisation échouée:', error.message);
                },
                {
                    enableHighAccuracy: false,
                    timeout: 5000,
                    maximumAge: 300000
                }
            );
        }
    }
    
    function getCurrentLocationAndFillAddress() {
        // Chercher le bouton existant dans le template
        const useLocationBtn = document.getElementById('locationBtn') || document.getElementById('useLocationBtn');
        
        if (!navigator.geolocation) {
            showAlert('La géolocalisation n\'est pas supportée par votre navigateur', 'error');
            return;
        }
        
        // Afficher l'état de chargement
        if (useLocationBtn) {
            useLocationBtn.disabled = true;
            const originalHTML = useLocationBtn.innerHTML;
            useLocationBtn.innerHTML = '🔄 Localisation...';
            
            // Stocker l'HTML original pour le restaurer plus tard
            useLocationBtn.originalHTML = originalHTML;
        }
        
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                
                // Remplir les champs de coordonnées cachés
                const latField = document.getElementById('latitude');
                const lngField = document.getElementById('longitude');
                
                if (latField && lngField) {
                    latField.value = latitude;
                    lngField.value = longitude;
                }
                
                // Obtenir l'adresse via geocoding inverse
                reverseGeocode(latitude, longitude);
                
                showLocationStatus(true, '📍 Position utilisée avec succès !');
                
                // Remettre le bouton en état normal
                if (useLocationBtn) {
                    useLocationBtn.disabled = false;
                    useLocationBtn.innerHTML = useLocationBtn.originalHTML || '📍 Ma position';
                }
            },
            function(error) {
                let errorMessage = 'Erreur de localisation';
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = '🚫 Autorisation de localisation refusée. Activez la géolocalisation dans votre navigateur.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = '❌ Position non disponible. Vérifiez votre connexion GPS.';
                        break;
                    case error.TIMEOUT:
                        errorMessage = '⏰ Délai de localisation dépassé. Réessayez.';
                        break;
                }
                
                showAlert(errorMessage, 'error');
                
                // Remettre le bouton en état normal
                if (useLocationBtn) {
                    useLocationBtn.disabled = false;
                    useLocationBtn.innerHTML = useLocationBtn.originalHTML || '📍 Ma position';
                }
            },
            {
                enableHighAccuracy: true,
                timeout: 15000,
                maximumAge: 60000
            }
        );
    }
    
    function reverseGeocode(latitude, longitude) {
        // Utiliser l'API de geocoding gratuite Nominatim (OpenStreetMap)
        const url = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json&accept-language=fr`;
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.display_name) {
                    fillAddressFields(data);
                    showAlert('Adresse récupérée automatiquement !', 'success');
                } else {
                    showAlert('Impossible de récupérer l\'adresse automatiquement', 'warning');
                }
            })
            .catch(error => {
                console.error('Erreur geocoding:', error);
                showAlert('Erreur lors de la récupération de l\'adresse', 'warning');
            });
    }
    
    function fillAddressFields(data) {
        const address = data.address || {};
        const displayName = data.display_name || '';
        
        // Remplir le champ adresse principal (chercher les deux noms possibles)
        const addressField = document.querySelector('input[name="address"]') || document.querySelector('input[name="adresse"]');
        if (addressField) {
            // Construire une adresse lisible
            let fullAddress = '';
            
            if (address.house_number) fullAddress += address.house_number + ' ';
            if (address.road) fullAddress += address.road + ', ';
            if (address.suburb || address.neighbourhood) {
                fullAddress += (address.suburb || address.neighbourhood) + ', ';
            }
            if (address.city || address.town || address.village) {
                fullAddress += (address.city || address.town || address.village);
            }
            
            // Fallback sur display_name si construction échoue
            if (!fullAddress.trim()) {
                fullAddress = displayName.split(',').slice(0, 3).join(', ');
            }
            
            addressField.value = fullAddress.trim();
            addressField.dispatchEvent(new Event('input')); // Déclencher la validation
            
            // Animation visuelle pour montrer le champ rempli
            addressField.style.backgroundColor = '#dcfce7';
            addressField.style.transition = 'background-color 0.5s ease';
            setTimeout(() => {
                addressField.style.backgroundColor = '';
            }, 2000);
        }
        
        // Essayer de remplir automatiquement la commune
        const communeField = document.querySelector('select[name="commune"]');
        if (communeField && (address.city || address.state)) {
            const cityName = address.city || address.state;
            const options = Array.from(communeField.options);
            const matchingOption = options.find(option => 
                option.text.toLowerCase().includes(cityName.toLowerCase()) ||
                cityName.toLowerCase().includes(option.text.toLowerCase())
            );
            
            if (matchingOption) {
                communeField.value = matchingOption.value;
                communeField.dispatchEvent(new Event('change'));
                
                // Animation de mise à jour
                communeField.style.backgroundColor = '#dcfce7';
                setTimeout(() => {
                    communeField.style.backgroundColor = '';
                }, 1500);
                
                showAlert(`Commune détectée: ${matchingOption.text}`, 'success');
            }
        }
        
        // Essayer de remplir le quartier
        setTimeout(() => {
            const quartierField = document.querySelector('select[name="quartier"]');
            if (quartierField && (address.suburb || address.neighbourhood)) {
                const neighbourhood = address.suburb || address.neighbourhood;
                const options = Array.from(quartierField.options);
                const matchingOption = options.find(option => 
                    option.text.toLowerCase().includes(neighbourhood.toLowerCase()) ||
                    neighbourhood.toLowerCase().includes(option.text.toLowerCase())
                );
                
                if (matchingOption) {
                    quartierField.value = matchingOption.value;
                    quartierField.dispatchEvent(new Event('change'));
                    
                    // Animation de mise à jour
                    quartierField.style.backgroundColor = '#dcfce7';
                    setTimeout(() => {
                        quartierField.style.backgroundColor = '';
                    }, 1500);
                    
                    showAlert(`Quartier détecté: ${matchingOption.text}`, 'success');
                }
            }
        }, 800); // Délai pour laisser le temps aux quartiers de se charger
    }
    
    function showLocationStatus(success, customMessage) {
        const message = customMessage || (success ? 'Localisation activée' : 'Localisation non disponible');
        const statusDiv = document.createElement('div');
        statusDiv.className = `alert ${success ? 'alert-success' : 'alert-warning'} fixed top-4 right-4 z-50 max-w-sm`;
        statusDiv.style.animation = 'slideInRight 0.5s ease-out';
        
        statusDiv.innerHTML = `
            <div class="flex items-center">
                <span class="mr-2">${success ? '📍' : '⚠️'}</span>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-auto text-gray-500 hover:text-gray-700">×</button>
            </div>
        `;
        
        document.body.appendChild(statusDiv);
        
        // Auto-remove après 4 secondes
        setTimeout(() => {
            statusDiv.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => statusDiv.remove(), 500);
        }, 4000);
    }
    
    // 4. Aperçu d'image amélioré
    function setupImagePreview() {
        const fileInput = document.querySelector('input[type="file"][name="photo"]');
        if (!fileInput) return;
        
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            // Validation du fichier
            if (!file.type.startsWith('image/')) {
                showAlert('Veuillez sélectionner une image valide', 'error');
                fileInput.value = '';
                return;
            }
            
            if (file.size > 5 * 1024 * 1024) { // 5MB
                showAlert('L\'image ne doit pas dépasser 5MB', 'error');
                fileInput.value = '';
                return;
            }
            
            // Créer l'aperçu
            const reader = new FileReader();
            reader.onload = function(e) {
                showImagePreview(e.target.result, file.name, file.size);
            };
            reader.readAsDataURL(file);
        });
    }
    
    function showImagePreview(src, name, size) {
        const previewContainer = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImg');
        
        if (previewContainer && previewImg) {
            previewImg.src = src;
            previewContainer.classList.remove('hidden');
            
            // Ajouter informations sur le fichier
            const fileInfo = document.createElement('div');
            fileInfo.className = 'text-sm text-gray-600 mt-2 text-center';
            fileInfo.innerHTML = `
                <p><strong>${name}</strong></p>
                <p>${(size / 1024 / 1024).toFixed(2)} MB</p>
            `;
            
            // Supprimer l'ancienne info si elle existe
            const oldInfo = previewContainer.querySelector('.file-info');
            if (oldInfo) oldInfo.remove();
            
            fileInfo.className += ' file-info';
            previewContainer.appendChild(fileInfo);
        }
    }
    
    // 5. Soumission de formulaire avec feedback
    function setupFormSubmission() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                // Valider tous les champs
                const inputs = form.querySelectorAll('.form-input, .form-select, .form-textarea');
                let isFormValid = true;
                
                inputs.forEach(input => {
                    if (!validateField(input)) {
                        isFormValid = false;
                    }
                });
                
                if (!isFormValid) {
                    e.preventDefault();
                    showAlert('Veuillez corriger les erreurs dans le formulaire', 'error');
                    return;
                }
                
                // Afficher l'état de chargement
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    showLoadingState(submitBtn);
                }
            });
        });
    }
    
    function showLoadingState(button) {
        button.disabled = true;
        button.classList.add('btn-loading', 'opacity-75');
        
        // Afficher le spinner
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.classList.remove('hidden');
        }
    }
    
    // 6. Système d'alertes
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} fixed top-4 right-4 z-50 max-w-sm`;
        alertDiv.style.animation = 'slideInRight 0.5s ease-out';
        
        alertDiv.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-gray-500 hover:text-gray-700">×</button>
            </div>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove après 5 secondes
        setTimeout(() => {
            alertDiv.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => alertDiv.remove(), 500);
        }, 5000);
    }
    
    // 7. Mise à jour dynamique des quartiers
    function setupCommuneQuartierDependency() {
        const communeSelect = document.querySelector('select[name="commune"]');
        const quartierSelect = document.querySelector('select[name="quartier"]');
        
        if (!communeSelect || !quartierSelect) return;
        
        communeSelect.addEventListener('change', function() {
            updateQuartiers(this.value, quartierSelect);
        });
    }
    
    function updateQuartiers(commune, quartierSelect) {
        // Reset
        quartierSelect.innerHTML = '<option value="">Sélectionnez un quartier...</option>';
        
        // Données des quartiers (à adapter selon votre structure)
        const quartiersByCommune = {
            'Kinshasa': ['Gombe', 'Kalamu', 'Lingwala', 'Bandalungwa', 'Kasa-Vubu'],
            'Lubumbashi': ['Kenya', 'Katuba', 'Annexe', 'Kampemba'],
            'Kananga': ['Katoka', 'Nganza', 'Salongo']
        };
        
        const quartiers = quartiersByCommune[commune] || [];
        
        quartiers.forEach(quartier => {
            const option = document.createElement('option');
            option.value = quartier;
            option.textContent = quartier;
            quartierSelect.appendChild(option);
        });
        
        // Animation de mise à jour
        quartierSelect.style.transform = 'scale(1.05)';
        setTimeout(() => {
            quartierSelect.style.transform = 'scale(1)';
        }, 200);
    }
    
    // 8. Sauvegarde automatique en brouillon (localStorage)
    function setupAutosave() {
        const form = document.getElementById('signalementForm');
        if (!form) return;
        
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Charger la valeur sauvegardée
            const savedValue = localStorage.getItem(`draft_${input.name}`);
            if (savedValue && !input.value) {
                input.value = savedValue;
            }
            
            // Sauvegarder à chaque modification
            input.addEventListener('input', function() {
                localStorage.setItem(`draft_${this.name}`, this.value);
            });
        });
        
        // Nettoyer lors de la soumission
        form.addEventListener('submit', function() {
            inputs.forEach(input => {
                localStorage.removeItem(`draft_${input.name}`);
            });
        });
    }
    
    // Initialisation de tous les modules
    function init() {
        animateFormElements();
        setupRealTimeValidation();
        setupGeolocation();
        setupImagePreview();
        setupFormSubmission();
        setupCommuneQuartierDependency();
        setupAutosave();
        
        console.log('✅ Formulaire amélioré initialisé');
    }
    
    // Démarrer l'initialisation
    init();
});

// Animations CSS supplémentaires
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);