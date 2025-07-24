from asyncio import run
import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
import mysql.connector 


st.set_page_config(
    page_title="Local Food Waste Management System",
    page_icon="🥬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🥬 Navigation")
page = st.sidebar.selectbox("Choose a page:", 
 ["Dashboard", "View Tables", "CRUD Operations", "SQL Queries"])

if 'df_providers' not in st.session_state:
    st.session_state.df_providers = pd.DataFrame()
if 'df_receivers' not in st.session_state:
    st.session_state.df_receivers = pd.DataFrame()
if 'df_food_listings' not in st.session_state:
    st.session_state.df_food_listings = pd.DataFrame()
if 'df_claims' not in st.session_state:
    st.session_state.df_claims = pd.DataFrame()

if page == "Dashboard":
    st.markdown('<h1 class="main-header">🌱 Local Food Waste Management System</h1>', unsafe_allow_html=True)
    left_co, cent_co, right_co = st.columns(3)
    with cent_co:
       st.image("C:/Users/ACER/Desktop/image/food_waste.jpeg", width=600)

    st.subheader("Introduction")

    st.markdown('''
            <p style="
            font-size:20px; 
            line-height:1.6; 
            color:#2E4057;
            text-align:justify;
           ">
        Food waste is a major problem. many homes and eateries throw away extra food, 
        and many individuals experience food insecurity. The objective of this project 
        is to create a local food waste management system that will allow individuals 
        and restaurants to list excess food.
       </p>
    ''', unsafe_allow_html=True)
    st.markdown('''
           <p style="
           font-size:20px; 
           line-height:1.6; 
           color:#2E4057;
           text-align:justify;
           ">
        🍄The food is available for NGOs or those in need to claim.</br>
        🥭Food locations and details are stored in SQL.</br>
        🥕Filtering, CRUD operations, visualization, and interaction are all made possible by Streamlit apps. 
        </p>
    ''', unsafe_allow_html=True)

elif page == "View Tables":
    st.title("📝Table View")
    st.markdown("Upload your specific CSV files below to view their contents and basic insights.")

    # --- Section for Providers Data ---
    st.header("👤 Providers Data")
    uploaded_providers_file = st.file_uploader(
        "Upload `providers_data.csv`", 
        type=["csv"], 
        key="providers_uploader" # Unique key for this uploader
    )

    if uploaded_providers_file is not None:
        try:
            st.session_state.df_providers = pd.read_csv(uploaded_providers_file)
            st.success("`providers_data.csv` uploaded successfully!")
        except pd.errors.EmptyDataError:
            st.error("The uploaded `providers_data.csv` is empty.")
        except pd.errors.ParserError:
            st.error("Could not parse `providers_data.csv`. Please check its format.")
        except Exception as e:
            st.error(f"An unexpected error occurred with `providers_data.csv`: {e}")

    # Display Providers DataFrame if available
    if not st.session_state.df_providers.empty:
        st.subheader("Preview: Providers Data")
        st.dataframe(st.session_state.df_providers, use_container_width=True)
        with st.expander("Show Data Summary for Providers"):
            st.write("Column types:")
            st.write(st.session_state.df_providers.dtypes)
    else:
        st.info("Awaiting upload for `providers_data.csv`.")


    # --- Section for Receivers Data ---
    st.header("👥 Receivers Data")
    uploaded_receivers_file = st.file_uploader(
        "Upload `receivers_data.csv`", 
        type=["csv"], 
        key="receivers_uploader" # Unique key
    )

    if uploaded_receivers_file is not None:
        try:
            st.session_state.df_receivers = pd.read_csv(uploaded_receivers_file)
            st.success("`receivers_data.csv` uploaded successfully!")
        except pd.errors.EmptyDataError:
            st.error("The uploaded `receivers_data.csv` is empty.")
        except pd.errors.ParserError:
            st.error("Could not parse `receivers_data.csv`. Please check its format.")
        except Exception as e:
            st.error(f"An unexpected error occurred with `receivers_data.csv`: {e}")

    # Display Receivers DataFrame if available
    if not st.session_state.df_receivers.empty:
        st.subheader("Preview: Receivers Data")
        st.dataframe(st.session_state.df_receivers, use_container_width=True)
        with st.expander("Show Data Summary for Receivers"):
            st.write("Column types:")
            st.write(st.session_state.df_receivers.dtypes)
    else:
        st.info("Awaiting upload for `receivers_data.csv`.")


    # --- Section for Food Listings Data ---
    st.header("🍔 Food Listings Data")
    uploaded_food_listings_file = st.file_uploader(
        "Upload `food_listings_data.csv`", 
        type=["csv"], 
        key="food_listings_uploader" # Unique key
    )

    if uploaded_food_listings_file is not None:
        try:
            st.session_state.df_food_listings = pd.read_csv(uploaded_food_listings_file)
            st.success("`food_listings_data.csv` uploaded successfully!")
        except pd.errors.EmptyDataError:
            st.error("The uploaded `food_listings_data.csv` is empty.")
        except pd.errors.ParserError:
            st.error("Could not parse `food_listings_data.csv`. Please check its format.")
        except Exception as e:
            st.error(f"An unexpected error occurred with `food_listings_data.csv`: {e}")

    # Display Food Listings DataFrame if available
    if not st.session_state.df_food_listings.empty:
        st.subheader("Preview: Food Listings Data")
        st.dataframe(st.session_state.df_food_listings, use_container_width=True)
        with st.expander("Show Data Summary for Food Listings"):
            st.write("Column types:")
            st.write(st.session_state.df_food_listings.dtypes)
    else:
        st.info("Awaiting upload for `food_listings_data.csv`.")


    # --- Section for Claims Data ---
    st.header("📝 Claims Data")
    uploaded_claims_file = st.file_uploader(
        "Upload `claims_data.csv`", 
        type=["csv"], 
        key="claims_uploader" # Unique key
    )

    if uploaded_claims_file is not None:
        try:
            st.session_state.df_claims = pd.read_csv(uploaded_claims_file)
            st.success("`claims_data.csv` uploaded successfully!")
        except pd.errors.EmptyDataError:
            st.error("The uploaded `claims_data.csv` is empty.")
        except pd.errors.ParserError:
            st.error("Could not parse `claims_data.csv`. Please check its format.")
        except Exception as e:
            st.error(f"An unexpected error occurred with `claims_data.csv`: {e}")

    # Display Claims DataFrame if available
    if not st.session_state.df_claims.empty:
        st.subheader("Preview: Claims Data")
        st.dataframe(st.session_state.df_claims, use_container_width=True)
        with st.expander("Show Data Summary for Claims"):
            st.write("Column types:")
            st.write(st.session_state.df_claims.dtypes)
    else:
        st.info("Awaiting upload for `claims_data.csv`.")

    st.markdown("---")
    
