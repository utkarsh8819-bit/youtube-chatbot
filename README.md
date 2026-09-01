# 🎥 YouTube AI Chatbot

An AI-powered chatbot that lets users ask questions about YouTube videos using **Retrieval-Augmented Generation (RAG)**.

The application extracts the video's transcript, splits it into meaningful chunks, converts the chunks into multilingual embeddings, retrieves the most relevant information using FAISS, and uses Google Gemini to generate grounded answers in English.

---

## 🚀 Live Demo

**Coming soon...**

The application will be deployed using Streamlit Community Cloud.

---

## ✨ Features

- 🎥 Process any YouTube video with an available transcript
- 📝 Automatically extract the YouTube transcript
- ✂️ Split transcripts into smaller text chunks
- 🧠 Generate multilingual sentence embeddings
- 🔎 Retrieve relevant transcript sections using FAISS
- 🤖 Generate answers using Google Gemini
- 💬 Ask multiple questions about the same video
- 🧠 Maintain conversation context during the session
- 🌍 Support Hindi and English transcripts
- 🇬🇧 Generate answers in English
- ⏱️ Display source timestamps for retrieved information
- ▶️ Watch the processed YouTube video inside the application
- 🌐 Interactive Streamlit web interface

---

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation pipeline:

```text
YouTube URL
     │
     ▼
YouTube Transcript
     │
     ▼
Text Chunking
     │
     ▼
Multilingual Embeddings
     │
     ▼
FAISS Vector Store
     │
     ▼
User Question
     │
     ▼
Similarity Search
     │
     ▼
Relevant Transcript Chunks
     │
     ▼
Google Gemini
     │
     ▼
English Answer + Sources
