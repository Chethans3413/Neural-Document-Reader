# 🧠 Neural Reader | Local AI Document Agent

Neural Reader is a fully private, locally-hosted Document AI Agent that allows you to upload PDF documents and ask questions about them. It leverages state-of-the-art Local LLMs to read, embed, index, and infer answers based strictly on the uploaded document's context, ensuring complete horizontal data privacy without relying on cloud APIs.

---

## ✨ Features

- **100% Local Processing:** Uses locally running Ollama instances, meaning your documents never leave your machine. No API keys or cloud subscriptions needed.
- **Advanced RAG Pipeline:**
  - **Text Extraction:** Robust local PDF parsing using LangChain's `PDFLoader`.
  - **Chunking:** Intelligent recursive character splitting to break down large documents.
  - **Embeddings:** Fast local vectorization using `nomic-embed-text` via Ollama.
  - **Vector Storage:** Instant, persistence-aware In-Memory Vector Store.
  - **Inference:** Powered by the Mistral 7B LLM (via Ollama) for accurate context-aware responses.
- **Stunning UI/UX Redesign:**
  - Completely custom **Glassmorphism** dark theme architecture.
  - Advanced CSS Keyframe ambient animations (pulsing neon blobs).
  - High-performance Framer Motion physics-based interactions and staggered UI mounting.
  - Premium custom typography and glowing gradients throughout the UI.
  - Custom fluid file Dropzone.

---

## 🏗️ Technical Architecture

### Tech Stack
* **Framework:** Next.js (App Router, React 18, Server Components API Routes)
* **Styling:** Tailwind CSS, Custom CSS Variables, generic utility classes.
* **Animations:** Framer Motion, CSS `@keyframes`.
* **Icons:** Lucide React.
* **AI Tooling:** LangChain.js (`@langchain/community`, `@langchain/core`, `@langchain/collama`).
* **Local LLM Engine:** Ollama (`mistral` for inference, `nomic-embed-text` for embeddings).
* **Document Parsing:** `pdf-parse`.

### Data Flow (The RAG Pipeline)
1. **Upload (`/api/upload`)**: A user uploads a PDF. The Next.js API route reads the file into a Node buffer.
2. **Extraction**: LangChain's `PDFLoader` combined with `pdf-parse` extracts the raw text.
3. **Chunking**: The text is split into overlapping chunks to preserve context borders.
4. **Embedding**: `OllamaEmbeddings` converts each chunk into a high-dimensional vector space using `nomic-embed-text`.
5. **Storage**: Vectors and metadata are stored in a custom Node-based In-Memory Vector Store that intentionally survives Next.js HMR (Hot Module Replacement) during development using `globalThis`.
6. **Inference (`/api/chat`)**: The user asks a question. The query is embedded, and a cosine similarity search retrieves the top matching chunks. The Mistral LLM is prompted with the question and the context to formulate a response.

---

## 🔬 AI Methodologies & Models

Neural Reader relies on several advanced artificial intelligence methodologies to process context accurately and safely.

### 1. RAG (Retrieval-Augmented Generation)
Large Language Models (LLMs) are frozen in time and do not inherently know the contents of your personal documents. **RAG** solves this pipeline by injecting your document data directly into the LLM's prompt context during inferencing.
- Instead of fine-tuning an entire model (expensive and slow), Neural Reader parses the PDF and creates an indexed, searchable "memory database" of paragraphs.
- When you ask a question, the application searches this database for the **most relevant** paragraphs matching your question, and feeds only those paragraphs to the LLM alongside your prompt.
- **Why it matters:** This drastically reduces hallucinations (AI making things up) and grounds the LLM strictly to the facts inside your uploaded document.

### 2. The LLM: Mistral 7B
The application uses **Mistral 7B** (via Ollama) as the core cognitive engine for natural language generation.
- Mistral 7B is an open-weights model created by Mistral AI, highly regarded for its phenomenal performance-to-size ratio.
- It is specifically adept at *instruction following* and *summarization*, making it the perfect candidate to read the dense technical context retrieved by the RAG pipeline and formulate a human-readable, conversational answer.
- **Local Advantage:** By running Mistral locally via Ollama, Neural Reader ensures 100% data privacy. The document context never touches OpenAI, Anthropic, or any other cloud provider's servers.

### 3. The Embedding Model: `nomic-embed-text`
Before text can be searched mathematically, paragraphs must be converted into numerical vectors (lists of floats representing semantic meaning).
- Neural Reader uses **Nomic Embed Text**, a highly optimized, open-source embedding model specifically fine-tuned for dense retrieval tasks.
- With an embedding dimension of `768`, it allows the custom Vector Store to perform lightning-fast **Cosine Similarity** mathematics to determine exactly which paragraphs of your 50-page PDF are relevant to your specific question, within milliseconds.

