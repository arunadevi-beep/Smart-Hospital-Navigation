/**
 * API Client Module
 * Handles all REST API communications with the Python Flask backend.
 */
const HospitalAPI = {
    async getHospitalMap() {
        const response = await fetch('/api/hospital-map');
        if (!response.ok) throw new Error('Failed to load hospital map layout');
        return await response.json();
    },

    async getDoctors() {
        const response = await fetch('/api/doctors');
        if (!response.ok) throw new Error('Failed to load doctors directory');
        return await response.json();
    },

    async getLocations() {
        const response = await fetch('/api/locations');
        if (!response.ok) throw new Error('Failed to load hospital locations');
        return await response.json();
    },

    async getFloorDirectory(floor) {
        const response = await fetch(`/api/floor-directory/${floor}`);
        if (!response.ok) throw new Error(`Failed to load directory for floor ${floor}`);
        return await response.json();
    },

    async getEmergencyRoutes() {
        const response = await fetch('/api/emergency-routes');
        if (!response.ok) throw new Error('Failed to load emergency routes');
        return await response.json();
    },

    async getBlockableFacilities() {
        const response = await fetch('/api/blockable-facilities');
        if (!response.ok) throw new Error('Failed to load blockable facilities');
        return await response.json();
    },

    async getQrLocations() {
        const response = await fetch('/api/qr-locations');
        if (!response.ok) throw new Error('Failed to load QR markers');
        return await response.json();
    },

    async calculateShortestRoute(params) {
        const response = await fetch('/api/navigate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Navigation routing failed');
        }
        return data;
    },

    async calculateMultiStopRoute(params) {
        const response = await fetch('/api/navigate-multistop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Multi-stop routing failed');
        }
        return data;
    },

    async triggerFireEvacuation(params) {
        const response = await fetch('/api/fire-evacuate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Fire evacuation routing failed');
        }
        return data;
    },

    async searchSymptoms(query) {
        const response = await fetch(`/api/search-symptoms?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Symptom search failed');
        return await response.json();
    },

    async getQueueStatus(doctorId, patientToken) {
        const response = await fetch('/api/queue-status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ doctor_id: doctorId, patient_token: patientToken })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Failed to fetch queue status');
        return data;
    },

    async optimizeJourney(start, stops, patientToken) {
        const response = await fetch('/api/optimize-journey', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start, stops, patient_token: patientToken })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Failed to optimize journey');
        return data;
    },

    async getCrowdDensity() {
        const response = await fetch('/api/crowd-density');
        if (!response.ok) throw new Error('Failed to load crowd density');
        return await response.json();
    },

    async getAmenities() {
        const response = await fetch('/api/amenities');
        if (!response.ok) throw new Error('Failed to load amenities list');
        return await response.json();
    },

    async getNearestAmenity(params) {
        const response = await fetch('/api/nearest-amenity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to locate nearest amenity');
        }
        return data;
    }
};

window.HospitalAPI = HospitalAPI;

