# AI-Powered Multilingual Sign Language Translator (Prototype)

## Overview
This repository contains a **browser‑based prototype** that demonstrates real‑time translation between Indian Sign Language (ISL) gestures and text/voice, and vice‑versa. It showcases two independent pipelines:
- **Sign → Text & Voice** – webcam → hand detection → remote AI model → stabilized word → sentence → optional speech synthesis.
- **Text/Voice → Sign** – user‑typed or spoken sentence → word mapping → 3‑D cartoon avatar.

The system is **educational**; it is not a production‑grade sign‑language recognizer. The AI model is a Keras model that accepts **128×128 RGB images** and outputs a probability vector over **26 classes** (the alphabet letters A‑Z). The confidence value returned by the model (0‑1) is a *score* and **does not represent real‑world accuracy**. Formal accuracy testing has not been performed.

## Features
- Home, Sign‑to‑Text, Text‑to‑Sign, About pages (English & Tamil UI).
- **Modern 3D Cartoon Human Avatars**:
  - Two switchable characters: **Arjun** (Male) and **Priya** (Female) with matching proportions and visual style.
  - Fully rigged upper body: shoulders, elbows, 3-axis wrists, and articulated 5-finger joints (thumb, index, middle, ring, pinky).
  - Expressive cartoon faces with mobile eyebrows, mouth morphs, and natural periodic eye-blinking.
  - Character switching preserves user text input and sentence progress without interruption.
  - Fullscreen avatar viewport, speed control (0.5×–1.5×), Play/Pause, Replay Current Sign, and Replay Sentence.
  - ISL Sign Information card showing linguistic descriptions, hand configurations, orientations, and ISLRTC reference sources.
- Camera start/stop, live landmark overlay, detected word, confidence indicator, recognition status.
- Stabilizer with jitter tolerance, duplicate suppression, and intentional release detection for repeated letters.
- Heuristic fallback classifier (used when the backend is unavailable).
- Text‑to‑speech (English/Tamil) via the Web Speech API; voice input for Text‑to‑Sign.
- Personalization stored in `localStorage` (clearable).
- Demo mode with button‑driven word entry (useful when the camera or backend is not available).
- Dynamic status banner that reports backend health (`checking`, `available`, `fallback`, `error`) in both languages.

## Technologies
- **Frontend**: React 19, Vite, React Router (HashRouter), MediaPipe Tasks Vision, Three.js, vanilla CSS.
- **Backend**: Python 3.11, TensorFlow 2.19 (no external web framework). Uses the standard library `http.server`.
- **Model**: Keras `.keras` model trained to classify 128×128 RGB images into 26 letters.
- **Internationalisation**: Simple i18n implementation in `src/i18n.jsx`.

## Repository Structure
```
isl-translator/          (project root)
├─ ai/                  # Model files
│   ├─ models/          # isl_alphabet.keras & .h5
│   └─ class_names.txt
├─ backend/             # Python HTTP server
│   └─ server.py        # loads the Keras model, /health and /predict endpoints
├─ public/              # static assets, MediaPipe wasm copied on install/build
├─ src/                 # React source
│   ├─ components/      # UI components (CameraView, DetectionPanel, …)
│   ├─ hooks/           # useSignRecognition hook (camera loop, backend calls)
│   ├─ services/        # signRecognitionService, remoteRecognitionService, …
│   ├─ data/            # signWords, gestureMap, signMappings
│   ├─ i18n.jsx         # English/Tamil strings
│   └─ pages/           # Home, SignToText, TextToSign, About
├─ scripts/             # copy‑wasm.mjs (runs on npm install/build)
├─ vite.config.js       # Vite dev server with `/api` proxy to localhost:8000
├─ package.json
└─ README.md            # this file
```

## Prerequisites (Windows)
1. **Git** – to clone the repository.
2. **Node.js 20+** – for the frontend (`npm` commands).
3. **Python 3.11** – for the backend. Use the bundled virtual environment `convert-env2` (already contains TensorFlow 2.19).
4. **Camera** – a webcam accessible by the browser.
5. **Internet** – required for the first load of the MediaPipe hand model and optional voice synthesis.

## Setup & Running the Project
Open **two separate terminal windows** (or VS Code terminals).

### 1. Backend (Python)
```bat
cd d:\DOWNLOADS\MINI PROJECT\isl-sign-translator\isl-translator\convert-env2\Scripts
activate               # activates the virtual environment
python ..\..\backend\server.py   # runs on http://127.0.0.1:8000
```
The server prints a line like `Serving HTTP on 127.0.0.1 port 8000 …`. It exposes:
- `GET /health` – JSON `{status: 'ok', model: 'isl_alphabet', input_shape: [128,128,3], output_classes: 26}`
- `POST /predict` – expects `{"image": "data:image/jpeg;base64,…"}` and returns `{"word": "A", "confidence": 0.87}`.

