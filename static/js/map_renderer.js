/**
 * Architectural Hospital Floor Plan Map Renderer (Canvas)
 * Distinct Color Coding:
 * - 🔵 Standard Patient Rooms & Clinics: Cool Medical Blue
 * - 🔴 Emergency & ICU: High-Visibility Emergency Red
 * - 🟣 Elevators / Lifts: Royal Purple
 * - 🟡 Staircases: Golden Amber
 * - 🟢 Highlighting: Start Location (Current Location) in Vibrant Green Halo
 * - 🚩 Highlighting: Destination in Vibrant Crimson Red Halo
 */
class HospitalMapRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');

        this.currentFloor = 0;
        this.mapData = null;
        this.currentRoute = null;
        this.blockedNodes = new Set();
        this.showCrowdHeatmap = false;
        this.crowdData = {};
        this.crowdLevelFilter = 'all'; // 'all' | 'low' | 'moderate' | 'high'

        // Start and Destination highlighting
        this.startNodeId = null;
        this.destNodeId = null;

        // Auto-fit scale & offsets
        this.scale = 1.0;
        this.offsetX = 0;
        this.offsetY = 0;
        this.userZoom = 1.0;

        // Animation state
        this.animOffset = 0;
        this.animId = null;
        this.highlightStepNodeId = null;

        // Callbacks
        this.onRoomSelect = null;
        this.onFloorTransitionTap = null;

        this._initEvents();
    }

    init(mapData) {
        this.mapData = mapData;
        this.resize();
        this.render();
        this.startAnimation();
    }

    setFloor(floorNum) {
        this.currentFloor = parseInt(floorNum, 10);
        this.render();
    }

    setRoute(routeData) {
        this.currentRoute = routeData;
        if (routeData && routeData.path_nodes && routeData.path_nodes.length > 0) {
            this.startNodeId = routeData.path_nodes[0];
            this.destNodeId = routeData.path_nodes[routeData.path_nodes.length - 1];
        } else {
            this.startNodeId = null;
            this.destNodeId = null;
        }
        this.render();
    }

    setHighlightedPoints(startId, destId) {
        this.startNodeId = startId || null;
        this.destNodeId = destId || null;
        this.render();
    }

    setBlockedNodes(nodesList) {
        this.blockedNodes = new Set(nodesList || []);
        this.render();
    }

    setCrowdHeatmap(show, crowdData) {
        this.showCrowdHeatmap = Boolean(show);
        if (crowdData) this.crowdData = crowdData;
        this.render();
    }

    setCrowdLevelFilter(level) {
        this.crowdLevelFilter = level || 'all';
        if (level && level !== 'all') {
            this.showCrowdHeatmap = true;
        }
        this.render();
    }

    clearRoute() {
        this.currentRoute = null;
        this.highlightStepNodeId = null;
        this.render();
    }

    highlightNode(nodeId) {
        this.highlightStepNodeId = nodeId;
        this.render();
    }

    resize() {
        const wrapper = this.canvas.parentElement;
        if (wrapper) {
            this.canvas.width = wrapper.clientWidth || 920;
            this.canvas.height = Math.max(540, wrapper.clientHeight || 560);
        }
        this._calculateFit();
    }

    _calculateFit() {
        const bpW = 880;
        const bpH = 540;

        const scaleX = (this.canvas.width - 36) / bpW;
        const scaleY = (this.canvas.height - 36) / bpH;
        this.scale = Math.min(scaleX, scaleY) * this.userZoom;

        this.offsetX = (this.canvas.width - bpW * this.scale) / 2;
        this.offsetY = (this.canvas.height - bpH * this.scale) / 2;
    }

    resetView() {
        this.userZoom = 1.0;
        this._calculateFit();
        this.render();
    }

    zoomIn() {
        this.userZoom = Math.min(1.6, this.userZoom + 0.15);
        this._calculateFit();
        this.render();
    }

    zoomOut() {
        this.userZoom = Math.max(0.85, this.userZoom - 0.15);
        this._calculateFit();
        this.render();
    }

    _initEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.render();
        });

        this.canvas.addEventListener('click', (e) => {
            if (!this.mapData) return;
            const rect = this.canvas.getBoundingClientRect();
            const clickX = (e.clientX - rect.left - this.offsetX) / this.scale;
            const clickY = (e.clientY - rect.top - this.offsetY) / this.scale;

            // 1. One-Tap Lift / Stairs transition
            if (this.currentRoute && this.currentRoute.path_details) {
                for (let i = 0; i < this.currentRoute.path_details.length - 1; i++) {
                    const p1 = this.currentRoute.path_details[i];
                    const p2 = this.currentRoute.path_details[i + 1];

                    if (p1.floor === this.currentFloor && p2.floor !== this.currentFloor) {
                        const dx = Math.abs(clickX - p1.x);
                        const dy = clickY - p1.y;
                        const inNode = (dx <= 45 && Math.abs(dy) <= 40);
                        const inBadge = (dx <= 150 && dy >= -55 && dy <= -10);

                        if (inNode || inBadge) {
                            if (this.onFloorTransitionTap) {
                                this.onFloorTransitionTap(p2.floor, p1.name);
                                return;
                            }
                        }
                    }
                }
            }

            // 2. Click on a Room
            for (const [nodeId, node] of Object.entries(this.mapData.nodes)) {
                if (node.floor === this.currentFloor && (node.type === 'room' || node.type === 'reception')) {
                    const w = node.w || 120;
                    const h = node.h || 70;
                    if (clickX >= node.x - w/2 && clickX <= node.x + w/2 &&
                        clickY >= node.y - h/2 && clickY <= node.y + h/2) {
                        if (this.onRoomSelect) this.onRoomSelect(nodeId);
                        break;
                    }
                }
            }
        });

        // Interactive cursor on hover
        this.canvas.addEventListener('mousemove', (e) => {
            if (!this.mapData) return;
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = (e.clientX - rect.left - this.offsetX) / this.scale;
            const mouseY = (e.clientY - rect.top - this.offsetY) / this.scale;

            let hovering = false;

            if (this.currentRoute && this.currentRoute.path_details) {
                for (let i = 0; i < this.currentRoute.path_details.length - 1; i++) {
                    const p1 = this.currentRoute.path_details[i];
                    const p2 = this.currentRoute.path_details[i + 1];
                    if (p1.floor === this.currentFloor && p2.floor !== this.currentFloor) {
                        const dx = Math.abs(mouseX - p1.x);
                        const dy = mouseY - p1.y;
                        if ((dx <= 45 && Math.abs(dy) <= 40) || (dx <= 150 && dy >= -55 && dy <= -10)) {
                            hovering = true;
                            break;
                        }
                    }
                }
            }

            if (!hovering) {
                for (const [nodeId, node] of Object.entries(this.mapData.nodes)) {
                    if (node.floor === this.currentFloor && (node.type === 'room' || node.type === 'reception')) {
                        const w = node.w || 120;
                        const h = node.h || 70;
                        if (mouseX >= node.x - w/2 && mouseX <= node.x + w/2 &&
                            mouseY >= node.y - h/2 && mouseY <= node.y + h/2) {
                            hovering = true;
                            break;
                        }
                    }
                }
            }

            this.canvas.style.cursor = hovering ? 'pointer' : 'default';
        });
    }

    startAnimation() {
        const loop = () => {
            this.animOffset = (this.animOffset + 0.6) % 24;
            this.render();
            this.animId = requestAnimationFrame(loop);
        };
        this.animId = requestAnimationFrame(loop);
    }

    render() {
        if (!this.mapData) return;
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        ctx.save();
        ctx.translate(this.offsetX, this.offsetY);
        ctx.scale(this.scale, this.scale);

        // 1. Building Shell & Hallways
        this._drawBuildingShell(ctx);
        this._drawHallwayGrid(ctx);

        // 1b. Live Crowd Density & Rush Heatmap
        if (this.showCrowdHeatmap) {
            this._drawCrowdHeatmap(ctx);
        }

        // 2. Rooms (Blue for standard, Red for emergency, Highlighting for Start/Dest)
        this._drawFloorRooms(ctx);

        // 3. Central Core (Purple for Lifts, Amber for Stairs)
        this._drawVerticalTransportCore(ctx);

        // 4. Blocked Hazards
        if (this.blockedNodes.size > 0) {
            this._drawBlockedHazards(ctx);
        }

        // 5. Shortest Path Route
        if (this.currentRoute) {
            this._drawShortestPath(ctx);
        }

        // 6. Highlighted step waypoint
        if (this.highlightStepNodeId) {
            this._drawHighlightNode(ctx, this.highlightStepNodeId);
        }

        ctx.restore();
    }

    _drawCrowdHeatmap(ctx) {
        if (!this.mapData || !this.crowdData) return;

        const isFiltered = this.crowdLevelFilter && this.crowdLevelFilter !== 'all';

        for (const [nodeId, metrics] of Object.entries(this.crowdData)) {
            const node = this.mapData.nodes[nodeId];
            if (!node || node.floor !== this.currentFloor) continue;

            const x = node.x;
            const y = node.y;
            const level = metrics.level || 'low';
            const pct = metrics.percentage || 20;

            const isMatch = !isFiltered || (level === this.crowdLevelFilter);

            let auraColor = 'rgba(34, 197, 94, 0.28)';
            let badgeBg = '#16a34a';

            if (level === 'high') {
                auraColor = 'rgba(239, 68, 68, 0.35)';
                badgeBg = '#dc2626';
            } else if (level === 'moderate') {
                auraColor = 'rgba(245, 158, 11, 0.3)';
                badgeBg = '#d97706';
            }

            ctx.save();

            if (isFiltered && !isMatch) {
                ctx.globalAlpha = 0.15; // Dim non-matching nodes
            } else {
                ctx.globalAlpha = 1.0;
            }

            const radius = level === 'high' ? 42 : (level === 'moderate' ? 32 : 22);
            const grad = ctx.createRadialGradient(x, y, 4, x, y, radius);
            grad.addColorStop(0, auraColor);
            grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();

            // Crowd Chip
            const chipW = 50;
            const chipH = 15;
            ctx.fillStyle = badgeBg;
            ctx.beginPath();
            ctx.roundRect(x - chipW/2, y + 14, chipW, chipH, 7);
            ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 8px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            const icon = level === 'high' ? '🔥' : (level === 'moderate' ? '👥' : '🟢');
            ctx.fillText(`${icon} ${pct}%`, x, y + 21.5);

            // If specifically filtered & matching, draw a prominent animated ring!
            if (isFiltered && isMatch) {
                ctx.strokeStyle = badgeBg;
                ctx.lineWidth = 2.5;
                ctx.setLineDash([6, 4]);
                ctx.lineDashOffset = -this.animOffset;
                ctx.beginPath();
                ctx.arc(x, y, radius + 8, 0, Math.PI * 2);
                ctx.stroke();
                ctx.setLineDash([]);

                // Floating label chip above room
                ctx.fillStyle = badgeBg;
                ctx.font = 'bold 8.5px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(`${icon} ${level.toUpperCase()} RUSH`, x, y - radius - 2);
            }

            ctx.restore();
        }
    }

    _drawBuildingShell(ctx) {
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 3.5;
        ctx.beginPath();
        ctx.roundRect(30, 20, 820, 500, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#cbd5e1';
        ctx.font = 'bold 22px Inter, sans-serif';
        ctx.textAlign = 'right';
        const floorTitle = this.currentFloor === 0 ? 'GROUND FLOOR' : (this.currentFloor === 1 ? '1ST FLOOR (OPD)' : '2ND FLOOR (SPECIALTY & ICU)');
        ctx.fillText(floorTitle, 830, 48);
    }

    _drawHallwayGrid(ctx) {
        ctx.fillStyle = '#f1f5f9';
        ctx.strokeStyle = '#cbd5e1';
        ctx.lineWidth = 1.5;

        // East-West Corridors
        ctx.fillRect(160, 135, 560, 50);
        ctx.fillRect(160, 255, 560, 50);
        ctx.fillRect(160, 395, 560, 50);

        // North-South Connecting Hallways
        ctx.fillRect(155, 135, 50, 310);
        ctx.fillRect(415, 135, 50, 310);
        ctx.fillRect(675, 135, 50, 310);

        // Corridor Edges
        ctx.strokeStyle = '#cbd5e1';
        ctx.lineWidth = 1;
        ctx.strokeRect(160, 135, 560, 50);
        ctx.strokeRect(160, 255, 560, 50);
        ctx.strokeRect(160, 395, 560, 50);

        // Corridor center tile line markings
        ctx.strokeStyle = '#e2e8f0';
        for (let x = 180; x < 720; x += 40) {
            ctx.beginPath();
            ctx.moveTo(x, 255);
            ctx.lineTo(x, 305);
            ctx.stroke();
        }
    }

    _drawFloorRooms(ctx) {
        for (const [nodeId, node] of Object.entries(this.mapData.nodes)) {
            if (node.floor !== this.currentFloor) continue;
            if (node.type !== 'room' && node.type !== 'reception' && node.type !== 'entrance' && node.type !== 'amenity' && node.type !== 'fire_exit') continue;

            const w = node.w || 120;
            const h = node.h || 70;
            const rx = node.x - w / 2;
            const ry = node.y - h / 2;

            // Handle Fire Exit Doors specially
            if (node.type === 'fire_exit') {
                this._drawFireExitDoor(ctx, node, rx, ry, w, h);
                continue;
            }

            const isStart = (nodeId === this.startNodeId);
            const isDest = (nodeId === this.destNodeId);
            const isEmergency = nodeId.includes('EMERGENCY') || nodeId.includes('ICU') || node.availability_status === 'emergency';

            let strokeColor = '#0284c7';   // Standard Rooms: Blue
            let fillColor = '#e0f2fe';     // Standard Rooms: Light Blue
            let badgeBg = '#bae6fd';
            let badgeColor = '#0369a1';
            let borderWidth = 2;

            if (isEmergency) {
                // Emergency Rooms: Red
                strokeColor = '#ef4444';
                fillColor = '#fee2e2';
                badgeBg = '#fecdd3';
                badgeColor = '#be123c';
                borderWidth = 2.2;
            } else if (node.type === 'amenity') {
                // Amenities: Soft Slate
                strokeColor = '#64748b';
                fillColor = '#f1f5f9';
                badgeBg = '#e2e8f0';
                badgeColor = '#334155';
            }

            // SPECIAL HIGHLIGHTING: IF THIS ROOM IS START OR DESTINATION
            if (isStart) {
                // Start Room: Vibrant Glowing Green
                strokeColor = '#16a34a';
                fillColor = '#dcfce7';
                badgeBg = '#86efac';
                badgeColor = '#14532d';
                borderWidth = 3.5;

                // Pulsing Green Aura Halo
                ctx.save();
                ctx.strokeStyle = 'rgba(22, 163, 74, 0.4)';
                ctx.lineWidth = 10 + Math.sin(this.animOffset * 0.4) * 3;
                ctx.beginPath();
                ctx.roundRect(rx - 4, ry - 4, w + 8, h + 8, 8);
                ctx.stroke();
                ctx.restore();
            } else if (isDest) {
                // Destination Room: Vibrant Glowing Crimson Red
                strokeColor = '#dc2626';
                fillColor = '#ffe4e6';
                badgeBg = '#fca5a5';
                badgeColor = '#7f1d1d';
                borderWidth = 3.5;

                // Pulsing Red Aura Halo
                ctx.save();
                ctx.strokeStyle = 'rgba(220, 38, 38, 0.45)';
                ctx.lineWidth = 10 + Math.sin(this.animOffset * 0.4) * 3;
                ctx.beginPath();
                ctx.roundRect(rx - 4, ry - 4, w + 8, h + 8, 8);
                ctx.stroke();
                ctx.restore();
            }

            // Room Box
            ctx.fillStyle = fillColor;
            ctx.strokeStyle = strokeColor;
            ctx.lineWidth = borderWidth;
            ctx.beginPath();
            ctx.roundRect(rx, ry, w, h, 6);
            ctx.fill();
            ctx.stroke();

            // Door Opening Notch
            if (node.door_x && node.door_y) {
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(node.door_x, node.door_y, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = strokeColor;
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            // Room Code Badge (top-left)
            let badgeText = node.room_code || 'RM';
            let badgeW = 42;
            if (isStart) {
                badgeText = '📍 START';
                badgeW = 54;
            } else if (isDest) {
                badgeText = '🏁 DEST';
                badgeW = 50;
            }

            ctx.fillStyle = badgeBg;
            ctx.beginPath();
            ctx.roundRect(rx + 6, ry + 6, badgeW, 16, 4);
            ctx.fill();

            ctx.fillStyle = badgeColor;
            ctx.font = 'bold 8.5px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(badgeText, rx + 6 + badgeW / 2, ry + 17);

            // Room Name
            ctx.fillStyle = (isStart || isDest) ? '#0f172a' : '#0f172a';
            ctx.font = (isStart || isDest) ? 'bold 10.5px Inter, sans-serif' : 'bold 10px Inter, sans-serif';
            ctx.textAlign = 'center';

            const parts = node.name.split(' - ');
            if (parts.length > 1) {
                ctx.fillText(parts[0], node.x, node.y - 2);
                ctx.font = '8px Inter, sans-serif';
                ctx.fillStyle = '#475569';
                const sub = parts[1].length > 18 ? parts[1].substring(0, 16) + '..' : parts[1];
                ctx.fillText(sub, node.x, node.y + 12);
            } else {
                ctx.fillText(node.name.length > 18 ? node.name.substring(0, 16) + '..' : node.name, node.x, node.y + 4);
            }
        }
    }

    _drawFireExitDoor(ctx, node, rx, ry, w, h) {
        ctx.save();
        ctx.fillStyle = '#f0fdf4';
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.roundRect(rx, ry, w, h, 6);
        ctx.fill();
        ctx.stroke();

        ctx.font = '16px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🚪🏃', node.x, node.y - 6);

        ctx.fillStyle = '#166534';
        ctx.font = 'bold 8px Inter, sans-serif';
        ctx.fillText('FIRE EXIT', node.x, node.y + 14);
        ctx.restore();
    }

    _drawVerticalTransportCore(ctx) {
        // Lifts in Royal Purple, Stairs in Golden Amber
        for (const [nodeId, node] of Object.entries(this.mapData.nodes)) {
            if (node.floor !== this.currentFloor) continue;
            if (node.type !== 'lift' && node.type !== 'stairs') continue;

            const w = node.w || 60;
            const h = node.h || 50;
            const rx = node.x - w / 2;
            const ry = node.y - h / 2;

            const isStart = (nodeId === this.startNodeId);
            const isDest = (nodeId === this.destNodeId);

            if (node.type === 'lift') {
                // LIFTS: ROYAL PURPLE
                let strokeColor = '#7c3aed';
                let fillColor = '#ede9fe';
                let borderWidth = 2.5;

                if (isStart) {
                    strokeColor = '#16a34a';
                    fillColor = '#dcfce7';
                    borderWidth = 3.5;
                } else if (isDest) {
                    strokeColor = '#dc2626';
                    fillColor = '#ffe4e6';
                    borderWidth = 3.5;
                }

                ctx.fillStyle = fillColor;
                ctx.strokeStyle = strokeColor;
                ctx.lineWidth = borderWidth;
                ctx.beginPath();
                ctx.roundRect(rx, ry, w, h, 6);
                ctx.fill();
                ctx.stroke();

                ctx.font = '16px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('🛗', node.x, node.y - 4);

                ctx.fillStyle = '#6d28d9';
                ctx.font = 'bold 8px Inter, sans-serif';
                ctx.fillText(node.room_code || 'LIFT', node.x, node.y + 14);

            } else if (node.type === 'stairs') {
                // STAIRS: GOLDEN AMBER
                let strokeColor = '#d97706';
                let fillColor = '#fef3c7';
                let borderWidth = 2.5;

                if (isStart) {
                    strokeColor = '#16a34a';
                    fillColor = '#dcfce7';
                    borderWidth = 3.5;
                } else if (isDest) {
                    strokeColor = '#dc2626';
                    fillColor = '#ffe4e6';
                    borderWidth = 3.5;
                }

                ctx.fillStyle = fillColor;
                ctx.strokeStyle = strokeColor;
                ctx.lineWidth = borderWidth;
                ctx.beginPath();
                ctx.roundRect(rx, ry, w, h, 6);
                ctx.fill();
                ctx.stroke();

                ctx.font = '16px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('🪜', node.x, node.y - 4);

                ctx.fillStyle = '#b45309';
                ctx.font = 'bold 8px Inter, sans-serif';
                ctx.fillText(node.room_code || 'STAIRS', node.x, node.y + 14);
            }
        }
    }

    _drawBlockedHazards(ctx) {
        for (const nodeId of this.blockedNodes) {
            const node = this.mapData.nodes[nodeId];
            if (!node || node.floor !== this.currentFloor) continue;

            const x = node.x;
            const y = node.y;
            const w = node.w || 60;
            const h = node.h || 50;

            ctx.save();
            ctx.fillStyle = 'rgba(239, 68, 68, 0.22)';
            ctx.strokeStyle = '#dc2626';
            ctx.lineWidth = 2.5;
            ctx.setLineDash([6, 6]);

            ctx.beginPath();
            ctx.roundRect(x - w/2 - 4, y - h/2 - 4, w + 8, h + 8, 8);
            ctx.fill();
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.fillStyle = '#dc2626';
            ctx.shadowColor = 'rgba(220, 38, 38, 0.4)';
            ctx.shadowBlur = 6;
            ctx.beginPath();
            ctx.roundRect(x - 45, y - 11, 90, 22, 11);
            ctx.fill();
            ctx.shadowBlur = 0;

            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 8.5px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('🚧 BLOCKED', x, y);
            ctx.restore();
        }
    }

    _drawShortestPath(ctx) {
        const route = this.currentRoute;
        if (!route || !route.path_details) return;

        const floorPath = [];
        for (let i = 0; i < route.path_details.length; i++) {
            const pt = route.path_details[i];
            if (pt.floor === this.currentFloor) {
                floorPath.push(pt);
            }
        }

        if (floorPath.length < 1) return;

        const isFire = Boolean(route.is_fire_evacuation);
        const auraColor = isFire ? 'rgba(234, 88, 12, 0.45)' : 'rgba(2, 132, 199, 0.35)';
        const solidColor = isFire ? '#ea580c' : '#0284c7';

        // Glowing Walking Corridor Line
        ctx.save();
        ctx.strokeStyle = auraColor;
        ctx.lineWidth = 14;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.beginPath();
        for (let i = 0; i < floorPath.length; i++) {
            const pt = floorPath[i];
            if (i === 0) ctx.moveTo(pt.x, pt.y);
            else ctx.lineTo(pt.x, pt.y);
        }
        ctx.stroke();

        ctx.strokeStyle = solidColor;
        ctx.lineWidth = 5;
        ctx.stroke();

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([8, 10]);
        ctx.lineDashOffset = -this.animOffset;
        ctx.stroke();
        ctx.setLineDash([]);

        this._drawDirectionalArrows(ctx, floorPath);
        ctx.restore();

        // Draw Intermediate Stops (For Multi-Stop Journey)
        for (let i = 0; i < floorPath.length; i++) {
            const pt = floorPath[i];
            if (pt.is_stop && pt.floor === this.currentFloor) {
                this._drawPin(ctx, pt.x, pt.y, '#eab308', `STOP ${pt.stop_number}`, '🛑');
            }
        }

        // Start Pin (Green)
        const first = route.path_details[0];
        if (first && first.floor === this.currentFloor) {
            this._drawPin(ctx, first.x, first.y, '#16a34a', 'START', '📍');
        }

        // Destination Pin (Red or Fire Exit Green)
        const last = route.path_details[route.path_details.length - 1];
        if (last && last.floor === this.currentFloor) {
            const destLabel = isFire ? 'SAFE FIRE EXIT' : 'DESTINATION';
            const destIcon = isFire ? '🚪' : '🏁';
            const destColor = isFire ? '#16a34a' : '#dc2626';
            this._drawPin(ctx, last.x, last.y, destColor, destLabel, destIcon);
        }

        // One-Tap Lift/Stairs Callout
        for (let i = 0; i < route.path_details.length - 1; i++) {
            const p1 = route.path_details[i];
            const p2 = route.path_details[i + 1];

            if (p1.floor === this.currentFloor && p2.floor !== this.currentFloor) {
                const via = p2.transition_via === 'stairs' ? '🪜 Stairs' : '🛗 Lift';
                const nextName = p2.floor === 0 ? 'Ground' : (p2.floor === 1 ? '1st Floor' : '2nd Floor');
                this._drawTransitionBadge(ctx, p1.x, p1.y - 32, `👉 TAP: Take ${via} to ${nextName}`);
            }
        }
    }

    _drawDirectionalArrows(ctx, path) {
        ctx.fillStyle = '#ffffff';
        for (let i = 0; i < path.length - 1; i++) {
            const p1 = path[i];
            const p2 = path[i + 1];
            const dist = Math.hypot(p2.x - p1.x, p2.y - p1.y);
            if (dist < 15) continue;

            const midX = (p1.x + p2.x) / 2;
            const midY = (p1.y + p2.y) / 2;
            const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);

            ctx.save();
            ctx.translate(midX, midY);
            ctx.rotate(angle);
            ctx.beginPath();
            ctx.moveTo(5, 0);
            ctx.lineTo(-4, -4);
            ctx.lineTo(-4, 4);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }
    }

    _drawTransitionBadge(ctx, x, y, text) {
        ctx.save();
        ctx.font = 'bold 10px Inter, sans-serif';
        ctx.textAlign = 'center';
        const w = ctx.measureText(text).width + 20;

        ctx.fillStyle = '#7c3aed';
        ctx.shadowColor = 'rgba(124, 58, 237, 0.5)';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.roundRect(x - w / 2, y - 12, w, 24, 12);
        ctx.fill();

        ctx.shadowBlur = 0;
        ctx.fillStyle = '#ffffff';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, x, y);
        ctx.restore();
    }

    _drawPin(ctx, x, y, color, title, emoji) {
        ctx.save();
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, 10, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(x, y, 4.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.font = 'bold 9.5px Inter, sans-serif';
        ctx.fillStyle = color;
        ctx.textAlign = 'center';
        ctx.fillText(`${emoji} ${title}`, x, y - 16);
        ctx.restore();
    }

    _drawHighlightNode(ctx, nodeId) {
        const node = this.mapData.nodes[nodeId];
        if (!node || node.floor !== this.currentFloor) return;

        ctx.save();
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(node.x, node.y, 22, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }
}

window.HospitalMapRenderer = HospitalMapRenderer;