elif page=="CRUD Operations":
    DB_FILE = "food_data_management.db" # Changed DB file name for clarity

# Removed @st.cache_resource from get_db_connection()
    def get_db_connection():
        """Establishes and returns a database connection."""
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row # Allows accessing columns by name (e.g., row['Name'])
        return conn

    def init_db():
        """Initializes the database and creates all necessary tables if they don't exist."""
        conn = get_db_connection()
        cursor = conn.cursor()

    # Providers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS providers_data (
            Provider_ID INTEGER PRIMARY KEY,
            Name TEXT,
            Type TEXT,
            Address TEXT,
            City TEXT,
            Contact TEXT
           )
        """)

    # Receivers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receivers_data (
            Receiver_ID INTEGER PRIMARY KEY,
            Name TEXT,
            Type TEXT,
            City TEXT,
            Contact TEXT
           )
        """)

    # Food Listings Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_listings_data (
            Food_ID INTEGER PRIMARY KEY,
            Food_Name TEXT,
            Quantity INTEGER,
            Expiry_Date TEXT, -- Stored as TEXT (YYYY-MM-DD)
            Provider_ID INTEGER,
            Provider_Type TEXT,
            Location TEXT,
            Food_Type TEXT,
            Meal_Type TEXT,
            FOREIGN KEY(Provider_ID) REFERENCES providers_data(Provider_ID)
           )
        """)

    # Claims Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims_data (
            Claim_ID INTEGER PRIMARY KEY,
            Food_ID INTEGER,
            Receiver_ID INTEGER,
            Status TEXT,
            Timestamp TEXT, -- Stored as TEXT (YYYY-MM-DD HH:MM:SS)
            FOREIGN KEY(Food_ID) REFERENCES food_listings_data(Food_ID),
            FOREIGN KEY(Receiver_ID) REFERENCES receivers_data(Receiver_ID)
           )
        """)

        conn.commit()
        conn.close() # Close the connection after use

