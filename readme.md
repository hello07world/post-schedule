# Post Schedule

Post Schedule is a Django-based social post scheduling application that allows users to create posts with text, images, or video content powered by AI. The application supports generating creative captions using OpenAI's GPT-3, generating images using OpenAI's DALL·E API, and generating text-to-video content via an external AI service (e.g., D-ID). Posts can be created, saved as drafts, scheduled for a future time, published, or deleted. A calendar view displays scheduled posts.

## Features

- **AI-Powered Content Generation:**
  - **Caption Generation:** Uses OpenAI's GPT-3 to generate creative captions.
  - **Image Generation:** Uses OpenAI's DALL·E API to generate images based on text input.
  - **Text-to-Video Generation:** Uses an external AI service (e.g., D-ID) to create videos from text input.
- **Post Management:**
  - Create posts with different post types: simple, image, and video.
  - Set post status: created, draft, scheduled, published, or deleted.
  - Schedule posts for future publishing.
- **Calendar View:**
  - View scheduled posts on a FullCalendar-based calendar.
- **Fake Data Generation:**
  - Create fake posts using Faker for testing and development.

## Requirements

Ensure you have Python installed (Python 3.10+ recommended). The project relies on the following dependencies:

