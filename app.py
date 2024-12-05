import streamlit as st
from pyswip import Prolog
from typing import List, Dict

# Initialize Prolog
prolog = Prolog()
prolog.consult("laptop.pl")

def get_mac_recommendations(budget: str, usage: str) -> List[Dict]:
    query = list(prolog.query(
        f"find_mac({budget}, {usage}, Details)", 
        maxresult=1
    ))
    if query:
        return query[0]['Details']
    return []

def get_windows_recommendations(budget: str, usage: str, touch: str, 
                              two_in_one: str, light_weight: str,
                              battery_life: str, screen_size: str) -> List[Dict]:
    query = list(prolog.query(
        f"find_windows({budget}, {usage}, {touch}, {two_in_one}, {light_weight}, {battery_life}, {screen_size}, Details)",
        maxresult=1
    ))
    if query:
        return query[0]['Details']
    return []

def get_usage_type(usage: str) -> str:
    if usage == "Gaming":
        return "gaming"
    elif usage == "Programming":
        return "programming"
    elif usage == "Designing":
        return "designing"
    else:
        return "daily_use"

def get_budget_range(amount: str) -> str:
    if amount == "LKR 0 - LKR 150000":
        return "range_1"
    elif amount == "LKR 150000 - LKR 300000":
        return "range_2"
    elif amount == "LKR 300000 - LKR 400000":
        return "range_3"
    elif amount == "LKR 400000 - LKR 500000":
        return "range_4"
    else:
        return "range_5"

# Title and introduction
st.title("💻 Laptop Recommendation Expert System")
st.write("Welcome! Let me help you find the perfect laptop.")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Please select your budget for the laptop:"}
    ]
if "budget_range" not in st.session_state:
    st.session_state.budget_range = None
if "usage_type" not in st.session_state:
    st.session_state.usage_type = None
if "show_usage_selector" not in st.session_state:
    st.session_state.show_usage_selector = False
if "preferred_os" not in st.session_state:
    st.session_state.preferred_os = None
if "show_touch_screen_option" not in st.session_state:
    st.session_state.show_touch_screen_option = False
if "touch_screen_preference" not in st.session_state:
    st.session_state.touch_screen_preference = None
if "two_in_one_preference" not in st.session_state:
    st.session_state.two_in_one_preference = None
if "light_weight_preference" not in st.session_state:
    st.session_state.light_weight_preference = None
if "battery_life_preference" not in st.session_state:
    st.session_state.battery_life_preference = None
if "large_screen_preference" not in st.session_state:
    st.session_state.large_screen_preference = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Ask for budget range
if st.session_state.budget_range is None:
    budget_options = [
        "LKR 0 - LKR 150000",
        "LKR 150000 - LKR 300000",
        "LKR 300000 - LKR 400000",
        "LKR 400000 - LKR 500000",
        "LKR 500000 and Above"
    ]
    budget = st.selectbox("Select your budget range:", budget_options, key="budget_select")
    if st.button("Confirm Budget"):
        st.session_state.budget_range = get_budget_range(budget)
        st.session_state.messages.append({
            "role": "user",
            "content": f"Budget range: {budget}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "What will be the primary use of your laptop? Choose from below:"
        })
        st.rerun()

# Show usage selector if budget is set but usage isn't
if st.session_state.budget_range and not st.session_state.usage_type:
    st.session_state.show_usage_selector = True

if st.session_state.show_usage_selector:
    usage_options = ["Programming", "Designing", "Daily Use","Gaming"]
    usage = st.selectbox("Select primary use:", usage_options, key="usage_select")
    if st.button("Confirm Usage"):
        st.session_state.usage_type = get_usage_type(usage)
        st.session_state.show_usage_selector = False
        st.session_state.messages.append({
            "role": "user",
            "content": f"Primary use: {usage}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Do you have a preferred operating system? (Mac/Windows)"
        })
        st.rerun()

# Ask for preferred operating system
if st.session_state.usage_type and not st.session_state.preferred_os:
    preferred_os = st.selectbox("Select preferred operating system:", ["Mac", "Windows"], key="os_select")
    if st.button("Confirm OS"):
        st.session_state.preferred_os = preferred_os
        st.session_state.messages.append({
            "role": "user",
            "content": f"Preferred OS: {preferred_os}"
        })
        if preferred_os == "Mac":
            recommendations = get_mac_recommendations(st.session_state.budget_range, st.session_state.usage_type)
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Here are some Mac laptops I recommend:"
            })
            
            for laptop in recommendations:
                # Wrap the processor in single quotes to handle spaces correctly
                processor_quoted = f"'{laptop['processor']}'"

                # Query explanations from Prolog
                explain_price = list(prolog.query(f"explain_price({st.session_state.budget_range}, X)"))
                explain_ram = list(prolog.query(f"explain_ram({laptop['ram']}, X)"))
                explain_storage = list(prolog.query(f"explain_storage({laptop['storage']}, X)"))
                explain_processor = list(prolog.query(f"explain_processor({processor_quoted}, X)"))

                # Extract explanations from the Prolog query results
                price_explanation = explain_price[0]['X'] if explain_price else "No explanation available."
                ram_explanation = explain_ram[0]['X'] if explain_ram else "No explanation available."
                storage_explanation = explain_storage[0]['X'] if explain_storage else "No explanation available."
                processor_explanation = explain_processor[0]['X'] if explain_processor else "No explanation available."

                # Appending messages with the new format
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"""
            ### {laptop['model']}
            **Price**: {laptop['price']} LKR

            **Explanation**:  
            - {price_explanation}  
            {ram_explanation}  
            {storage_explanation}  
            {processor_explanation}
            """
                })

        else:
            st.session_state.show_touch_screen_option = True
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Choose your preferences for a Windows laptop:"
            })
        st.rerun()

