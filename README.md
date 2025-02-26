# Geospatial AI Assisted Information Gathering Tool

This project is a web application with a split-screen interface that features:
- **Left Side:** An AI chat interface with a dropdown to choose among different AI models.
- **Right Side:** A map view rendered using Leaflet with basic interactions (location search, zooming, and switching between map providers).

The goal of this project is to provide a robust and modular platform that leverages geospatial data and AI to help users gather and analyze information interactively. Future iterations will incorporate more advanced AI agents, enhanced map interactions, and deeper data analytics capabilities.


![Image](./geospatical_ai.gif)


---

## Project Structure

```
geospatial-ai-app/
.
├── backend
│   ├── agents              # Directory for AI agent integrations
│   ├── app.py              # Main entry point for the backend server
│   ├── config              # Configuration files and environment settings
│   ├── ~flask_session~     # Session management (if using Flask)
│   ├── __pycache__         # Compiled Python files
│   ├── requirements.txt    # Python dependencies
│   ├── routes              # API route definitions
│   ├── services            # Business logic and service layers
│   ├── utils               # Utility functions and helpers
│   └── venv                # Python virtual environment
├── frontend
│   ├── node_modules        # Node.js dependencies
│   ├── package.json        # Frontend package configuration
│   ├── package-lock.json   # Dependency lock file
│   ├── public              # Static files and index.html
│   ├── README.md           # Frontend specific documentation
│   └── src                 # Source code for React components and styles
├── node_modules            # Root-level Node.js dependencies (if applicable)
├── package.json            # Root-level package configuration (if applicable)
├── package-lock.json       # Root-level dependency lock file (if applicable)
└── README.md               # This file
```

---

## Setup Instructions

### Backend
1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start the server:**
   ```bash
   python3 app.py
   ```

### Frontend
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
   **Once you are done, you will something like below, depending on your python version, the warnings might be different.**  
   ```bash
    /geospatial-app/backend/venv/lib/python3.11/site-packages/flask_limiter/extension.py:333: UserWarning: Using the in-memory storage for tracking rate limits as no storage was explicitly specified. This is not recommended for production use. See: https://flask-limiter.readthedocs.io#configuring-a-storage-backend for documentation about configuring the storage backend.
    warnings.warn(
    * Serving Flask app 'app'
    * Debug mode: on
    INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://10.0.5.226:5000
    INFO:werkzeug:Press CTRL+C to quit


   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
   
3. **Start the development server:**
   ```bash
   npm start
   ```
   **Once you are done for the frontend, you will see this in your terminal:**  
   ```bash

    Compiled successfully!
    You can now view frontend in the browser.

    Local:            http://localhost:3000
    On Your Network:  http://10.0.5.226:3000

    Note that the development build is not optimized.
    To create a production build, use npm run build.
    webpack compiled successfully
    ```

---

## Future Enhancements

- **Map Interactions:**  
  - Allow users to select portions of the map to query.
  - Export map images along with conversation summaries.
  - Integrate additional map layers and visualization options.

- **AI Agents:**  
  - Connect to multiple AI models and agents for advanced data analysis.
  - Enable object-centric summarization and climate change queries.
  - Support dynamic data filtering and interactive data visualizations.

- **Data Analysis:**  
  - Implement statistical analysis and real-time data updates.
  - Provide tools for advanced geospatial data processing.

- **Collaboration & Integration:**  
  - Expand modularity for easy integration of third-party APIs.
  - Enable user authentication and session management.
  - Implement role-based access for collaboration features.

---

## TODO

- [⏳] **Map Enhancements:**  
  - Add functionality for area selection and region-specific queries.
  - Implement multiple map provider integrations (e.g., Google Maps, Mapbox).

- [⏳] **AI Chat Enhancements:**  
  - Integrate function calling for more complex AI interactions.
  - Add support for contextual conversation history and dynamic agent switching.

- [❌] **Backend Improvements:**  
  - Expand API endpoints to support new functionalities.
  - Enhance error handling and logging mechanisms.

- [⏳] **User Experience:**  
  - Improve responsive design for various screen sizes.
  - Add comprehensive testing for both frontend and backend components.

- [❌] **Documentation:**  
  - Update inline documentation and code comments.

*and much more features to add*

---

## Collaboration

We welcome contributions and collaboration! If you’d like to help improve this project, please follow these guidelines:

- **Reporting Issues:**  
  - Use the [GitHub Issues](https://github.com/your-repo/geospatial-ai-app/issues) page to report bugs or request new features.
  
- **Pull Requests:**  
  - Fork the repository and create your feature branch (`git checkout -b feature/YourFeature`).
  - Commit your changes with clear, descriptive messages.
  - Push to your branch and open a pull request against the `main` branch.
  
- **Coding Standards:**  
  - Ensure your code follows the existing style and structure.
  - Include tests where applicable.
  - Write clear documentation for any new features or changes.

- **Discussion:**  
  - Join our community discussions on [Discord/Slack/Forum link] to share ideas and get support from other contributors.

---

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

Please make sure to update tests as appropriate.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgements

- [Leaflet](https://leafletjs.com/) for the excellent mapping library.
- [FastAPI](https://fastapi.tiangolo.com/) for the lightweight and powerful backend framework.
- [React](https://reactjs.org/) for building the dynamic frontend.
- Community contributors and all the open source projects that make this work possible.
