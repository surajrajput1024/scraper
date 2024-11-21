# Web Scraper 

## Overview

This project implements a web scraper service designed to extract product data from a paginated e-commerce website. The scraper uses **Selenium** for handling JavaScript-rendered content and **BeautifulSoup** for parsing the HTML. It incorporates retry logic to handle failures during page fetching and product data extraction.

## Features

- **Headless Web Scraping**: Uses Selenium and BeautifulSoup for dynamic content handling and HTML parsing.
- **Retry Logic**: Configurable retry mechanism for page loading and data extraction.
- **Product Data Extraction**: Extracts product name, price, link, and image URL.
- **Logging**: Tracks progress and errors for debugging and monitoring.

## Technologies Used

- **Selenium** for web scraping and dynamic content rendering.
- **BeautifulSoup** for parsing HTML.
- **Python** as the programming language.

## HLD:

```mermaid
graph TD
    %% Entry Point
    A[FastAPI Endpoint /scrape] -->|Authentication - Static Token | B[Scraper Service]
    
    %% Scraper Logic
    B --> C[Fetch Web Pages]
    C -->|Parse Product Data| D[Validate Product Data]
    D -->|Valid Data| E[Cache Service - Redis]
    D -->|Invalid Data| F[Log Parsing Errors]
    
    %% Cache Handling
    E -->|Check for Product Updates| G{Cache Hit?}
    G -->|Yes| H[Skip Update]
    G -->|No| I[Update Storage]

    %% Storage Logic
    I --> J[Store Data in JSON File]
    J -->|Extendable to DBs| K[(Database)]

    %% Notification System
    J --> L[Notify Results]
    L -->|Print Summary| M[Console Output]
    L -->|Extendable| N[Email/Slack/Other Channels]

    %% Retry Mechanism
    C --> O{Page Load Error?}
    O -->|Yes| P[Retry After N Seconds]
    P --> C
    O -->|No| D

    %% Style Definitions
    classDef endpoint fill:#0a9396,stroke:#000,stroke-width:2px,color:#ffffff;
    classDef scraper fill:#005f73,stroke:#000,stroke-width:2px,color:#ffffff;
    classDef cache fill:#ca6702,stroke:#000,stroke-width:2px,color:#ffffff;
    classDef storage fill:#94d2bd,stroke:#000,stroke-width:2px,color:#000000;
    classDef notification fill:#FF6347,stroke:#000,stroke-width:2px,color:#ffffff;
    classDef retry fill:#7f5539,stroke:#000,stroke-width:2px,color:#ffffff;

    %% Apply Styles
    class A endpoint;
    class B,C,D scraper;
    class E,G,H cache;
    class I,J,K storage;
    class L,M,N notification;
    class O,P retry;
```

