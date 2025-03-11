# FoodieSpot Restaurant Reservation System

A simple LLM-powered restaurant reservation assistant that helps users find restaurants and make reservations through natural language.

## Features

- **Restaurant Search**: Search for restaurants by cuisine, location, and price range
- **Availability Checking**: Check available time slots for a specific date
- **Reservation Management**: Make, view, and cancel reservations
- **Natural Language Interface**: Interact with the system through natural language

## Getting Started

### Prerequisites

- Python 3.11
- Groq API key( Llama 3.1-8b )

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Rahul-Bijarniya-1/Sarvam_Chatbot.git
   cd foodiespot
   ```

2. Create a virtual environment:
   ```bash
   py -3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API key:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API key
   ```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure

- `app.py`: Main Streamlit application
- `models/`: Data models for restaurants and reservations
- `data/`: Data storage and sample data generation
- `tools/`: Core functionality for searching, checking availability, and making reservations
- `utils/`: Utility functions for LLM integration and formatting

## How It Works

1. The user interacts with the Streamlit chat interface
2. User messages are sent to the LLM with tool definitions
3. The LLM generates responses and decides when to call tools
4. Tool results are incorporated into the final response
5. All data is stored in simple JSON files

## Customization

- Modify `generate_restuarants.py` to change the sample restaurant data
- Add new tools in the `tools/` directory and register them in `app.py`
- Customize the system prompt in `app.py` to change the assistant's behavior


## Use Case

FoodieSpot operates multiple restaurant locations across the city with varying cuisines, price points, and ambiance. Currently, they handle reservations through a combination of phone calls, third-party booking apps, and an outdated online form. This fragmented approach leads to double-bookings, missed reservations, and frustrated customers.

Our AI reservation system provides a natural language interface that makes it easy for customers to:

1. Search for restaurants based on cuisine, location, party size, and price range
2. Check real-time availability across multiple locations
3. Make, modify, and cancel reservations seamlessly
4. Receive personalized recommendations based on preferences and history
5. Handle special requests and dietary requirements

For restaurant managers, the system:

1. Centralizes reservation management
2. Optimizes table utilization by suggestion alternative times/locations
3. Captures customer preferences for personalized experiences
4. Provides analytics on booking patterns and customer behavior
5. Integrates with existing POS and staffing system

## Goal

To develop an intelligent, conversational AI reservation system that streamlines the booking process for restaurant chains while increasing customer satisfaction, operational efficiency, and revenue growth.

## Long Term Goal

To transform FoodieSpot from a simple reservation system into the industry's leading AI-powered restaurant operations platform, improving table utilization by 25%, increasing average check size by 15%, and reducing staff overhead by 20% within 3 years.

## Success Criteria

1. Customer satisfaction: 90%+ positive feedback on the booking experience
2. Operational efficiency: 30% reduction in time spent on managing reservations
3. Business impact: 15% increase in table utilization rate
4. Technical reliability: 99.5% uptime with <2 second response time
5. Adoption rate: 80% of bookings made through the AI system within 6 months
6. ROI: Complete return on investment within 12-18 months
7. Scalability: System handles 10,000+ concurrent users across 250+ locations

## Business Opportunities Beyond Basic Reservations

1.**Dynamic Pricing Model:** Implement demand-based pricing that offers discounts for off-peak hours and premium pricing for high-demand slots.

    Potential ROI: 8-12% increase in overall revenue


2. **Predictive Inventory Management:** Use reservation data to forecast ingredient needs and reduce food waste

    Potential ROI: 15-20% reduction in food costs.


3. **Pre-Order Functionality:** Allow guests to pre-order meals when making reservations

    Potential ROI: 10-15% increase in average check size.


4.**Customer Intelligence Platform:** Analyze dining patterns and preferences to create targeted marketing campaigns

    Potential ROI: 25% improvement in marketing conversion rates.


5.**Staff Optimization:** Use reservation data to optimize staffing levels
    Potential ROI: 10-15% reduction in labor costs.



# Vertical Expansion Opportunities

1. **FoodieSpot for Hotels:** Adapt the system for hotel restaurant management

    Market size: $15B global hotel restaurant market


2. **FoodieSpot Events:** Extend to event space bookings and catering services

    Market size: $143B global events industry


3. **FoodieSpot Enterprise:** Offer white-label solution to other restaurant groups

    Market size: $70B restaurant technology market


4. **FoodieSpot Analytics:** Sell anonymized trend data to food industry stakeholders

    Market size: $5B restaurant analytics market



# Competitive Advantages

1. **End-to-End AI Integration:** 
Unlike competitors who use AI only for initial customer interaction, our solution uses AI throughout the entire process, from discovery to post-dining follow-up.

2. **Predictive Recommendation Engine:** 
Our proprietary algorithm analyzes past behavior across the customer base to make highly accurate suggestions that competitors can't match.

3. **Operational Intelligence:** 
We don't just manage reservations; we provide actionable business intelligence that transforms reservation data into operational improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.