# Initialize the database when the app starts
    init_db()
    st.title("📝 CRUD Operations for Food Data")
    st.markdown("Managing data for Providers, Receivers, Food Listings, and Claims.")

    # --- CRUD Operations Functions (adapted to new schema) ---

    # --- Providers CRUD Functions ---
    @st.cache_data(ttl=5)
    def get_all_providers():
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM providers_data", conn)
        conn.close()
        return df

    def add_provider(provider_id, name, p_type, address, city, contact):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO providers_data (Provider_ID, Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?, ?)",
                (provider_id, name, p_type, address, city, contact)
            )
            conn.commit()
            st.success(f"Provider '{name}' (ID: {provider_id}) added successfully!")
            get_all_providers.clear()
        except sqlite3.IntegrityError:
            st.error(f"Error: Provider ID '{provider_id}' already exists. Please use a unique ID.")
        except sqlite3.Error as e:
            st.error(f"Error adding provider: {e}")
        finally:
            conn.close()

    def update_provider(provider_id, name, p_type, address, city, contact):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE providers_data SET Name = ?, Type = ?, Address = ?, City = ?, Contact = ? WHERE Provider_ID = ?",
                (name, p_type, address, city, contact, provider_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Provider ID {provider_id} updated successfully!")
                get_all_providers.clear()
            else:
                st.warning(f"No provider found with ID {provider_id} to update.")
        except sqlite3.Error as e:
            st.error(f"Error updating provider: {e}")
        finally:
            conn.close()

    def delete_provider(provider_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM providers_data WHERE Provider_ID = ?", (provider_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Provider ID {provider_id} deleted successfully!")
                get_all_providers.clear()
            else:
                st.warning(f"No provider found with ID {provider_id} to delete.")
        except sqlite3.Error as e:
            st.error(f"Error deleting provider: {e}")
        finally:
            conn.close()

    # --- Receivers CRUD Functions ---
    @st.cache_data(ttl=5)
    def get_all_receivers():
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM receivers_data", conn)
        conn.close()
        return df

    def add_receiver(receiver_id, name, r_type, city, contact):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO receivers_data (Receiver_ID, Name, Type, City, Contact) VALUES (?, ?, ?, ?, ?)",
                (receiver_id, name, r_type, city, contact)
            )
            conn.commit()
            st.success(f"Receiver '{name}' (ID: {receiver_id}) added successfully!")
            get_all_receivers.clear()
        except sqlite3.IntegrityError:
            st.error(f"Error: Receiver ID '{receiver_id}' already exists. Please use a unique ID.")
        except sqlite3.Error as e:
            st.error(f"Error adding receiver: {e}")
        finally:
            conn.close()

    def update_receiver(receiver_id, name, r_type, city, contact):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE receivers_data SET Name = ?, Type = ?, City = ?, Contact = ? WHERE Receiver_ID = ?",
                (name, r_type, city, contact, receiver_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Receiver ID {receiver_id} updated successfully!")
                get_all_receivers.clear()
            else:
                st.warning(f"No receiver found with ID {receiver_id} to update.")
        except sqlite3.Error as e:
            st.error(f"Error updating receiver: {e}")
        finally:
            conn.close()

    def delete_receiver(receiver_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM receivers_data WHERE Receiver_ID = ?", (receiver_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Receiver ID {receiver_id} deleted successfully!")
                get_all_receivers.clear()
            else:
                st.warning(f"No receiver found with ID {receiver_id} to delete.")
        except sqlite3.Error as e:
            st.error(f"Error deleting receiver: {e}")
        finally:
            conn.close()

    # --- Food Listings CRUD Functions ---
    @st.cache_data(ttl=5)
    def get_all_food_listings():
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM food_listings_data", conn)
        conn.close()
        return df

    def add_food_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO food_listings_data (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            )
            conn.commit()
            st.success(f"Food Listing '{food_name}' (ID: {food_id}) added successfully!")
            get_all_food_listings.clear()
        except sqlite3.IntegrityError:
            st.error(f"Error: Food ID '{food_id}' already exists. Please use a unique ID.")
        except sqlite3.Error as e:
            st.error(f"Error adding food listing: {e}")
        finally:
            conn.close()

    def update_food_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE food_listings_data SET Food_Name = ?, Quantity = ?, Expiry_Date = ?, Provider_ID = ?, Provider_Type = ?, Location = ?, Food_Type = ?, Meal_Type = ? WHERE Food_ID = ?",
                (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type, food_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Food Listing ID {food_id} updated successfully!")
                get_all_food_listings.clear()
            else:
                st.warning(f"No food listing found with ID {food_id} to update.")
        except sqlite3.Error as e:
            st.error(f"Error updating food listing: {e}")
        finally:
            conn.close()

    def delete_food_listing(food_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM food_listings_data WHERE Food_ID = ?", (food_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Food Listing ID {food_id} deleted successfully!")
                get_all_food_listings.clear()
            else:
                st.warning(f"No food listing found with ID {food_id} to delete.")
        except sqlite3.Error as e:
            st.error(f"Error deleting food listing: {e}")
        finally:
            conn.close()

    # --- Claims CRUD Functions ---
    @st.cache_data(ttl=5)
    def get_all_claims():
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM claims_data", conn)
        conn.close()
        return df

    def add_claim(claim_id, food_id, receiver_id, status, timestamp):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO claims_data (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, ?, ?)",
                (claim_id, food_id, receiver_id, status, timestamp)
            )
            conn.commit()
            st.success(f"Claim '{claim_id}' added successfully!")
            get_all_claims.clear()
        except sqlite3.IntegrityError:
            st.error(f"Error: Claim ID '{claim_id}' already exists. Please use a unique ID.")
        except sqlite3.Error as e:
            st.error(f"Error adding claim: {e}")
        finally:
            conn.close()

    def update_claim(claim_id, food_id, receiver_id, status, timestamp):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE claims_data SET Food_ID = ?, Receiver_ID = ?, Status = ?, Timestamp = ? WHERE Claim_ID = ?",
                (food_id, receiver_id, status, timestamp, claim_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Claim ID {claim_id} updated successfully!")
                get_all_claims.clear()
            else:
                st.warning(f"No claim found with ID {claim_id} to update.")
        except sqlite3.Error as e:
            st.error(f"Error updating claim: {e}")
        finally:
            conn.close()

    def delete_claim(claim_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM claims_data WHERE Claim_ID = ?", (claim_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Claim ID {claim_id} deleted successfully!")
                get_all_claims.clear()
            else:
                st.warning(f"No claim found with ID {claim_id} to delete.")
        except sqlite3.Error as e:
            st.error(f"Error deleting claim: {e}")
        finally:
            conn.close()

    # --- Streamlit UI Layout for each table ---

    # Load current data for all tables
    st.session_state.df_providers = get_all_providers()
    st.session_state.df_receivers = get_all_receivers()
    st.session_state.df_food_listings = get_all_food_listings()
    st.session_state.df_claims = get_all_claims()


    # --- Providers Section ---
    st.header("👤 Providers Data")
    with st.expander("Manage Providers"):
        # --- Create (Add New Provider) ---
        st.subheader("➕ Add New Provider")
        with st.form("add_provider_form", clear_on_submit=True):
            new_Provider_ID = st.number_input("Provider ID", min_value=1, step=1, format="%d", key="add_provider_id")
            new_Name = st.text_input("Provider Name", max_chars=255, key="add_provider_name")
            new_Type = st.text_input("Type", max_chars=100, key="add_provider_type")
            new_Address = st.text_input("Address", max_chars=255, key="add_provider_address")
            new_City = st.text_input("City", max_chars=100, key="add_provider_city")
            new_Contact = st.text_input("Contact Info", max_chars=50, key="add_provider_contact")
            
            submit_add = st.form_submit_button("Add Provider")

            if submit_add:
                if new_Provider_ID and new_Name and new_Type and new_Address and new_City and new_Contact:
                    add_provider(int(new_Provider_ID), new_Name, new_Type, new_Address, new_City, new_Contact)
                else:
                    st.warning("Please fill in all fields to add a provider.")

        st.markdown("---")

        # --- Read (Display Providers) ---
        st.subheader("📋 Current Providers List")
        if not st.session_state.df_providers.empty:
            st.dataframe(st.session_state.df_providers, use_container_width=True, hide_index=True)

            provider_options = [''] + [f"{row['Provider_ID']} - {row['Name']}" for _, row in st.session_state.df_providers.iterrows()]
            selected_option_provider = st.selectbox(
                "Select a Provider for Update/Delete:",
                options=provider_options,
                index=0,
                key="select_provider_id"
            )
            
            selected_provider_id = None
            if selected_option_provider:
                selected_provider_id = int(selected_option_provider.split(' - ')[0])
                st.session_state.selected_provider_data = st.session_state.df_providers[st.session_state.df_providers['Provider_ID'] == selected_provider_id].iloc[0].to_dict()
            else:
                st.session_state.selected_provider_data = {}

        else:
            st.info("No providers found. Add some using the form above!")

        st.markdown("---")

        # --- Update (Modify Existing Provider) ---
        st.subheader("✏️ Update Existing Provider")
        if st.session_state.get('selected_provider_data') and st.session_state.selected_provider_data.get('Provider_ID'):
            selected_id = st.session_state.selected_provider_data.get('Provider_ID')
            st.write(f"**Updating Provider ID:** `{selected_id}`")

            with st.form("update_provider_form"):
                st.text_input("Provider ID (Cannot be changed)", value=str(selected_id), disabled=True, key="update_provider_id_display")
                update_Name = st.text_input("Provider Name", value=st.session_state.selected_provider_data.get('Name', ''), max_chars=255, key="update_provider_name")
                update_Type = st.text_input("Provider Type", value=st.session_state.selected_provider_data.get('Type', ''), max_chars=100, key="update_provider_type")
                update_Address = st.text_input("Address", value=st.session_state.selected_provider_data.get('Address', ''), max_chars=255, key="update_provider_address")
                update_City = st.text_input("City", value=st.session_state.selected_provider_data.get('City', ''), max_chars=100, key="update_provider_city")
                update_Contact = st.text_input("Contact Info", value=st.session_state.selected_provider_data.get('Contact', ''), max_chars=50, key="update_provider_contact")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit_update = st.form_submit_button("Update Provider")
                with col2:
                    cancel_update = st.form_submit_button("Cancel Update")

                if submit_update:
                    if update_Name and update_Type and update_Address and update_City and update_Contact:
                        update_provider(selected_id, update_Name, update_Type, update_Address, update_City, update_Contact)
                        st.session_state.selected_provider_data = {}
                        st.rerun()
                    else:
                        st.warning("Please fill in all fields to update the provider.")
                elif cancel_update:
                    st.session_state.selected_provider_data = {}
                    st.info("Update cancelled.")
                    st.rerun()
        else:
            st.info("Select a provider from the list above to enable the update form.")

        st.markdown("---")

        # --- Delete (Remove Provider) ---
        st.subheader("🗑️ Delete Provider")
        if st.session_state.get('selected_provider_data') and st.session_state.selected_provider_data.get('Provider_ID'):
            selected_id_for_delete = st.session_state.selected_provider_data.get('Provider_ID')
            st.write(f"**Selected Provider for Deletion:** `{st.session_state.selected_provider_data.get('Name')}` (ID: `{selected_id_for_delete}`)")
            
            if st.button(f"Confirm Delete Provider '{st.session_state.selected_provider_data.get('Name')}'", key="delete_provider_button"):
                delete_provider(selected_id_for_delete)
                st.session_state.selected_provider_data = {}
                st.rerun()
        else:
            st.info("Select a provider from the list above to enable the delete option.")
    st.markdown("---") # End of Providers Expander

    # --- Receivers Section ---
    st.header("👥 Receivers Data")
    with st.expander("Manage Receivers"):
        # --- Create (Add New Receiver) ---
        st.subheader("➕ Add New Receiver")
        with st.form("add_receiver_form", clear_on_submit=True):
            new_Receiver_ID = st.number_input("Receiver ID", min_value=1, step=1, format="%d", key="add_receiver_id")
            new_Name_receiver = st.text_input("Receiver Name", max_chars=255, key="add_receiver_name")
            new_Type_receiver = st.text_input("Type", max_chars=100, key="add_receiver_type")
            new_City_receiver = st.text_input("City", max_chars=100, key="add_receiver_city")
            new_Contact_receiver = st.text_input("Contact Info", max_chars=50, key="add_receiver_contact")
            
            submit_add_receiver = st.form_submit_button("Add Receiver")

            if submit_add_receiver:
                if new_Receiver_ID and new_Name_receiver and new_Type_receiver and new_City_receiver and new_Contact_receiver:
                    add_receiver(int(new_Receiver_ID), new_Name_receiver, new_Type_receiver, new_City_receiver, new_Contact_receiver)
                else:
                    st.warning("Please fill in all fields to add a receiver.")

        st.markdown("---")

        # --- Read (Display Receivers) ---
        st.subheader("📋 Current Receivers List")
        if not st.session_state.df_receivers.empty:
            st.dataframe(st.session_state.df_receivers, use_container_width=True, hide_index=True)

            receiver_options = [''] + [f"{row['Receiver_ID']} - {row['Name']}" for _, row in st.session_state.df_receivers.iterrows()]
            selected_option_receiver = st.selectbox(
                "Select a Receiver for Update/Delete:",
                options=receiver_options,
                index=0,
                key="select_receiver_id"
            )
            
            selected_receiver_id = None
            if selected_option_receiver:
                selected_receiver_id = int(selected_option_receiver.split(' - ')[0])
                st.session_state.selected_receiver_data = st.session_state.df_receivers[st.session_state.df_receivers['Receiver_ID'] == selected_receiver_id].iloc[0].to_dict()
            else:
                st.session_state.selected_receiver_data = {}

        else:
            st.info("No receivers found. Add some using the form above!")

        st.markdown("---")

        # --- Update (Modify Existing Receiver) ---
        st.subheader("✏️ Update Existing Receiver")
        if st.session_state.get('selected_receiver_data') and st.session_state.selected_receiver_data.get('Receiver_ID'):
            selected_id_receiver = st.session_state.selected_receiver_data.get('Receiver_ID')
            st.write(f"**Updating Receiver ID:** `{selected_id_receiver}`")

            with st.form("update_receiver_form"):
                st.text_input("Receiver ID (Cannot be changed)", value=str(selected_id_receiver), disabled=True, key="update_receiver_id_display")
                update_Name_receiver = st.text_input("Receiver Name", value=st.session_state.selected_receiver_data.get('Name', ''), max_chars=255, key="update_receiver_name")
                update_Type_receiver = st.text_input("Type", value=st.session_state.selected_receiver_data.get('Type', ''), max_chars=100, key="update_receiver_type")
                update_City_receiver = st.text_input("City", value=st.session_state.selected_receiver_data.get('City', ''), max_chars=100, key="update_receiver_city")
                update_Contact_receiver = st.text_input("Contact Info", value=st.session_state.selected_receiver_data.get('Contact', ''), max_chars=50, key="update_receiver_contact")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit_update_receiver = st.form_submit_button("Update Receiver")
                with col2:
                    cancel_update_receiver = st.form_submit_button("Cancel Update")

                if submit_update_receiver:
                    if update_Name_receiver and update_Type_receiver and update_City_receiver and update_Contact_receiver:
                        update_receiver(selected_id_receiver, update_Name_receiver, update_Type_receiver, update_City_receiver, update_Contact_receiver)
                        st.session_state.selected_receiver_data = {}
                        st.rerun()
                    else:
                        st.warning("Please fill in all fields to update the receiver.")
                elif cancel_update_receiver:
                    st.session_state.selected_receiver_data = {}
                    st.info("Update cancelled.")
                    st.rerun()
        else:
            st.info("Select a receiver from the list above to enable the update form.")

        st.markdown("---")

        # --- Delete (Remove Receiver) ---
        st.subheader("🗑️ Delete Receiver")
        if st.session_state.get('selected_receiver_data') and st.session_state.selected_receiver_data.get('Receiver_ID'):
            selected_id_for_delete_receiver = st.session_state.selected_receiver_data.get('Receiver_ID')
            st.write(f"**Selected Receiver for Deletion:** `{st.session_state.selected_receiver_data.get('Name')}` (ID: `{selected_id_for_delete_receiver}`)")
            
            if st.button(f"Confirm Delete Receiver '{st.session_state.selected_receiver_data.get('Name')}'", key="delete_receiver_button"):
                delete_receiver(selected_id_for_delete_receiver)
                st.session_state.selected_receiver_data = {}
                st.rerun()
        else:
            st.info("Select a receiver from the list above to enable the delete option.")
    st.markdown("---") # End of Receivers Expander

    # --- Food Listings Section ---
    st.header("🍔 Food Listings Data")
    with st.expander("Manage Food Listings"):
        # --- Create (Add New Food Listing) ---
        st.subheader("➕ Add New Food Listing")
        with st.form("add_food_listing_form", clear_on_submit=True):
            new_Food_ID = st.number_input("Food ID", min_value=1, step=1, format="%d", key="add_food_id")
            new_Food_Name = st.text_input("Food Name", max_chars=255, key="add_food_name")
            new_Quantity = st.number_input("Quantity", min_value=0, step=1, format="%d", key="add_quantity")
            new_Expiry_Date = st.date_input("Expiry Date", value=datetime.today(), key="add_expiry_date")
            new_Provider_ID_food = st.number_input("Provider ID (FK)", min_value=1, step=1, format="%d", key="add_provider_id_food")
            new_Provider_Type_food = st.text_input("Provider Type", max_chars=100, key="add_provider_type_food")
            new_Location_food = st.text_input("Location", max_chars=255, key="add_location_food")
            new_Food_Type = st.text_input("Food Type", max_chars=100, key="add_food_type")
            new_Meal_Type = st.text_input("Meal Type", max_chars=100, key="add_meal_type")
            
            submit_add_food = st.form_submit_button("Add Food Listing")

            if submit_add_food:
                if new_Food_ID and new_Food_Name and new_Quantity is not None and new_Expiry_Date and new_Provider_ID_food and new_Provider_Type_food and new_Location_food and new_Food_Type and new_Meal_Type:
                    add_food_listing(int(new_Food_ID), new_Food_Name, int(new_Quantity), new_Expiry_Date.strftime('%Y-%m-%d'), int(new_Provider_ID_food), new_Provider_Type_food, new_Location_food, new_Food_Type, new_Meal_Type)
                else:
                    st.warning("Please fill in all fields to add a food listing.")

        st.markdown("---")

        # --- Read (Display Food Listings) ---
        st.subheader("📋 Current Food Listings List")
        if not st.session_state.df_food_listings.empty:
            st.dataframe(st.session_state.df_food_listings, use_container_width=True, hide_index=True)

            food_options = [''] + [f"{row['Food_ID']} - {row['Food_Name']}" for _, row in st.session_state.df_food_listings.iterrows()]
            selected_option_food = st.selectbox(
                "Select a Food Listing for Update/Delete:",
                options=food_options,
                index=0,
                key="select_food_id"
            )
            
            selected_food_id = None
            if selected_option_food:
                selected_food_id = int(selected_option_food.split(' - ')[0])
                st.session_state.selected_food_listing_data = st.session_state.df_food_listings[st.session_state.df_food_listings['Food_ID'] == selected_food_id].iloc[0].to_dict()
            else:
                st.session_state.selected_food_listing_data = {}

        else:
            st.info("No food listings found. Add some using the form above!")

        st.markdown("---")

        # --- Update (Modify Existing Food Listing) ---
        st.subheader("✏️ Update Existing Food Listing")
        if st.session_state.get('selected_food_listing_data') and st.session_state.selected_food_listing_data.get('Food_ID'):
            selected_id_food = st.session_state.selected_food_listing_data.get('Food_ID')
            st.write(f"**Updating Food Listing ID:** `{selected_id_food}`")

            with st.form("update_food_listing_form"):
                st.text_input("Food ID (Cannot be changed)", value=str(selected_id_food), disabled=True, key="update_food_id_display")
                update_Food_Name = st.text_input("Food Name", value=st.session_state.selected_food_listing_data.get('Food_Name', ''), max_chars=255, key="update_food_name")
                update_Quantity = st.number_input("Quantity", value=int(st.session_state.selected_food_listing_data.get('Quantity', 0)), min_value=0, step=1, format="%d", key="update_quantity")
                
                # Convert string date back to datetime object for date_input
                current_expiry_date = st.session_state.selected_food_listing_data.get('Expiry_Date')
                if current_expiry_date:
                    try:
                        current_expiry_date = datetime.strptime(current_expiry_date, '%Y-%m-%d').date()
                    except ValueError:
                        current_expiry_date = datetime.today().date() # Fallback if date format is wrong
                else:
                    current_expiry_date = datetime.today().date()

                update_Expiry_Date = st.date_input("Expiry Date", value=current_expiry_date, key="update_expiry_date")
                update_Provider_ID_food = st.number_input("Provider ID (FK)", value=int(st.session_state.selected_food_listing_data.get('Provider_ID', 1)), min_value=1, step=1, format="%d", key="update_provider_id_food")
                update_Provider_Type_food = st.text_input("Provider Type", value=st.session_state.selected_food_listing_data.get('Provider_Type', ''), max_chars=100, key="update_provider_type_food")
                update_Location_food = st.text_input("Location", value=st.session_state.selected_food_listing_data.get('Location', ''), max_chars=255, key="update_location_food")
                update_Food_Type = st.text_input("Food Type", value=st.session_state.selected_food_listing_data.get('Food_Type', ''), max_chars=100, key="update_food_type")
                update_Meal_Type = st.text_input("Meal Type", value=st.session_state.selected_food_listing_data.get('Meal_Type', ''), max_chars=100, key="update_meal_type")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit_update_food = st.form_submit_button("Update Food Listing")
                with col2:
                    cancel_update_food = st.form_submit_button("Cancel Update")

                if submit_update_food:
                    if update_Food_Name and update_Quantity is not None and update_Expiry_Date and update_Provider_ID_food and update_Provider_Type_food and update_Location_food and update_Food_Type and update_Meal_Type:
                        update_food_listing(selected_id_food, update_Food_Name, int(update_Quantity), update_Expiry_Date.strftime('%Y-%m-%d'), int(update_Provider_ID_food), update_Provider_Type_food, update_Location_food, update_Food_Type, update_Meal_Type)
                        st.session_state.selected_food_listing_data = {}
                        st.rerun()
                    else:
                        st.warning("Please fill in all fields to update the food listing.")
                elif cancel_update_food:
                    st.session_state.selected_food_listing_data = {}
                    st.info("Update cancelled.")
                    st.rerun()
        else:
            st.info("Select a food listing from the list above to enable the update form.")

        st.markdown("---")

        # --- Delete (Remove Food Listing) ---
        st.subheader("🗑️ Delete Food Listing")
        if st.session_state.get('selected_food_listing_data') and st.session_state.selected_food_listing_data.get('Food_ID'):
            selected_id_for_delete_food = st.session_state.selected_food_listing_data.get('Food_ID')
            st.write(f"**Selected Food Listing for Deletion:** `{st.session_state.selected_food_listing_data.get('Food_Name')}` (ID: `{selected_id_for_delete_food}`)")
            
            if st.button(f"Confirm Delete Food Listing '{st.session_state.selected_food_listing_data.get('Food_Name')}'", key="delete_food_button"):
                delete_food_listing(selected_id_for_delete_food)
                st.session_state.selected_food_listing_data = {}
                st.rerun()
        else:
            st.info("Select a food listing from the list above to enable the delete option.")
    st.markdown("---") # End of Food Listings Expander

    # --- Claims Section ---
    st.header("📝 Claims Data")
    with st.expander("Manage Claims"):
        # --- Create (Add New Claim) ---
        st.subheader("➕ Add New Claim")
        with st.form("add_claim_form", clear_on_submit=True):
            new_Claim_ID = st.number_input("Claim ID", min_value=1, step=1, format="%d", key="add_claim_id")
            new_Food_ID_claim = st.number_input("Food ID (FK)", min_value=1, step=1, format="%d", key="add_food_id_claim")
            new_Receiver_ID_claim = st.number_input("Receiver ID (FK)", min_value=1, step=1, format="%d", key="add_receiver_id_claim")
            new_Status = st.text_input("Status", max_chars=100, key="add_status")
            new_Timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), key="add_timestamp")
            
            submit_add_claim = st.form_submit_button("Add Claim")

            if submit_add_claim:
                if new_Claim_ID and new_Food_ID_claim and new_Receiver_ID_claim and new_Status and new_Timestamp:
                    add_claim(int(new_Claim_ID), int(new_Food_ID_claim), int(new_Receiver_ID_claim), new_Status, new_Timestamp)
                else:
                    st.warning("Please fill in all fields to add a claim.")

        st.markdown("---")

        # --- Read (Display Claims) ---
        st.subheader("📋 Current Claims List")
        if not st.session_state.df_claims.empty:
            st.dataframe(st.session_state.df_claims, use_container_width=True, hide_index=True)

            claim_options = [''] + [f"{row['Claim_ID']} - Status: {row['Status']}" for _, row in st.session_state.df_claims.iterrows()]
            selected_option_claim = st.selectbox(
                "Select a Claim for Update/Delete:",
                options=claim_options,
                index=0,
                key="select_claim_id"
            )
            
            selected_claim_id = None
            if selected_option_claim:
                selected_claim_id = int(selected_option_claim.split(' - ')[0])
                st.session_state.selected_claim_data = st.session_state.df_claims[st.session_state.df_claims['Claim_ID'] == selected_claim_id].iloc[0].to_dict()
            else:
                st.session_state.selected_claim_data = {}

        else:
            st.info("No claims found. Add some using the form above!")

        st.markdown("---")

        # --- Update (Modify Existing Claim) ---
        st.subheader("✏️ Update Existing Claim")
        if st.session_state.get('selected_claim_data') and st.session_state.selected_claim_data.get('Claim_ID'):
            selected_id_claim = st.session_state.selected_claim_data.get('Claim_ID')
            st.write(f"**Updating Claim ID:** `{selected_id_claim}`")

            with st.form("update_claim_form"):
                st.text_input("Claim ID (Cannot be changed)", value=str(selected_id_claim), disabled=True, key="update_claim_id_display")
                update_Food_ID_claim = st.number_input("Food ID (FK)", value=int(st.session_state.selected_claim_data.get('Food_ID', 1)), min_value=1, step=1, format="%d", key="update_food_id_claim")
                update_Receiver_ID_claim = st.number_input("Receiver ID (FK)", value=int(st.session_state.selected_claim_data.get('Receiver_ID', 1)), min_value=1, step=1, format="%d", key="update_receiver_id_claim")
                update_Status = st.text_input("Status", value=st.session_state.selected_claim_data.get('Status', ''), max_chars=100, key="update_status")
                update_Timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value=st.session_state.selected_claim_data.get('Timestamp', ''), key="update_timestamp")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit_update_claim = st.form_submit_button("Update Claim")
                with col2:
                    cancel_update_claim = st.form_submit_button("Cancel Update")

                if submit_update_claim:
                    if update_Food_ID_claim and update_Receiver_ID_claim and update_Status and update_Timestamp:
                        update_claim(selected_id_claim, int(update_Food_ID_claim), int(update_Receiver_ID_claim), update_Status, update_Timestamp)
                        st.session_state.selected_claim_data = {}
                        st.rerun()
                    else:
                        st.warning("Please fill in all fields to update the claim.")
                elif cancel_update_claim:
                    st.session_state.selected_claim_data = {}
                    st.info("Update cancelled.")
                    st.rerun()
        else:
            st.info("Select a claim from the list above to enable the update form.")

        st.markdown("---")

        # --- Delete (Remove Claim) ---
        st.subheader("🗑️ Delete Claim")
        if st.session_state.get('selected_claim_data') and st.session_state.selected_claim_data.get('Claim_ID'):
            selected_id_for_delete_claim = st.session_state.selected_claim_data.get('Claim_ID')
            st.write(f"**Selected Claim for Deletion:** `{selected_id_for_delete_claim}` (Status: `{st.session_state.selected_claim_data.get('Status')}`)")
            
            if st.button(f"Confirm Delete Claim '{selected_id_for_delete_claim}'", key="delete_claim_button"):
                delete_claim(selected_id_for_delete_claim)
                st.session_state.selected_claim_data = {}
                st.rerun()
        else:
            st.info("Select a claim from the list above to enable the delete option.")
    st.markdown("---") # End of Claims Expander
    st.markdown(f"This app demonstrates comprehensive CRUD operations for multiple tables using Streamlit and SQLite.")


    MYSQL_HOST = "localhost" # e.g., "34.123.45.67" or "your-db-instance.us-central1.cloudsql.app"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "12345"
    MYSQL_DATABASE = "food_data"

