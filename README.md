# Task Management Application

## Overview

This project implements a full-stack task management system with a backend API (FastAPI, async SQLAlchemy) and an Angular frontend. The focus is on:

- Asynchronous notifications to avoid blocking the backend main thread on task updates.
- Efficient RxJS usage in Angular for reactive data fetching, merging, and filtering.

---

## Features

### Backend

- CRUD operations for Users and Tasks.
- Asynchronous task update notifications using background tasks or websockets.
- Database initialization with random seed data for validation.
- Designed with SQLAlchemy ORM and Pydantic schemas for data validation.

### Frontend (Angular)

- Display and manage tasks grouped by status.
- Reactive task loading on user selection changes.
- RxJS observables merge user tasks with external or local data, then filter for display.
- Snackbar notifies users asynchronously on task updates.
- Uses Angular Signals and reactive patterns for efficient state management.

---

## Architecture and Design Choices

- **FastAPI with Async SQLAlchemy** enables non-blocking database operations and background task execution.
- Notifications are handled asynchronously via WebSocket connections to prevent main thread blocking.
- Angular RxJS integration merges multiple data streams, applying filtering to optimize performance and UX responsiveness.
- Angular Signals replace imperative lifecycle hooks for reactive, declarative state handling.
- Data seeding on startup facilitates easy testing and validation of async flows and RxJS data processing.

---

## Verification

- Backend logs and database show asynchronous notification handling without blocking requests.
- Angular UI dynamically updates tasks upon notifications without manual refresh.
- RxJS streams tested with merged data sources and filtering; results displayed in the task list.
- Random initial data ensures all flows can be exercised without additional setup.

---

## Code Quality

- Separation of concerns in backend and frontend layers.
- Usage of modern async/await syntax and reactive programming paradigms.
- Pydantic validation ensures data integrity and clear API contracts.
- Angular modular components and services maintain readability and scalability.

---

## Usage

- Run backend server (FastAPI).
- Angular frontend connects to backend APIs and WebSocket notifications.
- Select users to load tasks reactively.
- Update tasks to trigger async notifications.
- Observe filtered task data merged from multiple RxJS streams in UI.

---
