from dotenv import load_dotenv
from bot.models.condition import Condition, Operator
from bot.models.node import NodeFactory
from bot.models.flow import Flow

load_dotenv()


def main():
    # Define travel-related policies
    flight_info = """Flight Information
    Welcome to the TravelBot flight information service! Here are some common questions and answers to assist you with your flight inquiries:

    Q: Can you provide information about flight schedules and availability?
    A: Yes, we can help you find flight schedules and check availability for your desired travel dates. Please provide us with your departure and destination cities, as well as your preferred travel dates, and we'll provide you with the available flight options.

    Q: How can I book a flight ticket?
    A: Booking a flight ticket is easy! Simply let us know your travel itinerary, including your departure and destination cities, travel dates, and any specific preferences you may have, and we'll assist you with the booking process. You can also book tickets directly through our website or mobile app for added convenience.

    Q: What are the baggage allowance and restrictions for my flight?
    A: Baggage allowance and restrictions vary depending on the airline and ticket type. We recommend checking with the airline directly or reviewing the information provided on your ticket or booking confirmation for details about baggage allowances, fees, and restrictions.

    Q: Can I request special assistance or accommodations for my flight?
    A: Yes, many airlines offer special assistance and accommodations for passengers with disabilities or special needs. Please let us know about any specific requirements or requests you may have, and we'll work with the airline to ensure that your travel experience is comfortable and convenient.

    Q: How can I cancel or change my flight reservation?
    A: If you need to cancel or change your flight reservation, please contact our customer support team or the airline directly as soon as possible. Keep in mind that cancellation and change policies vary depending on the airline and ticket type, so it's best to review the terms and conditions of your booking for specific instructions and fees.

    Q: What should I do if my flight is delayed or canceled?
    A: In the event of a flight delay or cancellation, we recommend contacting the airline directly for assistance. They'll be able to provide you with information about alternative flight options, rebooking procedures, and any compensation or accommodations you may be entitled to under their policies and regulations.

    Q: Can I request a refund for my flight ticket?
    A: Refund policies vary depending on the airline, ticket type, and the reason for the refund request. If you're eligible for a refund, please contact our customer support team or the airline directly to initiate the refund process. Be sure to review the refund policy and any associated fees or restrictions before submitting your request."""

    hotel_info = """Hotel Information
    Welcome to the TravelBot hotel information service! Here are some common questions and answers to assist you with your hotel inquiries:

    Q: Can you help me find and book a hotel room?
    A: Certainly! We can assist you in finding and booking a hotel room based on your preferences, budget, and travel dates. Please provide us with the destination city, travel dates, and any specific requirements or preferences you may have, and we'll recommend suitable hotel options for you to choose from.

    Q: What amenities are available at your hotels?
    A: Our hotels offer a wide range of amenities to ensure a comfortable and enjoyable stay for our guests. Common amenities include complimentary breakfast, free Wi-Fi, fitness centers, swimming pools, on-site restaurants, and concierge services. Please let us know if you have any specific preferences or requirements, and we'll help you find a hotel that meets your needs.

    Q: Do you offer special rates or discounts for hotel bookings?
    A: Yes, we frequently offer special rates, discounts, and promotional deals for hotel bookings. These may include early booking discounts, last-minute deals, and special packages for holidays or special events. Please check our website or contact our customer support team for the latest offers and promotions available.

    Q: Can I request additional services or accommodations at the hotel?
    A: Absolutely! We're here to ensure that your stay is as comfortable and convenient as possible. If you have any special requests or require additional services, such as room upgrades, airport transfers, or restaurant reservations, please let us know, and we'll do our best to accommodate your needs.

    Q: What is your hotel's cancellation policy?
    A: Our cancellation policy may vary depending on the hotel, room type, and rate plan selected. We recommend reviewing the terms and conditions of your booking for specific details about our cancellation policy, including any applicable fees or penalties for cancellations made after the specified deadline.

    Q: How can I modify or cancel my hotel reservation?
    A: If you need to modify or cancel your hotel reservation, please contact our customer support team as soon as possible. We'll be happy to assist you with any changes or cancellations, subject to the terms and conditions of your booking. Please note that modifications and cancellations may be subject to fees or penalties, so it's best to review the policy before making any changes."""

    car_rental_info = """Car Rental Information
    Welcome to the TravelBot car rental information service! Here are some common questions and answers to assist you with your car rental inquiries:

    Q: How can I rent a car for my trip?
    A: Renting a car is easy! Simply provide us with your destination city, travel dates, and any specific requirements or preferences you may have, and we'll help you find the perfect car rental option for your needs. You can also book a car rental directly through our website or mobile app for added convenience.

    Q: What types of vehicles are available for rent?
    A: We offer a wide range of vehicles for rent to suit your needs and preferences. Our fleet includes economy cars, compact cars, midsize sedans, SUVs, minivans, and luxury vehicles. Whether you need a small and fuel-efficient car for city driving or a spacious SUV for a family road trip, we've got you covered.

    Q: Do you offer rental insurance coverage?
    A: Yes, we offer rental insurance coverage to provide peace of mind and protection during your rental period. Our insurance options typically include collision damage waiver (CDW), liability insurance, and personal accident insurance. Please let us know if you're interested in adding insurance coverage to your rental agreement, and we'll provide you with more information and options.

    Q: What are the requirements for renting a car?
    A: To rent a car, you must meet certain requirements, including age restrictions, a valid driver's license, and a major credit card for payment and security deposit purposes. The specific requirements may vary depending on the rental location and company policies. Please contact our customer support team for detailed information about the rental requirements in your area.

    Q: Can I pick up and drop off the rental car at different locations?
    A: Yes, we offer flexible pick-up and drop-off options to accommodate your travel itinerary and preferences. You can arrange to pick up the rental car at one location and drop it off at a different location within our network of rental locations. Additional fees may apply for one-way rentals, so please check with us for pricing and availability.

    Q: How can I extend or modify my car rental reservation?
    A: If you need to extend or modify your car rental reservation, please contact our customer support team or the rental location directly as soon as possible. We'll be happy to assist you with any changes or adjustments to your reservation, subject to availability and applicable fees or penalties."""

    vacation_packages_info = """Vacation Packages Information
    Welcome to the TravelBot vacation packages information service! Here are some common questions and answers to assist you with planning your dream vacation:

    Q: What vacation destinations do you offer packages for?
    A: We offer vacation packages for a wide range of destinations worldwide, including popular beach resorts, exotic tropical islands, bustling cities, scenic countryside retreats, and adventurous outdoor destinations. Whether you're dreaming of a relaxing beach getaway, a cultural city tour, or an adrenaline-fueled adventure, we've got the perfect vacation package for you.

    Q: What is included in your vacation packages?
    A: Our vacation packages typically include a combination of accommodation, transportation, meals, activities, and experiences tailored to your preferences and budget. Each package is carefully curated to provide you with a seamless and unforgettable travel experience, with everything you need for a stress-free vacation.

    Q: Can I customize my vacation package?
    A: Yes, we offer flexible options for customizing your vacation package to suit your interests, preferences, and budget. Whether you want to add extra nights, upgrade your accommodation, or include specific activities and experiences, we can tailor your package to create the perfect vacation itinerary for you.

    Q: How do I book a vacation package?
    A: Booking a vacation package is easy! Simply let us know your desired destination, travel dates, budget, and any special preferences or requirements you may have, and we'll create a customized package just for you. You can also browse our website or contact our customer support team for inspiration and assistance with booking.

    Q: What are the payment and cancellation policies for vacation packages?
    A: Our payment and cancellation policies may vary depending on the package, destination, and travel dates. We recommend reviewing the terms and conditions of your booking for specific details about our payment schedule, cancellation deadlines, and any applicable fees or penalties for changes or cancellations.

    Q: Do you offer travel insurance for vacation packages?
    A: Yes, we offer travel insurance options to provide peace of mind and protection during your vacation. Our travel insurance typically includes coverage for trip cancellation, trip interruption, medical emergencies, and other unforeseen events. Please let us know if you're interested in adding travel insurance to your vacation package, and we'll provide you with more information and options."""

    
    chitchat_prompt = """You are a warm and welcoming travel assistant chatbot of DPNA Group. 
    chat with the client in a chitchat style and ask them if they have questions from DPNA travel assistant chatbot.

    << USER MESSAGE >>
    {user_message}
    BOT RESPONSE:"""

    decision_prompt = """
    Categorize the user message into one of the following categories:
    1. flight
    2. hotel
    3. car_Rental
    4. vacation_packages
    5. chitchat

    << USER MESSAGE >>
    {user_message}

    << RULES >>
    1- Put your answer in json format.
    1- The output is a json object that the value of the input message category is TRUE and other output keys are FALSE
    """

    start_node = NodeFactory.create_node(prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'flight': bool,
                                                           'hotel': bool,
                                                           'car_rental': bool,
                                                           'vacation_packages': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)

    # Define nodes for different categories
    flight_info_prompt = f"""You are a travel assistant chatbot. 
    Answer the questions based on the provided policies.

    << FLIGHT QUESTIONS >>
    {flight_info}


    << USER MESSAGE >>
    """ + """{user_message}
    BOT RESPONSE:"""
    flight_node = NodeFactory.create_node(prompt_template=flight_info_prompt,
                                          input_variables=['user_message'],
                                          output_variables='response',
                                          is_output=True)
    
    
    hotel_info_prompt = f"""You are a travel assistant chatbot. 
    Answer the questions based on the provided policies.

    << HOTEL QUESTIONS >>
    {hotel_info}


    << USER MESSAGE >>
    """ + """{user_message}
    BOT RESPONSE:"""

    hotel_node = NodeFactory.create_node(prompt_template=hotel_info_prompt,
                                         input_variables=['user_message'],
                                         output_variables='response',
                                         is_output=True)
    
    car_info_prompt = f"""You are a travel assistant chatbot. 
    Answer the questions based on the provided policies.

    << CAR RENTAL QUESTIONS >>
    {car_rental_info}


    << USER MESSAGE >>
    """ + """{user_message}
    BOT RESPONSE:"""

    car_rental_node = NodeFactory.create_node(prompt_template=car_info_prompt,
                                              input_variables=['user_message'],
                                              output_variables='response',
                                              is_output=True)

    vacation_packages_info_prompt = f"""You are a travel assistant chatbot. 
    Answer the questions based on the provided policies.

    << VACATION PACKAGES QUESTIONS >>
    {vacation_packages_info}


    << USER MESSAGE >>
    """ + """{user_message}
    BOT RESPONSE:"""
    vacation_packages_node = NodeFactory.create_node(prompt_template=vacation_packages_info_prompt,
                                                     input_variables=['user_message'],
                                                     output_variables='response',
                                                     is_output=True)
    
    chitchat_node = NodeFactory.create_node(prompt_template=chitchat_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)


    # Set next nodes based on user selection
    start_node.set_next_item({flight_node: Condition('flight', True, Operator.EQUALS),
                            hotel_node: Condition('hotel', True, Operator.EQUALS),
                            car_rental_node: Condition('car_rental', True, Operator.EQUALS),
                            vacation_packages_node: Condition('vacation_packages', True, Operator.EQUALS),
                            chitchat_node: Condition('chitchat', True, Operator.EQUALS)})

    # Define the flow
    travel_bot_flow = Flow(start_node=start_node)
    travel_bot_flow.initialize()

    # Sample user input
    while(True):
        query = input("Ask me here:  ")
        if query == "exit":
            break
        inp = {'user_message': query}
        answer = travel_bot_flow.run(inp)
        print ("____________________Your Answer___________________________")
        print(answer['response'])
        print ("__________________________________________________________")
    
    




if __name__ == "__main__": 
    main()



