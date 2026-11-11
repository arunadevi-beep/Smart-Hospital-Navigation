/**
 * Hospital Indoor Navigation System - Master Controller
 * Features:
 * 1. Travel Modes: Walk, Wheelchair (Lifts only), Stretcher (Bed Lifts only)
 * 2. Audio Voice Guidance: Strictly ON DEMAND (Plays ONLY when user turns switch ON)
 * 3. Dynamic Obstacle Blockages & Instant Real-Time Rerouting
 * 4. Architectural Floor Plan, One-Tap Multi-Floor Transitions & Room Availability
 */
document.addEventListener('DOMContentLoaded', async () => {
    // Application State
    const state = {
        mapData: null,
        doctors: [],
        locationsByFloor: {},
        floors: {},
        qrMarkers: [],
        blockableFacilities: [],
        blockedNodes: new Set(),
        travelMode: 'walk', // 'walk' | 'wheelchair' | 'stretcher'
        voiceEnabled: false, // Default: OFF (Audio plays ONLY when turned ON)
        selectedVoiceLang: 'en-US',
        activeTab: 'doctors', // 'doctors' | 'departments' | 'multistop' | 'emergency'
        selectedDoctor: null,
        selectedEmergency: null,
        multiStops: ['', ''], // Initial 2 stops
        currentRouteData: null,
        currentFloor: 0,
        currentFloorRooms: [],
        activeDirFilter: 'all',
        crowdData: null,
        crowdHeatmapActive: false
    };

    // Subsystems Instances
    const mapRenderer = new HospitalMapRenderer('hospitalCanvas');
    const voice = new VoiceGuidance();
    const qrSimulator = new QrSimulator('qrModal', 'qrMarkersGrid', (nodeId, name, floor) => {
        const startSelect = document.getElementById('startLocation');
        if (startSelect) {
            startSelect.value = nodeId;
            switchFloor(floor);
            if (state.voiceEnabled) {
                voice.speakText(`Location set to ${name}`, state.selectedVoiceLang);
            }
        }
    });

    function updateMapHighlights() {
        const startId = document.getElementById('startLocation') ? document.getElementById('startLocation').value : null;
        let destId = null;

        if (state.activeTab === 'doctors' && state.selectedDoctor) {
            destId = state.selectedDoctor.room_id;
        } else if (state.activeTab === 'departments') {
            const roomSelect = document.getElementById('roomSelect');
            if (roomSelect && roomSelect.value) destId = roomSelect.value;
        } else if (state.activeTab === 'emergency' && state.selectedEmergency) {
            destId = state.selectedEmergency;
        } else if (state.activeTab === 'multistop') {
            const validStops = state.multiStops.filter(s => s && s.trim());
            if (validStops.length > 0) {
                destId = validStops[validStops.length - 1];
            }
        }

        mapRenderer.setHighlightedPoints(startId, destId);
    }

    // Room click on map sets as destination & navigates
    mapRenderer.onRoomSelect = (nodeId) => {
        switchToTab('departments');
        const roomSelect = document.getElementById('roomSelect');
        if (roomSelect) {
            roomSelect.value = nodeId;
            triggerRouteCalculation();
        }
    };

    // One-Tap Lift/Stairs Transition from Canvas Map
    mapRenderer.onFloorTransitionTap = (targetFloor, transitionName) => {
        executeFloorTransition(targetFloor, transitionName);
    };

    // Step change in voice guidance
    voice.onStepChange = (step, idx) => {
        highlightStepCard(idx);
        if (step.node_id) {
            mapRenderer.highlightNode(step.node_id);
            if (typeof step.floor === 'number' && step.floor !== state.currentFloor) {
                switchFloor(step.floor);
            }
        }
    };

    voice.onFinish = () => {
        resetAudioButton();
    };

    // ==========================================
    // 1. Initial Data Loading & Population
    // ==========================================
    try {
        const [mapRes, docsRes, locsRes, emerRes, qrRes, blockRes] = await Promise.all([
            HospitalAPI.getHospitalMap(),
            HospitalAPI.getDoctors(),
            HospitalAPI.getLocations(),
            HospitalAPI.getEmergencyRoutes(),
            HospitalAPI.getQrLocations(),
            HospitalAPI.getBlockableFacilities()
        ]);

        state.mapData = mapRes.data;
        state.doctors = docsRes.doctors;
        state.locationsByFloor = locsRes.locations_by_floor;
        state.floors = locsRes.floors;
        state.qrMarkers = qrRes.markers;
        state.blockableFacilities = blockRes.blockable_facilities;

        // Initialize Map
        mapRenderer.init(state.mapData);

        // Populate Dropdowns & Controls
        populateStartLocations(locsRes.locations_by_floor, locsRes.floors);
        populateDoctorsDropdown(state.doctors);
        populateRoomsDropdown(locsRes.locations_by_floor, locsRes.floors);
        populateEmergencyButtons(emerRes.emergency_locations);
        populateBlockableFacilities(state.blockableFacilities);
        initMultiStopUI();

        // Load Ground Floor Directory
        await loadFloorDirectory(0);

        // Load initial crowd density metrics
        try {
            const crowdRes = await HospitalAPI.getCrowdDensity();
            if (crowdRes && crowdRes.success) {
                state.crowdData = crowdRes.crowd_data;
            }
        } catch (cErr) {
            console.warn('Initial crowd load warning:', cErr);
        }

    } catch (err) {
        console.error('Initialization error:', err);
        alert('Could not connect to hospital navigation server. Please verify Flask backend is running.');
    }

    // ==========================================
    // 2. Travel Mode Preferences (Walk, Wheelchair, Stretcher)
    // ==========================================
    const modePills = document.querySelectorAll('.mode-pill');
    modePills.forEach(pill => {
        pill.addEventListener('click', () => {
            modePills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const radio = pill.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                state.travelMode = radio.value;
                // If route already active, immediately recalculate for new mode!
                if (state.currentRouteData) {
                    triggerRouteCalculation();
                }
            }
        });
    });

    // ==========================================
    // 3. Audio Voice Guidance Setting (ON DEMAND ONLY)
    // ==========================================
    const voiceToggle = document.getElementById('voiceGuidanceToggle');
    voiceToggle.addEventListener('change', (e) => {
        state.voiceEnabled = e.target.checked;
        if (!state.voiceEnabled) {
            voice.stop();
            resetAudioButton();
        } else {
            // Speak brief confirmation
            if (state.selectedVoiceLang.startsWith('ta')) {
                voice.speakText('குரல் வழி காட்டுதல் இயக்கப்பட்டது', 'ta-IN');
            } else {
                voice.speakText('Voice navigation guidance enabled', 'en-US');
            }
            if (state.currentRouteData) {
                playVoiceDirections();
            }
        }
    });

    const voiceLangSelect = document.getElementById('voiceLang');
    voiceLangSelect.addEventListener('change', (e) => {
        state.selectedVoiceLang = e.target.value;
        voice.setLanguage(state.selectedVoiceLang);
    });

    // ==========================================
    // 4. Dynamic Obstacle Blockage & Maintenance Simulator
    // ==========================================
    const obsHeader = document.getElementById('btnToggleObstaclePanel');
    const obsBody = document.getElementById('obstacleBody');
    const obsArrow = document.getElementById('obsArrow');
    obsHeader.addEventListener('click', () => {
        const isHidden = obsBody.classList.toggle('hidden');
        obsArrow.textContent = isHidden ? '▼' : '▲';
    });

    function populateBlockableFacilities(facilities) {
        const container = document.getElementById('blockableListContainer');
        container.innerHTML = '';

        facilities.forEach(fac => {
            const label = document.createElement('label');
            label.className = 'blockable-item';
            label.innerHTML = `
                <input type="checkbox" data-node-id="${fac.id}">
                <span>${fac.icon} ${fac.name}</span>
            `;

            const chk = label.querySelector('input');
            chk.addEventListener('change', () => {
                if (chk.checked) {
                    state.blockedNodes.add(fac.id);
                } else {
                    state.blockedNodes.delete(fac.id);
                }

                // Update Map visual hazard markers
                mapRenderer.setBlockedNodes(Array.from(state.blockedNodes));

                // If route currently active, IMMEDIATELY RECALCULATE ALTERNATIVE SHORTEST ROUTE!
                if (state.currentRouteData) {
                    if (state.currentRouteData.is_fire_evacuation) {
                        triggerFireEvacuation();
                    } else {
                        triggerRouteCalculation();
                    }
                }
            });

            container.appendChild(label);
        });
    }

    // ==========================================
    // 5. Floor Directory & Live Availability
    // ==========================================
    async function loadFloorDirectory(floor) {
        try {
            const data = await HospitalAPI.getFloorDirectory(floor);
            state.currentFloorRooms = data.rooms;

            const title = document.getElementById('directoryFloorTitle');
            const floorNames = {
                0: '🏢 Ground Floor - Department & Facility Directory',
                1: '🏢 1st Floor (OPD Wings) - Specialist Clinics Directory',
                2: '🏢 2nd Floor (Specialist & ICU) - Department Directory'
            };
            if (title) title.textContent = floorNames[floor] || `Floor ${floor} Directory`;

            renderFloorRooms(state.currentFloorRooms, state.activeDirFilter);
        } catch (err) {
            console.error('Failed to load floor directory:', err);
        }
    }

    function renderFloorRooms(rooms, filter = 'all') {
        const grid = document.getElementById('floorRoomsGrid');
        if (!grid) return;
        grid.innerHTML = '';

        const filtered = rooms.filter(r => {
            if (filter === 'all') return true;
            if (filter === 'consultation') return r.availability_status === 'available' || r.availability_status === 'consultation';
            if (filter === 'emergency') return r.availability_status === 'emergency' || r.availability_status === 'diagnostics';
            if (filter === 'crowd-low' || filter === 'low') return r.crowd_level === 'low';
            if (filter === 'crowd-moderate' || filter === 'moderate') return r.crowd_level === 'moderate';
            if (filter === 'crowd-high' || filter === 'high') return r.crowd_level === 'high';
            return true;
        });

        if (filtered.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; padding: 18px; text-align: center; color: #64748b; background: #ffffff; border: 1px dashed #cbd5e1; border-radius: 8px;">
                    <span>No rooms on this floor match the filter "<strong>${filter}</strong>". Switch floors above to view other rooms.</span>
                </div>
            `;
            return;
        }

        filtered.forEach(room => {
            const card = document.createElement('div');
            card.className = `room-dir-card border-${room.availability_status || 'available'}`;

            const docHtml = room.doctor 
                ? `<div class="rdc-doctor">👨‍⚕️ ${room.doctor.name} <br><small style="color:#64748b;">${room.doctor.specialty} • ${room.doctor.opd_timings}</small></div>`
                : (room.description ? `<p style="font-size:0.75rem; color:#64748b; margin-bottom:6px;">${room.description}</p>` : '');

            const crowdIcon = room.crowd_level === 'high' ? '🔥' : (room.crowd_level === 'moderate' ? '👥' : '🟢');
            const crowdTagClass = room.crowd_level === 'high' ? 'tag-rush-high' : (room.crowd_level === 'moderate' ? 'tag-rush-moderate' : 'tag-rush-low');
            const crowdLabel = room.crowd_level === 'high' ? 'Heavy Rush' : (room.crowd_level === 'moderate' ? 'Moderate Rush' : 'Low Crowd');
            const crowdHtml = `<div class="rdc-crowd-tag ${crowdTagClass}">
                <span>${crowdIcon} ${crowdLabel} (${room.crowd_percentage || 20}%)</span>
            </div>`;

            card.innerHTML = `
                <div>
                    <div class="rdc-top">
                        <span class="rdc-code">${room.room_code || 'ROOM'}</span>
                        ${crowdHtml}
                    </div>
                    <div class="rdc-title">${room.name}</div>
                    ${docHtml}
                    <div class="rdc-availability status-${room.availability_status || 'open'}">
                        ${room.availability_text || 'Available'}
                    </div>
                </div>
                <button type="button" class="btn-nav-room">
                    <span>🧭 Navigate to this Room</span>
                </button>
            `;

            card.querySelector('.btn-nav-room').addEventListener('click', () => {
                switchToTab('departments');
                const roomSelect = document.getElementById('roomSelect');
                if (roomSelect) {
                    roomSelect.value = room.id;
                    triggerRouteCalculation();
                }
            });

            grid.appendChild(card);
        });
    }

    const dirFilterBtns = document.querySelectorAll('.dir-filter-btn');
    dirFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            dirFilterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.activeDirFilter = btn.dataset.filter;
            renderFloorRooms(state.currentFloorRooms, state.activeDirFilter);
        });
    });

    // ==========================================
    // 6. Floor Switching & One-Tap Transitions
    // ==========================================
    function switchFloor(floorNum) {
        state.currentFloor = parseInt(floorNum, 10);
        mapRenderer.setFloor(state.currentFloor);
        updateActiveFloorTab(state.currentFloor);
        updateFloorOverlayBadge(state.currentFloor);
        loadFloorDirectory(state.currentFloor);
        checkMultiFloorTransitionBanner();
        if (typeof updateCrowdSuggestionBanner === 'function') {
            updateCrowdSuggestionBanner(currentSelectedCrowdFilter);
        }
    }

    const floorButtons = document.querySelectorAll('.floor-tab');
    floorButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            switchFloor(parseInt(btn.dataset.floor, 10));
        });
    });

    function updateActiveFloorTab(floor) {
        floorButtons.forEach(b => b.classList.toggle('active', parseInt(b.dataset.floor, 10) === floor));
        const sideHeader = document.getElementById('sideFloorHeader');
        if (sideHeader) {
            sideHeader.textContent = floor === 0 ? 'FLOOR 00' : (floor === 1 ? 'FLOOR 01' : 'FLOOR 02');
        }
    }

    function updateFloorOverlayBadge(floor) {
        const label = document.getElementById('currentFloorLabel');
        const names = { 0: 'Ground Floor Blueprint', 1: '1st Floor (OPD Wings)', 2: '2nd Floor (Specialist & ICU)' };
        if (label) label.textContent = names[floor] || `Floor ${floor}`;

        const crowdSummary = document.getElementById('floorCrowdSummaryBadge');
        if (crowdSummary) {
            crowdSummary.className = 'floor-crowd-chip';
            if (floor === 0) {
                crowdSummary.classList.add('chip-high');
                crowdSummary.textContent = '🔴 Floor Rush: Heavy (Reception & Pharmacy ~88%)';
            } else if (floor === 1) {
                crowdSummary.classList.add('chip-mod');
                crowdSummary.textContent = '🟡 Floor Rush: Moderate (OPD Clinics ~55%)';
            } else {
                crowdSummary.classList.add('chip-low');
                crowdSummary.textContent = '🟢 Floor Rush: Low Crowd / Quiet (~22%)';
            }
        }

        const quickReturn = document.getElementById('btnQuickReturnGround');
        if (quickReturn) {
            quickReturn.classList.toggle('hidden', floor === 0 || !state.currentRouteData);
        }
    }

    function executeFloorTransition(targetFloor, transitionName) {
        switchFloor(targetFloor);

        // Voice audio speaks ONLY IF voiceGuidanceToggle is explicitly enabled
        if (state.voiceEnabled) {
            const floorTitle = targetFloor === 0 ? 'Ground Floor' : (targetFloor === 1 ? '1st Floor' : '2nd Floor');
            if (state.selectedVoiceLang.startsWith('ta')) {
                voice.speakText(`${transitionName} வழியாக ${floorTitle} வந்தாச்சு. உங்கள் அடுத்த வழி பாதையை தொடரவும்.`, 'ta-IN');
            } else {
                voice.speakText(`Arrived on ${floorTitle} via ${transitionName}. Continuing shortest path.`, 'en-US');
            }
        }
    }

    const oneTapBtn = document.getElementById('btnOneTapTransition');
    if (oneTapBtn) {
        oneTapBtn.addEventListener('click', () => {
            const targetFloor = parseInt(oneTapBtn.dataset.targetFloor, 10);
            const transitionName = oneTapBtn.dataset.transName || 'Elevator';
            executeFloorTransition(targetFloor, transitionName);
        });
    }

    function checkMultiFloorTransitionBanner() {
        const banner = document.getElementById('multiFloorBanner');
        if (!banner) return;

        if (!state.currentRouteData || !state.currentRouteData.path_details) {
            banner.classList.add('hidden');
            return;
        }

        const details = state.currentRouteData.path_details;
        let transitionFound = null;

        for (let i = 0; i < details.length - 1; i++) {
            const p1 = details[i];
            const p2 = details[i + 1];

            if (p1.floor === state.currentFloor && p2.floor !== state.currentFloor) {
                transitionFound = { from: p1, to: p2 };
                break;
            }
        }

        if (transitionFound) {
            const targetFloor = transitionFound.to.floor;
            const targetFloorName = targetFloor === 0 ? 'Ground Floor' : (targetFloor === 1 ? '1st Floor (OPD)' : '2nd Floor');
            const via = transitionFound.to.transition_via === 'stairs' ? 'Stairs' : 'Lift / Elevator';
            const icon = transitionFound.to.transition_via === 'stairs' ? '🪜' : '🛗';

            document.getElementById('ftIcon').textContent = icon;
            document.getElementById('ftTitle').textContent = `Walk to ${transitionFound.from.name} ➡️ Ride to ${targetFloorName}`;
            document.getElementById('ftSubtitle').textContent = `One-Tap: When you reach this spot, tap below to open ${targetFloorName}!`;
            document.getElementById('ftTargetFloorNum').textContent = targetFloor;

            oneTapBtn.dataset.targetFloor = targetFloor;
            oneTapBtn.dataset.transName = transitionFound.from.name;
            banner.classList.remove('hidden');
        } else {
            banner.classList.add('hidden');
        }
    }

    // ==========================================
    // 7. Destination Tabs & Doctor Cards
    // ==========================================
    const tabButtons = document.querySelectorAll('.dest-tabs .tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            switchToTab(btn.dataset.tab);
        });
    });

    function switchToTab(tabKey) {
        state.activeTab = tabKey;
        tabButtons.forEach(b => b.classList.toggle('active', b.dataset.tab === tabKey));
        document.querySelectorAll('.tab-content').forEach(tc => {
            tc.classList.toggle('active', tc.id === `tab-${tabKey}`);
        });
        updateMapHighlights();
    }

    const doctorSelect = document.getElementById('doctorSelect');
    const doctorPreview = document.getElementById('doctorCardPreview');
    doctorSelect.addEventListener('change', (e) => {
        const docId = e.target.value;
        const doc = state.doctors.find(d => d.id === docId);
        state.selectedDoctor = doc;

        if (doc) {
            document.getElementById('docSpecialty').textContent = doc.specialty;
            document.getElementById('docName').textContent = doc.name;
            document.getElementById('docRoom').textContent = `${doc.room_name} (Floor ${doc.floor})`;
            document.getElementById('docTimings').textContent = `⏱ ${doc.opd_timings}`;
            document.getElementById('docStatus').textContent = doc.status;
            doctorPreview.classList.remove('hidden');

            // Fetch live queue status & wait time for this doctor
            updateDoctorQueueTracker(doc.id);
        } else {
            doctorPreview.classList.add('hidden');
        }
        updateMapHighlights();
    });

    // Live Smart Token Queue Tracker
    async function updateDoctorQueueTracker(doctorId) {
        if (!doctorId) return;
        const tokenInput = document.getElementById('patientTokenInput');
        const tokenVal = tokenInput ? parseInt(tokenInput.value, 10) : 24;

        try {
            const q = await HospitalAPI.getQueueStatus(doctorId, tokenVal);
            if (!q || !q.success) return;

            const servingNow = document.getElementById('qmServingNow');
            const qmAhead = document.getElementById('qmAhead');
            const qmWait = document.getElementById('qmWaitTime');
            const statusBanner = document.getElementById('queueStatusBanner');
            const statusText = document.getElementById('queueStatusText');

            if (servingNow) servingNow.textContent = `#${q.current_token}`;
            if (qmAhead) qmAhead.textContent = `${q.patients_ahead}`;
            if (qmWait) qmWait.textContent = `~${q.estimated_wait_minutes} min`;

            if (statusBanner && statusText) {
                statusBanner.className = `queue-status-banner status-${q.urgency_level}`;
                statusText.textContent = state.selectedVoiceLang.startsWith('ta') ? q.status_text_ta : q.status_text_en;
            }
        } catch (err) {
            console.warn('Queue update failed:', err);
        }
    }

    const btnUpdateQueue = document.getElementById('btnUpdateQueue');
    if (btnUpdateQueue) {
        btnUpdateQueue.addEventListener('click', () => {
            if (state.selectedDoctor) updateDoctorQueueTracker(state.selectedDoctor.id);
        });
    }

    const patientTokenInput = document.getElementById('patientTokenInput');
    if (patientTokenInput) {
        patientTokenInput.addEventListener('change', () => {
            if (state.selectedDoctor) updateDoctorQueueTracker(state.selectedDoctor.id);
        });
    }

    // ==========================================
    // Bilingual Symptom to Doctor Smart Search
    // ==========================================
    const symptomInput = document.getElementById('symptomSearchInput');
    const symptomDropdown = document.getElementById('symptomSearchResults');
    const btnClearSearch = document.getElementById('btnClearSymptomSearch');
    let searchDebounceTimer = null;

    if (symptomInput) {
        symptomInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (btnClearSearch) {
                btnClearSearch.classList.toggle('hidden', query.length === 0);
            }

            clearTimeout(searchDebounceTimer);
            if (query.length < 2) {
                if (symptomDropdown) {
                    symptomDropdown.classList.add('hidden');
                    symptomDropdown.innerHTML = '';
                }
                return;
            }

            searchDebounceTimer = setTimeout(async () => {
                try {
                    const data = await HospitalAPI.searchSymptoms(query);
                    renderSymptomSearchResults(data.results || []);
                } catch (err) {
                    console.error('Symptom search failed:', err);
                }
            }, 250);
        });
    }

    if (btnClearSearch) {
        btnClearSearch.addEventListener('click', () => {
            if (symptomInput) symptomInput.value = '';
            if (symptomDropdown) {
                symptomDropdown.classList.add('hidden');
                symptomDropdown.innerHTML = '';
            }
            btnClearSearch.classList.add('hidden');
        });
    }

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.symptom-search-container')) {
            if (symptomDropdown) symptomDropdown.classList.add('hidden');
        }
    });

    function renderSymptomSearchResults(results) {
        if (!symptomDropdown) return;
        symptomDropdown.innerHTML = '';

        if (!results || results.length === 0) {
            symptomDropdown.innerHTML = `
                <div class="symptom-result-item" style="cursor:default; color:#64748b; font-size:0.75rem;">
                    <span>No medical match found. Please choose from Doctor or Room tab.</span>
                </div>
            `;
            symptomDropdown.classList.remove('hidden');
            return;
        }

        const isTa = state.selectedVoiceLang.startsWith('ta');

        results.forEach(item => {
            const card = document.createElement('div');
            card.className = 'symptom-result-item';

            const title = isTa ? item.title_ta : item.title_en;
            const advice = isTa ? item.advice_ta : item.advice_en;
            const urgencyLabel = {
                emergency: isTa ? '🚨 அவசரம்' : '🚨 Emergency',
                priority: isTa ? '⚡ முன்னுரிமை' : '⚡ Priority',
                routine: isTa ? '🟢 வழக்கமான OPD' : '🟢 Routine OPD'
            }[item.urgency] || 'OPD';

            card.innerHTML = `
                <div class="sri-header">
                    <span class="sri-title">${title}</span>
                    <span class="urgency-pill urgency-${item.urgency}">${urgencyLabel}</span>
                </div>
                <div class="sri-match-tag">${item.badge} • Floor ${item.floor}</div>
                <div class="sri-advice">${advice}</div>
                <div class="sri-dest">📍 Destination: ${item.target_node_name} ➡️ Tap to Navigate</div>
            `;

            card.addEventListener('click', () => {
                symptomInput.value = title;
                symptomDropdown.classList.add('hidden');

                if (item.doctor) {
                    switchToTab('doctors');
                    const doctorSelect = document.getElementById('doctorSelect');
                    if (doctorSelect) {
                        doctorSelect.value = item.doctor.id;
                        doctorSelect.dispatchEvent(new Event('change'));
                    }
                } else {
                    switchToTab('departments');
                    const roomSelect = document.getElementById('roomSelect');
                    if (roomSelect) {
                        roomSelect.value = item.target_node_id;
                        roomSelect.dispatchEvent(new Event('change'));
                    }
                }

                updateMapHighlights();
                triggerRouteCalculation();

                if (state.voiceEnabled) {
                    voice.speakText(advice, state.selectedVoiceLang);
                }
            });

            symptomDropdown.appendChild(card);
        });

        symptomDropdown.classList.remove('hidden');
    }

    const roomSelect = document.getElementById('roomSelect');
    if (roomSelect) {
        roomSelect.addEventListener('change', () => {
            updateMapHighlights();
        });
    }

    // ==========================================
    // Multi-Stop Journey UI Management
    // ==========================================
    function initMultiStopUI() {
        renderMultiStopRows();

        const btnAdd = document.getElementById('btnAddStop');
        if (btnAdd) {
            btnAdd.addEventListener('click', () => {
                if (state.multiStops.length >= 6) {
                    alert('Maximum 6 stops supported in a single journey.');
                    return;
                }
                state.multiStops.push('');
                renderMultiStopRows();
                updateMapHighlights();
            });
        }

        // Preset 1: Dr. Priya (Ortho) -> X-Ray -> Pharmacy
        const btnPresetOpd = document.getElementById('btnPresetOpdScan');
        if (btnPresetOpd) {
            btnPresetOpd.addEventListener('click', () => {
                switchToTab('multistop');
                state.multiStops = ['ROOM_102', 'ROOM_RADIOLOGY', 'ROOM_PHARMACY'];
                renderMultiStopRows();
                updateMapHighlights();
                triggerRouteCalculation();
            });
        }

        // Preset 2: Dr. Kumar (Cardio) -> Ultrasound -> Pharmacy
        const btnPresetCardio = document.getElementById('btnPresetCardioEcho');
        if (btnPresetCardio) {
            btnPresetCardio.addEventListener('click', () => {
                switchToTab('multistop');
                state.multiStops = ['ROOM_101', 'ROOM_105', 'ROOM_PHARMACY'];
                renderMultiStopRows();
                updateMapHighlights();
                triggerRouteCalculation();
            });
        }

        // Preset 3: Dr. Arun (Neuro - Room 201) -> Return to Ground Floor
        const btnPresetNeuro = document.getElementById('btnPresetNeuroReturn');
        if (btnPresetNeuro) {
            btnPresetNeuro.addEventListener('click', () => {
                switchToTab('multistop');
                state.multiStops = ['ROOM_201', 'ENTRANCE_MAIN'];
                renderMultiStopRows();
                updateMapHighlights();
                triggerRouteCalculation();
            });
        }

        // Button: Add Return to Ground Floor as final stop
        const btnAddReturn = document.getElementById('btnAddReturnGround');
        if (btnAddReturn) {
            btnAddReturn.addEventListener('click', () => {
                if (state.multiStops.length >= 6) {
                    alert('Maximum 6 stops supported in a single journey.');
                    return;
                }
                const lastIdx = state.multiStops.length - 1;
                if (state.multiStops[lastIdx] !== 'ENTRANCE_MAIN') {
                    if (!state.multiStops[lastIdx]) {
                        state.multiStops[lastIdx] = 'ENTRANCE_MAIN';
                    } else {
                        state.multiStops.push('ENTRANCE_MAIN');
                    }
                }
                renderMultiStopRows();
                updateMapHighlights();
                const activeStops = state.multiStops.filter(s => s && s.trim());
                if (activeStops.length > 1) {
                    triggerRouteCalculation();
                }
            });
        }
    }

    function renderMultiStopRows() {
        const container = document.getElementById('stopsContainer');
        if (!container) return;
        container.innerHTML = '';

        state.multiStops.forEach((selectedVal, idx) => {
            const isLast = (idx === state.multiStops.length - 1 && state.multiStops.length > 1);
            const row = document.createElement('div');
            row.className = 'stop-input-row';

            const badgeClass = isLast ? 'stop-num-badge badge-final' : 'stop-num-badge';
            const badgeLabel = isLast ? `Final 🏁` : `Stop ${idx + 1}`;

            row.innerHTML = `
                <div class="${badgeClass}">${badgeLabel}</div>
                <div class="stop-select-wrap">
                    <select class="form-select stop-select" data-index="${idx}">
                        <option value="">-- Choose Stop / Department --</option>
                    </select>
                </div>
                <button type="button" class="btn-remove-stop" title="Remove this stop" ${state.multiStops.length <= 1 ? 'disabled' : ''}>✕</button>
            `;

            const select = row.querySelector('.stop-select');
            populateMultiStopSelectOptions(select, selectedVal);

            select.addEventListener('change', (e) => {
                state.multiStops[idx] = e.target.value;
                updateMapHighlights();
            });

            const removeBtn = row.querySelector('.btn-remove-stop');
            removeBtn.addEventListener('click', () => {
                if (state.multiStops.length > 1) {
                    state.multiStops.splice(idx, 1);
                    renderMultiStopRows();
                    updateMapHighlights();
                    if (state.currentRouteData && state.activeTab === 'multistop') {
                        triggerRouteCalculation();
                    }
                }
            });

            container.appendChild(row);
        });
    }

    function populateMultiStopSelectOptions(select, currentVal) {
        if (!state.locationsByFloor) return;

        // Group rooms by floor
        for (const [floorNum, locations] of Object.entries(state.locationsByFloor)) {
            const optgroup = document.createElement('optgroup');
            const floorNames = { 0: 'Ground Floor Facilities & Entrance', 1: '1st Floor OPD Clinics', 2: '2nd Floor Specialty & ICU' };
            optgroup.label = (state.floors && state.floors[floorNum]) ? state.floors[floorNum].name : (floorNames[floorNum] || `Floor ${floorNum}`);

            locations.forEach(loc => {
                if (loc.type === 'room' || loc.type === 'amenity' || loc.type === 'reception' || loc.type === 'entrance') {
                    const opt = document.createElement('option');
                    opt.value = loc.id;
                    opt.textContent = loc.name;
                    if (loc.id === currentVal) opt.selected = true;
                    optgroup.appendChild(opt);
                }
            });

            select.appendChild(optgroup);
        }
    }

    // ==========================================
    // 1-Click Return to Ground Floor (Same Path / Reverse Route)
    // ==========================================
    function returnToGroundFloor() {
        let fromNodeId = 'ROOM_201'; // Default

        if (state.currentRouteData && state.currentRouteData.path_nodes) {
            const nodes = state.currentRouteData.path_nodes;
            for (let i = nodes.length - 1; i >= 0; i--) {
                const nId = nodes[i];
                const node = state.mapData ? state.mapData.nodes[nId] : null;
                if (node && (node.type === 'room' || node.type === 'reception')) {
                    fromNodeId = nId;
                    break;
                }
            }
        } else if (state.activeTab === 'departments') {
            const roomSelect = document.getElementById('roomSelect');
            if (roomSelect && roomSelect.value) fromNodeId = roomSelect.value;
        } else if (state.activeTab === 'doctors' && state.selectedDoctor) {
            fromNodeId = state.selectedDoctor.room_id;
        }

        // 1. Set current location to current room
        const startSelect = document.getElementById('startLocation');
        if (startSelect) {
            startSelect.value = fromNodeId;
        }

        // 2. Switch to departments tab and set destination to Ground Floor Main Entrance
        switchToTab('departments');
        const roomSelect = document.getElementById('roomSelect');
        if (roomSelect) {
            roomSelect.value = 'ENTRANCE_MAIN';
        }

        updateMapHighlights();
        triggerRouteCalculation();

        if (state.voiceEnabled) {
            const fromName = (state.mapData && state.mapData.nodes[fromNodeId]) ? state.mapData.nodes[fromNodeId].name : 'Current Room';
            if (state.selectedVoiceLang.startsWith('ta')) {
                voice.speakText(`${fromName}-லிருந்து தரைத்தளம் மெயின் என்ட்ரன்ஸுக்கு திரும்பும் பாதை கணக்கிடப்பட்டது.`, 'ta-IN');
            } else {
                voice.speakText(`Calculating return route from ${fromName} back to Ground Floor Main Entrance.`, 'en-US');
            }
        }
    }

    const btnReturnToGround = document.getElementById('btnReturnToGround');
    if (btnReturnToGround) {
        btnReturnToGround.addEventListener('click', returnToGroundFloor);
    }

    const btnQuickReturnGround = document.getElementById('btnQuickReturnGround');
    if (btnQuickReturnGround) {
        btnQuickReturnGround.addEventListener('click', returnToGroundFloor);
    }

    // ==========================================
    // Live Crowd Density Heatmap Toggle Controller & Interactive Rush Filter
    // ==========================================
    let currentSelectedCrowdFilter = 'all';

    const btnToggleCrowdHeatmap = document.getElementById('btnToggleCrowdHeatmap');
    if (btnToggleCrowdHeatmap) {
        btnToggleCrowdHeatmap.addEventListener('click', () => {
            state.crowdHeatmapActive = !state.crowdHeatmapActive;
            const btnText = document.getElementById('heatmapBtnText');
            if (state.crowdHeatmapActive) {
                btnToggleCrowdHeatmap.classList.add('active');
                if (btnText) btnText.innerText = 'Crowd: ON';
            } else {
                btnToggleCrowdHeatmap.classList.remove('active');
                if (btnText) btnText.innerText = 'Crowd Heatmap';
            }
            mapRenderer.setCrowdHeatmap(state.crowdHeatmapActive, state.crowdData);
        });
    }

    const crowdFilterBtns = document.querySelectorAll('.crowd-filter-btn');
    const crowdSuggestionBanner = document.getElementById('crowdSuggestionBanner');
    const csbIcon = document.getElementById('csbIcon');
    const csbText = document.getElementById('csbText');
    const btnCsbSwitchFloor = document.getElementById('btnCsbSwitchFloor');
    const csbSwitchText = document.getElementById('csbSwitchText');

    function updateCrowdSuggestionBanner(rushLevel) {
        if (!crowdSuggestionBanner) return;

        if (rushLevel === 'all') {
            crowdSuggestionBanner.classList.add('hidden');
            return;
        }

        crowdSuggestionBanner.className = 'crowd-suggestion-banner';
        if (btnCsbSwitchFloor) btnCsbSwitchFloor.classList.add('hidden');

        if (rushLevel === 'low') {
            crowdSuggestionBanner.classList.add('banner-low');
            if (state.currentFloor === 0) {
                if (csbIcon) csbIcon.textContent = '🟢';
                if (csbText) csbText.innerHTML = `<strong>Ground Floor:</strong> Blood Bank (22%) is Low Crowd. <br><small>💡 Tip: <strong>2nd Floor (Specialist & ICU)</strong> has 5 quiet low crowd wards (ICU 15%, OT 10%, Dialysis 25%).</small>`;
                if (btnCsbSwitchFloor) {
                    btnCsbSwitchFloor.classList.remove('hidden');
                    if (csbSwitchText) csbSwitchText.textContent = '👉 Go to 2nd Floor (Low Crowd)';
                    btnCsbSwitchFloor.onclick = () => switchFloor(2);
                }
            } else if (state.currentFloor === 1) {
                if (csbIcon) csbIcon.textContent = '🟢';
                if (csbText) csbText.innerHTML = `<strong>1st Floor:</strong> Ultrasound & 2D Echo (30%) and Physiotherapy (20%) are Low Crowd. <br><small>💡 Tip: <strong>2nd Floor</strong> is also quiet (10-28%).</small>`;
                if (btnCsbSwitchFloor) {
                    btnCsbSwitchFloor.classList.remove('hidden');
                    if (csbSwitchText) csbSwitchText.textContent = '👉 Go to 2nd Floor (Quiet)';
                    btnCsbSwitchFloor.onclick = () => switchFloor(2);
                }
            } else {
                if (csbIcon) csbIcon.textContent = '🟢';
                if (csbText) csbText.innerHTML = `<strong>2nd Floor:</strong> This entire floor is quiet! ICU (15%), Operation Theatre (10%), Dialysis (25%), Nephrology (35%) & Oncology (28%).`;
                if (btnCsbSwitchFloor) btnCsbSwitchFloor.classList.add('hidden');
            }
        } else if (rushLevel === 'moderate') {
            crowdSuggestionBanner.classList.add('banner-moderate');
            if (state.currentFloor === 0) {
                if (csbIcon) csbIcon.textContent = '🟡';
                if (csbText) csbText.innerHTML = `<strong>Ground Floor:</strong> Radiology & CT Scan (48%) is in Moderate Rush. <br><small>💡 Tip: <strong>1st Floor (OPD Wings)</strong> has specialist consultation clinics with moderate rush (45%-68%).</small>`;
                if (btnCsbSwitchFloor) {
                    btnCsbSwitchFloor.classList.remove('hidden');
                    if (csbSwitchText) csbSwitchText.textContent = '👉 Go to 1st Floor (OPD Clinics)';
                    btnCsbSwitchFloor.onclick = () => switchFloor(1);
                }
            } else if (state.currentFloor === 1) {
                if (csbIcon) csbIcon.textContent = '🟡';
                if (csbText) csbText.innerHTML = `<strong>1st Floor:</strong> Cardiology (68%), Orthology (62%), Pediatrics (58%) & Surgery (45%) are in Moderate Rush.`;
                if (btnCsbSwitchFloor) btnCsbSwitchFloor.classList.add('hidden');
            } else {
                if (csbIcon) csbIcon.textContent = '🟡';
                if (csbText) csbText.innerHTML = `<strong>2nd Floor:</strong> Neurology Clinic (42%) and ENT & Eye Clinic (44%) are in Moderate Rush.`;
                if (btnCsbSwitchFloor) btnCsbSwitchFloor.classList.add('hidden');
            }
        } else if (rushLevel === 'high') {
            crowdSuggestionBanner.classList.add('banner-high');
            if (state.currentFloor === 0) {
                if (csbIcon) csbIcon.textContent = '🔴';
                if (csbText) csbText.innerHTML = `<strong>Ground Floor:</strong> Heavy Rush in 24/7 Pharmacy (92%), Main Reception (88%), and Emergency Ward (78%).`;
                if (btnCsbSwitchFloor) btnCsbSwitchFloor.classList.add('hidden');
            } else {
                if (csbIcon) csbIcon.textContent = '🔴';
                if (csbText) csbText.innerHTML = `This floor has no extreme rush! Heavy rush is only on <strong>Ground Floor</strong> (Reception & Pharmacy).`;
                if (btnCsbSwitchFloor) {
                    btnCsbSwitchFloor.classList.remove('hidden');
                    if (csbSwitchText) csbSwitchText.textContent = '👉 View Ground Floor Heavy Rush';
                    btnCsbSwitchFloor.onclick = () => switchFloor(0);
                }
            }
        }

        crowdSuggestionBanner.classList.remove('hidden');
    }

    crowdFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            crowdFilterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const rushLevel = btn.dataset.crowd;
            currentSelectedCrowdFilter = rushLevel;

            // Automatically turn on crowd heatmap if user clicks a filter
            if (rushLevel !== 'all' && !state.crowdHeatmapActive) {
                state.crowdHeatmapActive = true;
                if (btnToggleCrowdHeatmap) {
                    btnToggleCrowdHeatmap.classList.add('active');
                    const bTxt = document.getElementById('heatmapBtnText');
                    if (bTxt) bTxt.innerText = 'Crowd: ON';
                }
            }

            // Apply filter to canvas map
            mapRenderer.setCrowdLevelFilter(rushLevel);

            // Sync with Floor Directory filter below
            if (rushLevel === 'all') {
                state.activeDirFilter = 'all';
            } else {
                state.activeDirFilter = `crowd-${rushLevel}`;
            }

            dirFilterBtns.forEach(dfb => {
                dfb.classList.toggle('active', dfb.dataset.filter === state.activeDirFilter || (rushLevel === 'all' && dfb.dataset.filter === 'all'));
            });
            renderFloorRooms(state.currentFloorRooms, state.activeDirFilter);

            updateCrowdSuggestionBanner(rushLevel);
        });
    });

    // ==========================================
    // Printable Hospital Route Slip & WhatsApp Digital Pass Modal
    // ==========================================
    function openRouteSlipModal() {
        if (!state.currentRouteData) {
            alert('Please find a route first to generate the Hospital Route Slip.');
            return;
        }

        const route = state.currentRouteData;
        const now = new Date();
        const dateTimeStr = now.toLocaleDateString('en-IN', {
            day: '2-digit', month: 'short', year: 'numeric'
        }) + ', ' + now.toLocaleTimeString('en-IN', {
            hour: '2-digit', minute: '2-digit', hour12: true
        });

        // Token #
        const tokenInput = document.getElementById('patientTokenInput');
        const tokenNum = tokenInput && tokenInput.value ? tokenInput.value : '24';
        const slipTokenElem = document.getElementById('slipTokenNum');
        if (slipTokenElem) slipTokenElem.textContent = `#${tokenNum}`;

        const slipDateElem = document.getElementById('slipDateTime');
        if (slipDateElem) slipDateElem.textContent = dateTimeStr;

        const qmServing = document.getElementById('qmServingNow');
        const slipQueueElem = document.getElementById('slipQueueStatus');
        if (slipQueueElem) {
            slipQueueElem.textContent = qmServing ? `Serving ${qmServing.textContent}` : 'Active Queue';
        }

        // Start location
        const startSelect = document.getElementById('startLocation');
        const startId = startSelect ? startSelect.value : 'ENTRANCE_MAIN';
        const startNode = (state.mapData && state.mapData.nodes) ? state.mapData.nodes[startId] : null;
        const startName = startNode ? startNode.name : 'Main Entrance';
        const slipStartElem = document.getElementById('slipStartLoc');
        if (slipStartElem) slipStartElem.textContent = startName;

        // Destination location & Floor/Wing
        let destName = 'Hospital Facility';
        let floorWingText = 'Ground Floor • Main Wing';

        if (route.is_amenity_route) {
            destName = `${route.amenity_icon} ${route.found_name} (${route.amenity_title})`;
            const floorName = (state.floors && state.floors[route.found_floor]) ? state.floors[route.found_floor].name : `Floor ${route.found_floor}`;
            floorWingText = `${floorName} • Hospital Amenity`;
        } else if (state.activeTab === 'doctors' && state.selectedDoctor) {
            destName = `Dr. ${state.selectedDoctor.name} (${state.selectedDoctor.specialty}) • Room ${state.selectedDoctor.room_number || state.selectedDoctor.room_id}`;
            const targetFloor = state.selectedDoctor.floor;
            const floorName = (state.floors && state.floors[targetFloor]) ? state.floors[targetFloor].name : `Floor ${targetFloor}`;
            floorWingText = `${floorName} • ${state.selectedDoctor.wing || 'Consultation Wing'}`;
        } else if (state.activeTab === 'departments') {
            const rSelect = document.getElementById('roomSelect');
            const roomId = rSelect ? rSelect.value : null;
            const rNode = (state.mapData && state.mapData.nodes && roomId) ? state.mapData.nodes[roomId] : null;
            if (rNode) {
                destName = `${rNode.name} (${roomId})`;
                const floorName = (state.floors && state.floors[rNode.floor]) ? state.floors[rNode.floor].name : `Floor ${rNode.floor}`;
                floorWingText = `${floorName} • ${rNode.zone || 'Clinical Wing'}`;
            }
        } else if (state.activeTab === 'emergency') {
            destName = state.selectedEmergency ? `EMERGENCY: ${state.selectedEmergency}` : 'Emergency Ward';
            floorWingText = 'Ground Floor • Emergency Trauma Wing';
        } else if (state.activeTab === 'multistop') {
            const stops = state.multiStops.filter(s => s && s.trim());
            destName = `Multi-Stop Journey (${stops.length} locations)`;
            floorWingText = 'Multi-Floor Route Sequence';
        }

        const slipDestElem = document.getElementById('slipDestLoc');
        if (slipDestElem) slipDestElem.textContent = destName;

        const slipFloorElem = document.getElementById('slipFloorWing');
        if (slipFloorElem) slipFloorElem.textContent = floorWingText;

        // Mobility mode
        const modeLabels = {
            walk: '🚶 Walk (Stairs Preferred)',
            wheelchair: '♿ Wheelchair (Elevators Only)',
            stretcher: '🛏️ Stretcher (Bed Lifts Only)'
        };
        const slipMobilityElem = document.getElementById('slipMobility');
        if (slipMobilityElem) slipMobilityElem.textContent = modeLabels[route.travel_mode] || '🚶 By Walk';

        // Distance & Time
        const stepsText = route.estimated_steps > 0 ? ` (~${route.estimated_steps} steps)` : '';
        const slipMetricsElem = document.getElementById('slipMetrics');
        if (slipMetricsElem) {
            slipMetricsElem.textContent = `${route.total_distance} m • ~${route.estimated_minutes} min${stepsText}`;
        }

        // Ordered directions
        const ol = document.getElementById('slipDirectionsOrderedList');
        if (ol) {
            ol.innerHTML = '';
            const instructions = (state.selectedVoiceLang.startsWith('ta'))
                ? route.instructions_ta
                : route.instructions_en;

            if (instructions && instructions.length > 0) {
                instructions.forEach(step => {
                    if (step.type === 'stage_header') {
                        const liHeader = document.createElement('li');
                        liHeader.style.listStyle = 'none';
                        liHeader.style.fontWeight = 'bold';
                        liHeader.style.color = '#0369a1';
                        liHeader.style.marginTop = '6px';
                        liHeader.textContent = `▶ ${step.text}`;
                        ol.appendChild(liHeader);
                    } else {
                        const li = document.createElement('li');
                        li.textContent = `${step.text}`;
                        ol.appendChild(li);
                    }
                });
            }
        }

        const slipModal = document.getElementById('routeSlipModal');
        if (slipModal) slipModal.classList.remove('hidden');
    }

    const btnPrintRouteSlip = document.getElementById('btnPrintRouteSlip');
    if (btnPrintRouteSlip) {
        btnPrintRouteSlip.addEventListener('click', openRouteSlipModal);
    }

    const btnCloseSlipModal = document.getElementById('btnCloseSlipModal');
    if (btnCloseSlipModal) {
        btnCloseSlipModal.addEventListener('click', () => {
            const slipModal = document.getElementById('routeSlipModal');
            if (slipModal) slipModal.classList.add('hidden');
        });
    }

    const slipModalElem = document.getElementById('routeSlipModal');
    if (slipModalElem) {
        slipModalElem.addEventListener('click', (e) => {
            if (e.target === slipModalElem) slipModalElem.classList.add('hidden');
        });
    }

    const btnPrintSlipNow = document.getElementById('btnPrintSlipNow');
    if (btnPrintSlipNow) {
        btnPrintSlipNow.addEventListener('click', () => {
            window.print();
        });
    }

    const btnShareWhatsApp = document.getElementById('btnShareWhatsApp');
    if (btnShareWhatsApp) {
        btnShareWhatsApp.addEventListener('click', () => {
            if (!state.currentRouteData) return;
            const route = state.currentRouteData;

            const tokenInput = document.getElementById('patientTokenInput');
            const tokenNum = tokenInput && tokenInput.value ? tokenInput.value : '24';
            const startElem = document.getElementById('slipStartLoc');
            const destElem = document.getElementById('slipDestLoc');
            const floorElem = document.getElementById('slipFloorWing');
            const metricsElem = document.getElementById('slipMetrics');

            const startText = startElem ? startElem.textContent : 'Main Entrance';
            const destText = destElem ? destElem.textContent : 'Consultation Room';
            const floorText = floorElem ? floorElem.textContent : '1st Floor';
            const metricsText = metricsElem ? metricsElem.textContent : `${route.total_distance} m`;

            const instructions = (state.selectedVoiceLang.startsWith('ta'))
                ? route.instructions_ta
                : route.instructions_en;

            let stepLines = '';
            let sNum = 1;
            if (instructions && instructions.length > 0) {
                instructions.forEach(step => {
                    if (step.type === 'stage_header') {
                        stepLines += `\n*${step.text}*\n`;
                    } else {
                        stepLines += `${sNum}. ${step.text}\n`;
                        sNum++;
                    }
                });
            }

            const waMsg = `🏥 *CITY CARE HOSPITAL - NAVIGATION PASS*
🎟️ *Token #:* #${tokenNum}
📍 *From:* ${startText}
🎯 *Destination:* ${destText}
🏢 *Floor & Wing:* ${floorText}
📏 *Distance & Time:* ${metricsText}

📋 *Turn-by-Turn Route Directions:*
${stepLines}
⚠️ *Please present this pass at the department reception or nurse desk upon arrival.*`;

            const waUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(waMsg)}`;
            window.open(waUrl, '_blank');
        });
    }

    // ==========================================
    // Emergency Code Red Fire Evacuation Handler
    // ==========================================
    async function triggerFireEvacuation() {
        const startId = document.getElementById('startLocation') ? document.getElementById('startLocation').value : 'ENTRANCE_MAIN';

        try {
            const fireResult = await HospitalAPI.triggerFireEvacuation({
                current_location: startId,
                blocked_nodes: Array.from(state.blockedNodes)
            });

            state.currentRouteData = fireResult;

            // Render evacuation route
            mapRenderer.setRoute(fireResult);

            // Auto switch to current floor
            const startFloor = fireResult.path_details[0].floor;
            switchFloor(startFloor);

            floorButtons.forEach(b => {
                const f = parseInt(b.dataset.floor, 10);
                b.classList.toggle('has-route', fireResult.floors_traversed.includes(f));
            });

            displayRouteSummary(fireResult);
            checkMultiFloorTransitionBanner();

            // Announce voice alert if audio is enabled
            if (state.voiceEnabled) {
                playVoiceDirections();
            }
        } catch (err) {
            alert(err.message || 'Error calculating fire evacuation route.');
        }
    }

    const btnFire = document.getElementById('btnFireEvacuation');
    if (btnFire) {
        btnFire.addEventListener('click', triggerFireEvacuation);
    }

    // ==========================================
    // 1-Click Nearest Amenities Handler
    // ==========================================
    async function handleNearestAmenityClick(amenityType) {
        const startSelect = document.getElementById('startLocation');
        const startId = startSelect ? startSelect.value : 'ENTRANCE_MAIN';

        if (!startId) {
            alert('Please select your Current Location (or scan a Wall QR code).');
            return;
        }

        // Active visual state on buttons
        document.querySelectorAll('.btn-amenity-quick').forEach(b => {
            b.classList.toggle('active-amenity', b.dataset.amenity === amenityType);
        });

        try {
            const result = await HospitalAPI.getNearestAmenity({
                start: startId,
                amenity_type: amenityType,
                travel_mode: state.travelMode,
                blocked_nodes: Array.from(state.blockedNodes)
            });

            state.currentRouteData = result;

            // Render route on Blueprint Canvas
            mapRenderer.setRoute(result);

            // Auto-switch to start floor
            const startFloor = result.path_details[0].floor;
            switchFloor(startFloor);

            // Floor tabs indicators
            floorButtons.forEach(b => {
                const f = parseInt(b.dataset.floor, 10);
                b.classList.toggle('has-route', result.floors_traversed.includes(f));
            });

            displayRouteSummary(result);
            checkMultiFloorTransitionBanner();

            // Audio voice alert if guidance is enabled
            if (state.voiceEnabled) {
                const alertVoice = state.selectedVoiceLang.startsWith('ta') ? result.amenity_alert_ta : result.amenity_alert_en;
                voice.speakText(alertVoice, state.selectedVoiceLang);
            }
        } catch (err) {
            alert(err.message || 'Error locating nearest amenity.');
        }
    }

    document.querySelectorAll('.btn-amenity-quick').forEach(btn => {
        btn.addEventListener('click', () => {
            const amenityType = btn.dataset.amenity;
            handleNearestAmenityClick(amenityType);
        });
    });

    const startLocationSelect = document.getElementById('startLocation');
    if (startLocationSelect) {
        startLocationSelect.addEventListener('change', () => {
            updateMapHighlights();
        });
    }

    document.getElementById('btnZoomIn').addEventListener('click', () => mapRenderer.zoomIn());
    document.getElementById('btnZoomOut').addEventListener('click', () => mapRenderer.zoomOut());
    document.getElementById('btnResetView').addEventListener('click', () => mapRenderer.resetView());
    document.getElementById('btnAnimatePath').addEventListener('click', () => {
        if (state.currentRouteData) {
            mapRenderer.animOffset = 0;
            if (state.voiceEnabled) {
                playVoiceDirections();
            }
        }
    });

    document.getElementById('btnOpenQrModal').addEventListener('click', () => {
        qrSimulator.open(state.qrMarkers);
    });

    document.getElementById('btnFindRoute').addEventListener('click', triggerRouteCalculation);
    document.getElementById('btnSpeakDirections').addEventListener('click', toggleAudioPlay);

    // ==========================================
    // 8. Dijkstra Routing Execution
    // ==========================================
    async function triggerRouteCalculation() {
        const startId = document.getElementById('startLocation').value;

        if (!startId) {
            alert('Please select your Current Location (or scan a Wall QR code).');
            return;
        }

        // A. Multi-Stop Tab Calculation
        if (state.activeTab === 'multistop') {
            const activeStops = state.multiStops.filter(s => s && s.trim());
            if (activeStops.length === 0) {
                alert('Please select at least one destination stop for your journey.');
                return;
            }

            // Check Smart Queue Reordering Advisory
            const tokenInput = document.getElementById('patientTokenInput');
            const tokenVal = tokenInput ? parseInt(tokenInput.value, 10) : 24;
            try {
                const optCheck = await HospitalAPI.optimizeJourney(startId, activeStops, tokenVal);
                const advBanner = document.getElementById('queueAdvisoryBanner');
                const advText = document.getElementById('queueAdvisoryText');
                const btnApplyOpt = document.getElementById('btnApplyOptimizedQueue');

                if (optCheck && optCheck.can_optimize) {
                    if (advText) {
                        advText.textContent = state.selectedVoiceLang.startsWith('ta') ? optCheck.advisory_ta : optCheck.advisory_en;
                    }
                    if (advBanner) advBanner.classList.remove('hidden');

                    if (btnApplyOpt) {
                        btnApplyOpt.onclick = () => {
                            state.multiStops = optCheck.optimized_stops;
                            renderMultiStopRows();
                            if (advBanner) advBanner.classList.add('hidden');
                            triggerRouteCalculation();
                        };
                    }
                } else {
                    if (advBanner) advBanner.classList.add('hidden');
                }
            } catch (qErr) {
                console.warn('Queue advisory check:', qErr);
            }

            try {
                const routeResult = await HospitalAPI.calculateMultiStopRoute({
                    start: startId,
                    stops: activeStops,
                    travel_mode: state.travelMode,
                    blocked_nodes: Array.from(state.blockedNodes)
                });

                state.currentRouteData = routeResult;

                // Render route on Blueprint Canvas
                mapRenderer.setRoute(routeResult);

                // Auto-switch to start floor
                const startFloor = routeResult.path_details[0].floor;
                switchFloor(startFloor);

                // Floor tabs indicators
                floorButtons.forEach(b => {
                    const f = parseInt(b.dataset.floor, 10);
                    b.classList.toggle('has-route', routeResult.floors_traversed.includes(f));
                });

                displayRouteSummary(routeResult);
                checkMultiFloorTransitionBanner();

                if (state.voiceEnabled) {
                    playVoiceDirections();
                }

            } catch (err) {
                alert(err.message || 'Error calculating multi-stop route.');
            }
            return;
        }

        // B. Single Destination Routing (Doctor / Department / Emergency)
        let destinationQuery = null;
        let isDoctor = false;

        if (state.activeTab === 'doctors') {
            const docId = document.getElementById('doctorSelect').value;
            if (!docId) {
                alert('Please select a Specialist Doctor.');
                return;
            }
            destinationQuery = docId;
            isDoctor = true;
        } else if (state.activeTab === 'departments') {
            const roomId = document.getElementById('roomSelect').value;
            if (!roomId) {
                alert('Please select a Room or Department.');
                return;
            }
            destinationQuery = roomId;
            isDoctor = false;
        } else if (state.activeTab === 'emergency') {
            if (!state.selectedEmergency) {
                alert('Please click one of the Emergency destination buttons.');
                return;
            }
            destinationQuery = state.selectedEmergency;
            isDoctor = false;
        }

        try {
            // Call Flask API with travel_mode & blocked_nodes
            const routeResult = await HospitalAPI.calculateShortestRoute({
                start: startId,
                destination: destinationQuery,
                is_doctor: isDoctor,
                travel_mode: state.travelMode,
                blocked_nodes: Array.from(state.blockedNodes)
            });

            state.currentRouteData = routeResult;

            // Render route on Blueprint Canvas
            mapRenderer.setRoute(routeResult);

            // Auto-switch to start floor
            const startFloor = routeResult.path_details[0].floor;
            switchFloor(startFloor);

            // Floor tabs indicators
            floorButtons.forEach(b => {
                const f = parseInt(b.dataset.floor, 10);
                b.classList.toggle('has-route', routeResult.floors_traversed.includes(f));
            });

            displayRouteSummary(routeResult);
            checkMultiFloorTransitionBanner();

            // Audio plays ONLY IF explicitly enabled by user
            if (state.voiceEnabled) {
                playVoiceDirections();
            }

        } catch (err) {
            alert(err.message || 'Error calculating shortest route.');
        }
    }

    // ==========================================
    // 9. Results & Directions Display
    // ==========================================
    function displayRouteSummary(route) {
        const card = document.getElementById('routeResultCard');
        card.classList.remove('hidden');

        const titleElem = document.getElementById('resCardTitle');
        const subtitleElem = document.getElementById('resCardSubtitle');
        const fireAlertBanner = document.getElementById('fireEvacuationAlertBanner');
        const fireAlertText = document.getElementById('fireAlertBannerText');
        const amenityBanner = document.getElementById('amenityAlertBanner');
        const amenityIconElem = document.getElementById('amenityNoticeIcon');
        const amenityTitleElem = document.getElementById('amenityNoticeTitle');
        const amenityTextElem = document.getElementById('amenityNoticeText');

        if (route.is_fire_evacuation) {
            if (titleElem) titleElem.textContent = '🚨 CODE RED: Fire Evacuation Route';
            if (subtitleElem) subtitleElem.textContent = `Safest Exit: ${route.nearest_exit} (Elevators strictly disabled)`;
            if (fireAlertBanner) {
                fireAlertBanner.classList.remove('hidden');
                if (fireAlertText) {
                    fireAlertText.textContent = state.selectedVoiceLang.startsWith('ta') ? route.fire_alert_ta : route.fire_alert_en;
                }
            }
            if (amenityBanner) amenityBanner.classList.add('hidden');
        } else if (route.is_amenity_route) {
            if (titleElem) titleElem.textContent = `${route.amenity_icon} Nearest ${route.amenity_title}`;
            const floorTitle = (state.floors && state.floors[route.found_floor]) ? state.floors[route.found_floor].name : `Floor ${route.found_floor}`;
            if (subtitleElem) subtitleElem.textContent = `${route.found_name} (${floorTitle})`;
            if (fireAlertBanner) fireAlertBanner.classList.add('hidden');
            if (amenityBanner) {
                amenityBanner.classList.remove('hidden');
                if (amenityIconElem) amenityIconElem.textContent = route.amenity_icon || '⚡';
                if (amenityTitleElem) amenityTitleElem.textContent = state.selectedVoiceLang.startsWith('ta') ? route.amenity_title_ta : route.amenity_title;
                if (amenityTextElem) amenityTextElem.textContent = state.selectedVoiceLang.startsWith('ta') ? route.amenity_alert_ta : route.amenity_alert_en;
            }
        } else if (route.is_multi_stop) {
            const stopCount = (route.legs && route.legs.length) ? route.legs.length : 'Multi';
            if (titleElem) titleElem.textContent = `🏥 Multi-Stop Journey (${stopCount} Stops Completed)`;
            if (subtitleElem) subtitleElem.textContent = `Optimized Visiting Order Planned (${route.total_distance} m)`;
            if (fireAlertBanner) fireAlertBanner.classList.add('hidden');
            if (amenityBanner) amenityBanner.classList.add('hidden');
        } else {
            if (titleElem) titleElem.textContent = 'Calculated Route Summary';
            if (subtitleElem) subtitleElem.textContent = 'Guaranteed Shortest Path (Dijkstra)';
            if (fireAlertBanner) fireAlertBanner.classList.add('hidden');
            if (amenityBanner) amenityBanner.classList.add('hidden');
        }

        document.getElementById('resDistance').textContent = `${route.total_distance} m`;
        document.getElementById('resTime').textContent = `~${route.estimated_minutes} min`;
        document.getElementById('resSteps').textContent = route.estimated_steps > 0 ? `~${route.estimated_steps}` : 'N/A';
        
        const modeLabels = { walk: '🚶 Walk', wheelchair: '♿ Wheelchair', stretcher: '🛏️ Stretcher' };
        document.getElementById('resMode').textContent = modeLabels[route.travel_mode] || 'Walk';

        // Obstacle Reroute Alert Banner
        const rerouteBanner = document.getElementById('rerouteAlertBanner');
        const rerouteText = document.getElementById('rerouteAlertText');
        if (route.rerouted && (route.reroute_alert_en || route.reroute_alert_ta)) {
            const alertMsg = state.selectedVoiceLang.startsWith('ta') ? route.reroute_alert_ta : route.reroute_alert_en;
            rerouteText.textContent = alertMsg;
            rerouteBanner.classList.remove('hidden');

            // If voice enabled, speak the reroute notice
            if (state.voiceEnabled) {
                voice.speakText(alertMsg, state.selectedVoiceLang);
            }
        } else {
            rerouteBanner.classList.add('hidden');
        }

        // Directions list
        const listContainer = document.getElementById('directionsList');
        listContainer.innerHTML = '';

        const instructions = (state.selectedVoiceLang.startsWith('ta')) 
            ? route.instructions_ta 
            : route.instructions_en;

        instructions.forEach((step, idx) => {
            if (step.type === 'stage_header') {
                const stageDiv = document.createElement('div');
                stageDiv.className = 'stage-divider-card';
                stageDiv.innerHTML = `
                    <div class="stage-divider-title">${step.icon} ${step.text}</div>
                `;
                listContainer.appendChild(stageDiv);
                return;
            }

            const stepDiv = document.createElement('div');
            stepDiv.className = `step-card ${step.type === 'fire_alert' ? 'active-step' : ''}`;
            stepDiv.dataset.index = idx;
            stepDiv.innerHTML = `
                <div class="step-icon">${step.icon}</div>
                <div class="step-content">
                    <div class="step-num">STEP ${step.step}</div>
                    <div class="step-text">${step.text}</div>
                </div>
            `;

            stepDiv.addEventListener('click', () => {
                highlightStepCard(idx);
                if (step.node_id) {
                    mapRenderer.highlightNode(step.node_id);
                    if (typeof step.floor === 'number' && step.floor !== state.currentFloor) {
                        switchFloor(step.floor);
                    }
                }
                // Speak individual step on user click
                voice.speakText(step.text, state.selectedVoiceLang);
            });

            listContainer.appendChild(stepDiv);
        });

        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function highlightStepCard(index) {
        document.querySelectorAll('.step-card').forEach((c, idx) => {
            c.classList.toggle('active-step', idx === index);
        });
    }

    function toggleAudioPlay() {
        if (!state.currentRouteData) return;
        if (voice.isSpeakingNow) {
            voice.stop();
            resetAudioButton();
        } else {
            playVoiceDirections();
        }
    }

    function playVoiceDirections() {
        if (!state.currentRouteData) return;
        const instructions = (state.selectedVoiceLang.startsWith('ta'))
            ? state.currentRouteData.instructions_ta
            : state.currentRouteData.instructions_en;

        document.getElementById('audioBtnIcon').textContent = '⏹️';
        document.getElementById('audioBtnText').textContent = 'Stop Audio';

        voice.speakDirections(instructions, state.selectedVoiceLang);
    }

    function resetAudioButton() {
        document.getElementById('audioBtnIcon').textContent = '🔊';
        document.getElementById('audioBtnText').textContent = 'Read Aloud';
    }

    // ==========================================
    // 10. Helpers for Initial Population
    // ==========================================
    function populateStartLocations(locationsByFloor, floors) {
        const select = document.getElementById('startLocation');
        select.innerHTML = '';

        for (const [floorNum, locations] of Object.entries(locationsByFloor)) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = floors[floorNum] ? floors[floorNum].name : `Floor ${floorNum}`;

            locations.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc.id;
                opt.textContent = `${loc.name}`;
                if (loc.id === 'ENTRANCE_MAIN') opt.selected = true;
                optgroup.appendChild(opt);
            });

            select.appendChild(optgroup);
        }
    }

    function populateDoctorsDropdown(doctors) {
        const select = document.getElementById('doctorSelect');
        select.innerHTML = '<option value="">-- Choose Specialist Doctor --</option>';

        doctors.forEach(doc => {
            const opt = document.createElement('option');
            opt.value = doc.id;
            opt.textContent = `${doc.specialty} — ${doc.name} (${doc.room_name})`;
            select.appendChild(opt);
        });
    }

    function populateRoomsDropdown(locationsByFloor, floors) {
        const select = document.getElementById('roomSelect');
        select.innerHTML = '<option value="">-- Choose Room / Ward --</option>';

        for (const [floorNum, locations] of Object.entries(locationsByFloor)) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = floors[floorNum] ? floors[floorNum].name : `Floor ${floorNum}`;

            locations.forEach(loc => {
                if (loc.type === 'room' || loc.type === 'amenity' || loc.type === 'reception' || loc.type === 'entrance') {
                    const opt = document.createElement('option');
                    opt.value = loc.id;
                    opt.textContent = loc.name;
                    optgroup.appendChild(opt);
                }
            });

            select.appendChild(optgroup);
        }
    }

    function populateEmergencyButtons(emergencyList) {
        const container = document.getElementById('emergencyButtonsContainer');
        container.innerHTML = '';

        emergencyList.forEach(item => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-emergency-item';
            btn.innerHTML = `<span>${item.icon}</span> <span>${item.name}</span>`;

            btn.addEventListener('click', () => {
                document.querySelectorAll('.btn-emergency-item').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                state.selectedEmergency = item.id;
                updateMapHighlights();
                triggerRouteCalculation();
            });

            container.appendChild(btn);
        });
    }
});
