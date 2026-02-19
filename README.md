🍵 Matcha Journal
A web application for matcha enthusiasts to track, rate, and discover teas. This project uses a decoupled architecture, separating a high-performance Python backend from a modern, responsive React frontend.

🛠 The Tech Stack
Backend (The "Brain")
Framework: FastAPI

ORM: SQLAlchemy (Handles complex relational logic)

Validation: Pydantic (The "sieve" for data integrity)

Frontend (The "Face")
Library: React.js (Component-based UI)

Styling: Tailwind CSS (Utility-first CSS for a clean, "zen" aesthetic)

State Management: Axios (For talking to the FastAPI backend)

🏗 System Architecture
The app follows a strict Client-Server model:

The Database (Relational): Brands and Entries are normalized. We use joinedload in the backend so the frontend gets a clean, nested JSON object in a single request.

The API (RESTful): FastAPI serves JSON over HTTP. It acts as a secure gatekeeper.

The Frontend (Reactive): React fetches the data and maps it into beautiful, reusable components (e.g., a MatchaCard component).

🎨 Frontend Features
Responsive Journal: A grid of your tried matchas that looks great on mobile or desktop.

Dynamic Forms: Add new entries and select from a pre-populated list of brands fetched from the API.

Tailwind Design: A "Matcha-inspired" color palette using emerald and slate tones for a calm user experience.

Real-time Feedback: Instantly update the UI when a new tea is added without a full page refresh.

🚀 Getting Started
Backend Setup
Bash

# Install dependencies
pip install fastapi sqlalchemy pydantic uvicorn

# Start the API
uvicorn app.main:app --reload
Frontend Setup
Bash

# Move to frontend directory
cd frontend

# Install packages
npm install

# Start the dev server
npm start
🚦 Core API Flow
React sends a GET request to /entries/.

FastAPI uses SQLAlchemy to perform a JOIN on the brands and matcha_entries tables.

SQLAlchemy returns a Python object; Pydantic serializes it into JSON.

React receives the JSON and updates the state, triggering a re-render of the tea cards.