### 2. Frontend (React/Vite)
```bat
cd d:\DOWNLOADS\MINI PROJECT\isl-sign-translator\isl-translator
npm install            # one‑time, installs node_modules
npm run dev            # starts Vite dev server on http://localhost:5173
```
The Vite config proxies `/api/*` to the backend (`http://127.0.0.1:8000`).

### 3. Verify Backend Health
Open a browser tab and navigate to:
- Direct: `http://127.0.0.1:8000/health`
- Via Vite proxy: `http://localhost:5173/api/health`
Both should return a JSON payload with `status: "ok"`. The UI status banner will show **"AI model online – using remote predictions"** (English) or the Tamil equivalent.

## Troubleshooting Common Issues
| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **Camera permission denied** | Browser blocked webcam access. | Click the address‑bar lock icon, allow camera, or restart the page. The UI will show a localized error message. |
| **Port 8000 already in use** | Another process (e.g., previous backend) is listening. | Stop the existing process (`Ctrl+C` in its terminal) or change the port in `backend/server.py` and the proxy target in `vite.config.js`. |
| **Backend unreachable / status remains *checking*** | Backend not running or blocked by firewall. | Ensure `python backend/server.py` is running, no firewall rule blocks `127.0.0.1:8000`. Check the console logs for errors. |
| **Health‑check timeout** | Backend responded slower than 5 s (network hiccup). | The UI will fall back to heuristic classifier and display *Remote backend unavailable – using heuristic classifier*. Restart the backend and reload the page. |
| **Malformed prediction response** | Backend crashed or returned non‑JSON. | The frontend logs a warning and ignores the response; the status banner switches to fallback. Review `backend/server.py` logs (`.system_generated/tasks/task-322.log`). |
| **No hand detected** | Hand not in view or lighting poor. | Adjust lighting, keep hand within webcam frame, and wait for the MediaPipe overlay to appear. |
| **Confidence values out of range** | Unexpected backend data. | The frontend validates that confidence is a finite number between 0 and 1; out‑of‑range values are ignored. |

## Limitations
- **Vocabulary** limited to 26 letters (A‑Z) – the model does not understand full words or sentences.
- The confidence number is a **score** from the softmax layer; it is **not** a guarantee of correctness.
- No formal accuracy testing has been performed; real‑world performance may vary.
- Avatar animations are placeholders and not linguistically verified.
- Tamil output is a word‑by‑word gloss; grammar is not adjusted.
- The backend runs only on a local machine (no cloud deployment). 

## Future Enhancements (Roadmap)
- Train a dedicated ISL‑word model (image‑based) and replace the placeholder recognizer.
- Expand vocabulary and add fingerspelling for names.
- Support two‑hand gestures and facial expressions.
- Integrate a real 3‑D avatar with linguist‑validated animations.
- Offline PWA capability and optional on‑device inference (e.g., TensorFlow.js).
- More robust error handling and automated health‑monitoring.

---
*The implementation described here has been verified on Windows 10 with Node 20, Python 3.11, and Chrome 118. The documentation reflects the current state of the repository; no additional packages were installed or model files altered.*

A browser-based **prototype** for **Indian Sign Language (ISL) word-based translation** (not alphabet recognition), in two independent directions:

- **Sign → Text & Voice:** webcam → hand detection → recognized word → continuous sentence → correction → text + speech
- **Text/Voice → Sign:** text or microphone → word mapping → cartoon 3D avatar sign sequence

> **Prototype / Limited Vocabulary.** This is an academic prototype with a limited ISL vocabulary. Recognition accuracy depends on the trained model, lighting, camera quality, hand position, and gesture variation.

## Features
- Home, Sign → Text & Voice, Text/Voice → Sign, and About / How It Works pages (English and Tamil UI)
- Camera start/stop, live landmark overlay, detected word, confidence indicator, recognition status
- Continuous sentence building with **stability hold (700 ms)** and **cooldown (1.2 s)**, and no repeats while a gesture is held
- Local correction (`I NEED HEL` → `I NEED HELP`), Accept / Edit / Reset
- Text-to-speech (English and Tamil buttons) and voice input via the Web Speech API
- Three.js cartoon avatar with play / pause / replay / speed, and one prototype animation per word
- Privacy-friendly personalization in `localStorage` (**stored locally, never uploaded**) with a Clear button
- **Prototype Demo Mode** (button-driven word entry, clearly labelled, not fake AI)
- Friendly errors: camera denied/missing, model load failure, mic denied, unsupported speech, no hand, unknown sign, empty text, unsupported words

