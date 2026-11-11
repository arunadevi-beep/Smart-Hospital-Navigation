/**
 * Indoor QR Code Localization Simulator
 * Replaces GPS in indoor environments: Patients scan physical QR codes placed on hospital walls/pillars.
 */
class QrSimulator {
    constructor(modalId, gridId, onSelectLocation) {
        this.modal = document.getElementById(modalId);
        this.grid = document.getElementById(gridId);
        this.onSelectLocation = onSelectLocation;

        this._initEvents();
    }

    _initEvents() {
        const closeBtn = document.getElementById('btnCloseQrModal');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.close());
        }

        // Close on backdrop click
        if (this.modal) {
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) this.close();
            });
        }
    }

    open(markers) {
        if (!this.modal || !this.grid) return;
        this.grid.innerHTML = '';

        markers.forEach(marker => {
            const card = document.createElement('div');
            card.className = 'qr-card';
            card.innerHTML = `
                <div class="qr-graphic">▦</div>
                <div class="qr-info">
                    <h5>${marker.name}</h5>
                    <p>📍 ${marker.floor_name} • Code: ${marker.qr_code}</p>
                </div>
            `;
            card.addEventListener('click', () => {
                if (this.onSelectLocation) {
                    this.onSelectLocation(marker.node_id, marker.name, marker.floor);
                }
                this.close();
            });
            this.grid.appendChild(card);
        });

        this.modal.classList.remove('hidden');
    }

    close() {
        if (this.modal) {
            this.modal.classList.add('hidden');
        }
    }
}

window.QrSimulator = QrSimulator;