### 4. Custom In-Memory Vector Store (RAG Storage)
While many RAG pipelines rely on heavy, external cloud databases, Neural Reader has been engineered to be as lightweight and local as possible. 
- It implements a custom, highly efficient **In-Memory Vector Store** directly within the Next.js API Node environment.
- The vectors are kept alive across Next.js Hot Module reloads using `globalThis`, ensuring that during development or localized usage, you aren't constantly re-uploading the same PDF and waiting for extraction.

### 5. LangChain Integration & PDF Parsing
Neural Reader extensively utilizes **LangChain.js** to orchestrate the RAG pipeline.
- **`PDFLoader` + `pdf-parse`:** The Next.js `/api/upload` route uses LangChain's `PDFLoader` combined with `pdf-parse@1.1.1` to reliably extract text content from raw PDF Buffers uploaded by the client.
- **`RecursiveCharacterTextSplitter`**: Extracts are intelligently chunked into segments (e.g., 1000 characters with 200 character overlap) to ensure that sentences or paragraphs are not cut off abruptly, preserving the semantic context required by the embedding model.
- **LCEL (LangChain Expression Language)**: The inference endpoint (`/api/chat`) uses `RunnableSequence` to pipe the retrieved context and the user query directly into a specialized prompt template, which is then streamed to the Ollama LLM execution chain.

### 6. Prompt Engineering
To ensure Mistral 7B pays attention exclusively to the uploaded document, the application employs strict system-level prompt engineering. The LLM is forced to adopt a persona that uses *only* the provided context chunks.
- The prompt is structured using exact instruction identifiers (`Instruct:` and `Output:`) which aligns perfectly with how the Mistral/Phi family of models were trained, minimizing reasoning errors and preventing the LLM from answering outside the bounds of the provided data.

### 7. Full-Stack Architecture (Next.js API Routes)
The frontend and backend are tightly integrated within the **Next.js App Router**:
- **Client Components (`page.tsx`)**: Handles the beautiful Drag-and-Drop UI, file state management, and real-time Chat interactions using React hooks and Framer Motion.
- **Server Routes (`/api/upload`, `/api/chat`)**: Act as secure intermediaries, receiving the heavy PDF buffers, communicating mathematically with the local Ollama instance running on port `11434`, and managing the node-based In-Memory Vector Store.

### 8. Future Scalability (ChromaDB & Streamlit)
While the current version of Neural Reader is a full-stack Next.js application tailored for modern web browsers and an In-Memory vector store, the architecture is designed to be easily decoupled:
- **ChromaDB Integration:** If persistence across server restarts or handling massive document corpora (thousands of PDFs) is required, the `RAG Storage` local memory vector layer can be easily swapped out for **ChromaDB**, an open-source vector database built specifically for AI workloads.
- **Streamlit Portability:** The core data extraction, chunking, and context logic (`RAG Pipeline`) operates independently of the frontend. If a Python-centric data science UI is preferred over Next.js, the backend logic is 100% portable to a **Streamlit** dashboard, retaining the exact same local privacy guarantees.

---

## 🚀 Getting Started

### 1. Prerequisites
You must have [Ollama](https://ollama.ai/) installed and running locally on your machine.

### 2. Download the Models
Before starting the app, you need to pull the required local models. Open your terminal and run:

```bash
ollama run mistral
ollama pull nomic-embed-text
```
*(The Mistral model is roughly 4.1GB, so this may take a moment depending on your internet connection).*

### 3. Install Dependencies
Navigate to the root directory (`ai-doc-reader`) and run:
```bash
npm install
```

### 4. Run the Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

---

## 🎨 UI/UX Design Philosophy

The redesign of Neural Reader was focused on providing a "Wow" factor right out of the box, leaning into a futuristic, premium "Neural AI" aesthetic. 

- **Ambient Backgrounds:** Instead of flat colors, the background consists of massive glowing Cyan and Violet spheres that continuously shift, pulse, and morph behind a translucent dotted mesh screen.
- **Glassmorphism:** All core modular panels (the Upload Sidebar and the Main Chat Thread) utilize stacked translucent blurs (`backdrop-blur-2xl`) with highly subtle white borders, to create the illusion of etched floating glass over the ambient neon background.
- **Micro-Interactions:** The Upload Dropzone features a Framer Motion spring-physics scaling mechanism, making the target feel physical and responsive to drag-and-drop operations.
- **Typographic Polish:** System fonts were removed in favor of strict tracking, gradient-masked dynamic colors, and text-glows. Let the data shine.

Enjoy local, private document analysis!