## Technologies
React 19, Vite, React Router (HashRouter), MediaPipe Tasks Vision (HandLandmarker), Three.js, Web Speech API, localStorage. Plain CSS. No backend, no paid APIs.

## Folder structure
```
src/
  components/  Navbar, Footer, CameraView, DetectionPanel, SentenceBox, CorrectionSuggestion,
               LanguageSelector, VoiceButton, AvatarViewer, SignSequence
  pages/       Home, SignToText, TextToSign, About
  services/    signRecognitionService, correctionService, speechService,
               personalizationService, signMappingService
  hooks/       useSignRecognition (camera + recognition loop + cleanup)
  avatar/      createAvatar (Three.js rig and animation player)
  data/        signWords, gestureMap, signMappings
  i18n.jsx     English/Tamil strings
scripts/copy-wasm.mjs   copies the MediaPipe WASM into public/ (runs on install/build)
```

## Install and run
```bash
npm install
npm run dev        # open the printed http://localhost:5173
npm run build      # production build in dist/
```

## Browser requirements
Recent **Chrome or Edge** recommended (best Web Speech support). Camera needs `localhost` or HTTPS. Voice input needs an internet connection in Chrome. Tamil speech needs a Tamil voice installed in your OS. The hand model file (~7 MB) is downloaded once from Google's CDN, so the first camera start needs internet.
For fully offline use, download `hand_landmarker.task` into `public/models/` and change `MODEL_URL` in `signRecognitionService.js` to `` `${import.meta.env.BASE_URL}models/hand_landmarker.task` ``.

## Demo Mode
Tick **Demo Mode** on the Sign → Text page. Buttons for each supported word appear; pressing one feeds the same sentence/correction/speech pipeline. It is labelled *Prototype Demo Mode* and does not claim recognition. Use it when the camera or model is unavailable.

The built-in camera recognizer maps five-finger patterns (thumb/index/middle/ring/pinky extended or curled) to words, see `src/data/gestureMap.js`. These are demo hand shapes, **not real ISL signs**.

## Add a new sign word
1. `src/data/signWords.js`: add `{ id: 'HOME', ta: 'வீடு', aliases: {...} }`
2. `src/data/gestureMap.js`: add an unused finger pattern (only needed for the built-in recognizer)
3. `src/data/signMappings.js`: add `HOME: 'home'` to `SIGN_ANIMATION_MAP` and keyframes to `ANIMATIONS.home`
4. Optional: add the word to `EXTRA`/phrases in `correctionService.js`

## Replace the prototype recognizer with a trained ISL model
All recognition goes through `src/services/signRecognitionService.js`. The simplest swap:
```js
import { setRecognitionModel } from './services/signRecognitionService';
setRecognitionModel((landmarks) => {          // 21 MediaPipe landmarks {x,y,z}
  // run your TensorFlow.js / ONNX model here
  return { word: 'HELLO', confidence: 0.93 }; // or null when unsure
});
```
Keep the same `{ word, confidence }` shape and everything else (stabilizer, sentence, correction, speech) keeps working. For sequence models, buffer landmarks over several frames inside your function. Word labels must match ids in `signWords.js`. Then hide the demo gesture list on the page if you want.

## Replace or add avatar animations
`src/data/signMappings.js` maps `WORD → animation name → keyframes` (`HELLO → hello`). Edit the numbers to tune gestures. To use a real rigged GLTF avatar, reimplement `createAvatar()` in `src/avatar/createAvatar.js` and keep its API (`play(word)`, `rest()`, `setSpeed()`, `dispose()`); no component changes are needed.

## Replace the correction layer with an LLM
`suggest(sentence)` in `correctionService.js` is the single entry point returning `{ text, reason }`. Swap its body (or wrap it) with an API call.

## Limitations
- 16-word vocabulary. Names (e.g. RAHUL) are not recognized; add them with **Edit**.
- Demo gestures and avatar animations are placeholders, not linguistically verified ISL.
- Single hand, word-level only. No facial expression or two-hand dynamic signs.
- Tamil output is word-by-word (no grammar reordering).
- The confidence value is a heuristic score, not model accuracy.

## Future enhancements
Train an ISL word model on a dataset such as INCLUDE, a real rigged avatar with linguist-verified animations, two-hand and motion-sequence recognition, fingerspelling for names, an LLM corrector, offline PWA, more Indian languages.
