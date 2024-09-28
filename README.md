# WhatsApp Chat Analysis 📱

[View WhatsApp Chat Analysis](https://your-streamlit-app-link)

## Overview

The WhatsApp Chat Analysis is a web application built using Streamlit. It provides insights and visualizations based on WhatsApp chat data, allowing users to analyze message statistics, user activity, word clouds, emoji usage, and more.

## Features

- **Message Statistics:** Provides key statistics such as the number of messages, words, and media messages.
- **User Activity Analysis:** Analyzes user activity over time and displays the most active users.
- **Word Cloud Visualization:** Generates a word cloud of the most frequently used words in the chat.
- **Emoji Analysis:** Displays the most commonly used emojis in the chat.

## Technologies Used

- **Python:** Programming language used for developing the app.
- **Streamlit:** Framework used for building the interactive web application.
- **Pandas:** Library used for data manipulation and analysis.
- **NLTK:** Library used for natural language processing, specifically for stopword removal and stemming.
- **Emoji:** Library used for emoji processing.
- **Urlextract:** Library used for extracting URLs from chat messages.
- **Matplotlib & Seaborn:** Libraries used for data visualization.


## How It Works

### Data Preprocessing and Analysis

#### Data Loading:
- Load WhatsApp chat data from a specified file.
- Parse the data to extract user messages, timestamps, and other relevant information.

#### Data Cleaning:
- Handle missing values and clean the data for analysis.
- Normalize message content to lowercase and remove unnecessary characters.

#### Feature Engineering:
- Extract key features such as user activity, message counts, and media messages.
- Create visualizations to represent user activity, word frequency, and emoji usage.

#### Analysis Functions:
- Define functions to generate statistics, user activity maps, and word clouds.
- Use libraries like Matplotlib and Seaborn for data visualization.

## Configuration

You can configure the app by updating the following variables in the script:

- **File Path:** Update the path to your WhatsApp chat data file in the data loading section of the script.

## View the App

You can view the live WhatsApp Chat Analysis app by clicking on the link below:

[View WhatsApp Chat Analysis](https://your-streamlit-app-link)

## Contact

For any questions, suggestions, or feedback, please feel free to reach out:

- **Aditya Pathak**
- **Email:** [adityapathak034@gmail.com](mailto:adityapathak034@gmail.com)
- **GitHub:** [adityapathak0007](https://github.com/adityapathak0007)
- **LinkedIn:** [adityapathak07](https://www.linkedin.com/in/adityapathak07)

### Prerequisites

Ensure you have Python 3.7 or higher installed on your system.

### Clone the Repository

Clone the repository and install the required packages:

```bash
git clone <https://github.com/adityapathak0007/WhatsAppChatAnalysis>
cd WhatsAppChatAnalysis
pip install -r requirements.txt
