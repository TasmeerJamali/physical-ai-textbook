---
type: implement
mode: frontend
---

# Feature: Voice Interaction for Chat Widget

## Context
The project aims to be a "Physical AI & Humanoid Robotics" textbook. To align with the "Humanoid" theme and "VLA Models" (Vision-Language-Action) curriculum, the Chat Widget should support natural voice interaction.

## Requirements
1.  **Voice Input**: Add a microphone button to the Chat Widget input area.
    *   Use the browser's `SpeechRecognition` API.
    *   Transcribe speech to text and populate the input field.
    *   Auto-send the message after a pause or stop.
2.  **Voice Output**: Add a speaker button to AI responses.
    *   Use the browser's `SpeechSynthesis` API.
    *   Read the AI's answer aloud when clicked.
3.  **Visual Feedback**:
    *   Show a "Listening..." state or animation when the microphone is active.
    *   Show a "Speaking" state when reading aloud.

## Technical Constraints
- Must work in modern browsers (Chrome/Edge).
- No external API keys for speech (use Web APIs to keep it lightweight).
- Must integrate with the existing `ChatWidget` component.

## Goal
Enhance the user experience by allowing "hands-free" or "conversational" interaction with the AI tutor, mimicking a humanoid robot interface.
