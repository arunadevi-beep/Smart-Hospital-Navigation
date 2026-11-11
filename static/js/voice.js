/**
 * Voice Navigation Guidance Module
 * Uses Web Speech API to provide hands-free audio directions in English & Tamil.
 */
class VoiceGuidance {
    constructor() {
        this.synth = window.speechSynthesis;
        this.currentLang = 'en-US';
        this.isSpeakingNow = false;
        this.stepQueue = [];
        this.currentStepIndex = 0;
        this.onStepChange = null;
        this.onFinish = null;
    }

    setLanguage(langCode) {
        this.currentLang = langCode;
    }

    speakDirections(instructions, langCode = 'en-US') {
        if (!this.synth) {
            console.warn('Web Speech API is not supported in this browser.');
            return;
        }

        this.stop();
        this.currentLang = langCode;
        this.stepQueue = instructions;
        this.currentStepIndex = 0;
        this.isSpeakingNow = true;

        this._playNextStep();
    }

    _playNextStep() {
        if (this.currentStepIndex >= this.stepQueue.length) {
            this.isSpeakingNow = false;
            if (this.onFinish) this.onFinish();
            return;
        }

        const step = this.stepQueue[this.currentStepIndex];
        if (this.onStepChange) {
            this.onStepChange(step, this.currentStepIndex);
        }

        const utterance = new SpeechSynthesisUtterance(step.text);
        utterance.lang = this.currentLang;
        utterance.rate = 0.95; // Slightly slower for clarity
        utterance.pitch = 1.0;

        // Try to match appropriate voice
        const voices = this.synth.getVoices();
        if (this.currentLang.startsWith('ta')) {
            const tamilVoice = voices.find(v => v.lang.includes('ta') || v.lang.includes('ta-IN'));
            if (tamilVoice) utterance.voice = tamilVoice;
        } else {
            const enVoice = voices.find(v => (v.lang === 'en-IN' || v.lang === 'en-US') && !v.name.includes('David'));
            if (enVoice) utterance.voice = enVoice;
        }

        utterance.onend = () => {
            this.currentStepIndex++;
            // Brief 400ms pause between instructions
            setTimeout(() => {
                if (this.isSpeakingNow) {
                    this._playNextStep();
                }
            }, 400);
        };

        utterance.onerror = () => {
            this.currentStepIndex++;
            this._playNextStep();
        };

        this.synth.speak(utterance);
    }

    speakText(text, langCode = 'en-US') {
        if (!this.synth) return;
        this.stop();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = langCode || this.currentLang;
        utterance.rate = 1.0;
        this.synth.speak(utterance);
    }

    stop() {
        this.isSpeakingNow = false;
        this.stepQueue = [];
        this.currentStepIndex = 0;
        if (this.synth) {
            this.synth.cancel();
        }
    }
}

window.VoiceGuidance = VoiceGuidance;