# --- Database Connection Functions ---
    def get_db_connection():
         """Establishes and returns a MySQL database connection."""
         try:
            conn = mysql.connector.connect(
                 host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            return conn
         except mysql.connector.Error as err:
            st.error(f"Error connecting to MySQL database: {err}")
            st.stop() # Stop the app if connection fails
         except Exception as e:
            st.error(f"An unexpected error occurred during MySQL connection: {e}")
            st.stop()

    def init_db():
        """
        Initializes the MySQL database and creates necessary tables if they don't exist.
        Note: For production MySQL, table creation is often handled separately
        (e.g., via migrations or a database administration tool).
        """
        try:
        # Connect without specifying database first to create it if needed
            conn = mysql.connector.connect(
               host=MYSQL_HOST,
               user=MYSQL_USER,
               password=MYSQL_PASSWORD
            )
            cursor = conn.cursor()

            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
            # Switch to the newly created/existing database
            cursor.execute(f"USE {MYSQL_DATABASE}")

            # Providers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS providers_data (
                    Provider_ID INT PRIMARY KEY,
                    Name VARCHAR(255),
                    Type VARCHAR(100),
                    Address VARCHAR(255),
                    City VARCHAR(100),
                    Contact VARCHAR(50)
                )  ENGINE=InnoDB;
             """)

             # Receivers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS receivers_data (
                   Receiver_ID INT PRIMARY KEY,
                   Name VARCHAR(255),
                   Type VARCHAR(100),
                   City VARCHAR(100),
                   Contact VARCHAR(50)
                )  ENGINE=InnoDB;
             """)

            # Food Listings Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS food_listings_data (
                   Food_ID INT PRIMARY KEY,
                   Food_Name VARCHAR(255),
                   Quantity INT,
                   Expiry_Date DATE, -- Use DATE type for dates
                   Provider_ID INT,
                   Provider_Type VARCHAR(100),
                   Location VARCHAR(255),
                   Food_Type VARCHAR(100),
                   Meal_Type VARCHAR(100),
                   FOREIGN KEY(Provider_ID) REFERENCES providers_data(Provider_ID)
                ) ENGINE=InnoDB;
             """)

            # Claims Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS claims_data (
                   Claim_ID INT PRIMARY KEY,
                   Food_ID INT,
                   Receiver_ID INT,
                   Status VARCHAR(100),
                   Timestamp DATETIME, -- Use DATETIME type for timestamps
                   FOREIGN KEY(Food_ID) REFERENCES food_listings_data(Food_ID),
                   FOREIGN KEY(Receiver_ID) REFERENCES receivers_data(Receiver_ID)
                )  ENGINE=InnoDB;
             """)

            conn.commit()
            conn.close()
            st.success("MySQL database and tables initialized successfully (or already exist).")
        except mysql.connector.Error as err:
            st.error(f"Error initializing MySQL database: {err}")
            st.stop()
        except Exception as e:
            st.error(f"An unexpected error occurred during database initialization: {e}")
            st.stop()

# Initialize the database when the app starts
    init_db()

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="SQL Queries Page (MySQL)", # Changed title to reflect MySQL
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- SQL Queries Page Content ---
if page == "SQL Queries":
    st.title("🔍 SQL Query Page")
    st.markdown("Execute and view results of specific SQL queries from your MySQL database.")
    