# Ask for touch screen preference if Windows is selected
if st.session_state.show_touch_screen_option and st.session_state.touch_screen_preference is None:
    touch_screen_preference = st.radio("Do you prefer a touch screen laptop?", ["Yes", "No"], key="touch_screen_select")
    if st.button("Confirm Touch Screen Preference"):
        st.session_state.touch_screen_preference = "touch_screen" if touch_screen_preference == "Yes" else "none"
        st.session_state.messages.append({
            "role": "user",
            "content": f"Touch screen preference: {touch_screen_preference}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Choose your preferences for a Windows laptop:"
        })
        st.rerun()

# Ask for two-in-one preference
if st.session_state.touch_screen_preference and st.session_state.two_in_one_preference is None:
    two_in_one_preference = st.radio("Do you prefer a two-in-one laptop?", ["Yes", "No"], key="two_in_one_select")
    if st.button("Confirm Two-in-One Preference"):
        st.session_state.two_in_one_preference = "two_in_one" if two_in_one_preference == "Yes" else "none"
        st.session_state.messages.append({
            "role": "user",
            "content": f"Two-in-one preference: {two_in_one_preference}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Choose your preferences for a Windows laptop:"
        })
        st.rerun()

# Ask for light weight preference
if st.session_state.two_in_one_preference and st.session_state.light_weight_preference is None:
    light_weight_preference = st.radio("Do you prefer a light weight laptop?", ["Yes", "No"], key="light_weight_select")
    if st.button("Confirm Light Weight Preference"):
        st.session_state.light_weight_preference = "light_weight" if light_weight_preference == "Yes" else "none"
        st.session_state.messages.append({
            "role": "user",
            "content": f"Light weight preference: {light_weight_preference}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Choose your preferences for a Windows laptop:"
        })
        st.rerun()

# Ask for battery life preference
if st.session_state.light_weight_preference and st.session_state.battery_life_preference is None:
    battery_life_preference = st.radio("Do you prefer a long battery life laptop?", ["Yes", "No"], key="battery_life_select")
    if st.button("Confirm Battery Life Preference"):
        st.session_state.battery_life_preference = "long_battery_life" if battery_life_preference == "Yes" else "none"
        st.session_state.messages.append({
            "role": "user",
            "content": f"Battery life preference: {battery_life_preference}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Choose your preferences for a Windows laptop:"
        })
        st.rerun()

# Ask for large screen preference
if st.session_state.battery_life_preference and st.session_state.large_screen_preference is None:
    large_screen_preference = st.radio("Do you prefer a large screen laptop?", ["Yes", "No"], key="large_screen_select")
    if st.button("Confirm Large Screen Preference"):
        st.session_state.large_screen_preference = "large_screen" if large_screen_preference == "Yes" else "none"
        st.session_state.messages.append({
            "role": "user",
            "content": f"Large screen preference: {large_screen_preference}"
        })
        # Call get_windows_recommendations and display recommendations
        recommendations = get_windows_recommendations(
            st.session_state.budget_range,
            st.session_state.usage_type,
            st.session_state.touch_screen_preference,
            st.session_state.two_in_one_preference,
            st.session_state.light_weight_preference,
            st.session_state.battery_life_preference,
            st.session_state.large_screen_preference
        )
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Here are some Windows laptops I recommend:"
        })
        for laptop in recommendations:
                # Wrap the processor in single quotes to handle spaces correctly
                processor_quoted = f"'{laptop['processor']}'"

                # Query explanations from Prolog
                explain_price = list(prolog.query(f"explain_price({st.session_state.budget_range}, X)"))
                explain_ram = list(prolog.query(f"explain_ram({laptop['ram']}, X)"))
                explain_storage = list(prolog.query(f"explain_storage({laptop['storage']}, X)"))
                explain_processor = list(prolog.query(f"explain_processor({processor_quoted}, X)"))

                # Extract explanations from the Prolog query results
                price_explanation = explain_price[0]['X'] if explain_price else "No explanation available."
                ram_explanation = explain_ram[0]['X'] if explain_ram else "No explanation available."
                storage_explanation = explain_storage[0]['X'] if explain_storage else "No explanation available."
                processor_explanation = explain_processor[0]['X'] if explain_processor else "No explanation available."

                # Appending messages with the new format
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"""
            ### {laptop['model']}
            **Price**: {laptop['price']} LKR

            **Explanation**:  
            - {price_explanation}  
            {ram_explanation}  
            {storage_explanation}  
            {processor_explanation}
            """
                })