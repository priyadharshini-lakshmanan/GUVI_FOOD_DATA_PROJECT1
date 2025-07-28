import streamlit as st
import pandas as pd
import mysql.connector
import os
from datetime import datetime

# -------------------------
# Streamlit page config and sidebar navigation
# -------------------------
st.set_page_config(
    page_title="Local Food Waste Management System",
    page_icon="🥬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🥬 Navigation")
page = st.sidebar.selectbox("Choose a page:", 
                            ["Dashboard", "View Tables", "CRUD Operations", "SQL Queries"])

# -------------------------
# MySQL Configuration - Single Connection Point
# -------------------------
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Localhost@123"  
MYSQL_DATABASE = "food_data"
MYSQL_PORT = 3306

def get_mysql_connection():
    """Establish and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to MySQL database: {err}")
        return None
    except Exception as e:
        st.error(f"Unexpected error during MySQL connection: {e}")
        return None

def init_mysql_db():
    """Create MySQL database and tables if not exist."""
    try:
        # First connect without database to create it
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
        cursor.close()
        conn.close()
        
        # Now connect to the database and create tables
        conn = get_mysql_connection()
        if conn is None:
            return False
            
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS providers_data (
                Provider_ID INT PRIMARY KEY,
                Name VARCHAR(255),
                Type VARCHAR(100),
                Address VARCHAR(255),
                City VARCHAR(100),
                Contact VARCHAR(50)
            ) ENGINE=InnoDB;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receivers_data (
                Receiver_ID INT PRIMARY KEY,
                Name VARCHAR(255),
                Type VARCHAR(100),
                City VARCHAR(100),
                Contact VARCHAR(50)
            ) ENGINE=InnoDB;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_listings_data (
                Food_ID INT PRIMARY KEY,
                Food_Name VARCHAR(255),
                Quantity INT,
                Expiry_Date DATE,
                Provider_ID INT,
                Provider_Type VARCHAR(100),
                Location VARCHAR(255),
                Food_Type VARCHAR(100),
                Meal_Type VARCHAR(100),
                FOREIGN KEY (Provider_ID) REFERENCES providers_data(Provider_ID) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims_data (
                Claim_ID INT PRIMARY KEY,
                Food_ID INT,
                Receiver_ID INT,
                Status VARCHAR(100),
                Timestamp DATETIME,
                FOREIGN KEY (Food_ID) REFERENCES food_listings_data(Food_ID) ON DELETE CASCADE,
                FOREIGN KEY (Receiver_ID) REFERENCES receivers_data(Receiver_ID) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error initializing MySQL database: {err}")
        return False
    except Exception as e:
        st.error(f"Unexpected error during database initialization: {e}")
        return False

# Initialize database on startup
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = init_mysql_db()

# -------------------------
# Session state initialization
# -------------------------
if 'selected_provider_data' not in st.session_state:
    st.session_state.selected_provider_data = {}
if 'selected_receiver_data' not in st.session_state:
    st.session_state.selected_receiver_data = {}
if 'selected_food_listing_data' not in st.session_state:
    st.session_state.selected_food_listing_data = {}
if 'selected_claim_data' not in st.session_state:
    st.session_state.selected_claim_data = {}

# -------------------------
# Data Loading Functions
# -------------------------
@st.cache_data(ttl=5)
def load_table_data(table_name):
    """Load data from MySQL table"""
    conn = get_mysql_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading {table_name}: {e}")
        conn.close()
        return pd.DataFrame()

def clear_cache():
    """Clear all cached data"""
    load_table_data.clear()

# ===========================
# Dashboard Page
# ===========================
if page == "Dashboard":
    st.markdown('<h1 class="main-header">🌱 Local Food Waste Management System</h1>', unsafe_allow_html=True)
    left_co, cent_co, right_co = st.columns(3)
    with cent_co:
        # Use a placeholder image or remove this line if image doesn't exist
        try:
            st.image("C:/Users/ACER/Desktop/image/food_waste.jpeg", width=600)
        except:
            st.info("🌱 Welcome to Food Waste Management System")
    
    st.subheader("Introduction")
    st.markdown('''
        <p style="
        font-size:20px; 
        line-height:1.6; 
        color:#2E4057;
        text-align:justify;
        ">
        Food waste is a major problem. Many homes and eateries throw away extra food, 
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
        🍄The food is available for NGOs or those in need to claim.<br>
        🥭Food locations and details are stored in MySQL database.<br>
        🥕Filtering, CRUD operations, visualization, and interaction are all made possible by Streamlit apps. 
        </p>
    ''', unsafe_allow_html=True)

# ===========================
# View Tables Page
# ===========================
elif page == "View Tables":
    st.title("📝 Table View")
    st.markdown("Select a table to view and filter its data from MySQL database.")

    if not st.session_state.db_initialized:
        st.error("Database not initialized. Please check your MySQL connection.")
        st.stop()

    table_dict = {
        "Providers Data": "providers_data",
        "Receivers Data": "receivers_data", 
        "Food Listings Data": "food_listings_data",
        "Claims Data": "claims_data"
    }

    selected_table_name = st.selectbox("Select Table to View", list(table_dict.keys()))
    table_name = table_dict[selected_table_name]

    # Load data from MySQL
    df = load_table_data(table_name)
    
    if df.empty:
        st.info(f"No {selected_table_name} found in database. Please add data using CRUD Operations.")
    else:
        st.subheader(f"Preview: {selected_table_name}")
        st.dataframe(df, use_container_width=True)

        with st.expander(f"Show Data Summary for {selected_table_name}"):
            st.write(f"Total rows: {len(df)}")
            st.write("Column types:")
            st.write(df.dtypes)

        st.markdown("---")
        st.markdown("### Search and Filter Rows")
        with st.form("filter_form"):
            search_text = st.text_input("Type the filter text:")
            filter_button = st.form_submit_button("Filter")

        if filter_button and search_text:
            mask = pd.Series([False] * len(df))
            for col in df.select_dtypes(include=['object', 'string']).columns:
                mask = mask | df[col].astype(str).str.contains(search_text, case=False, na=False)
            filtered_df = df[mask]
            if filtered_df.empty:
                st.warning("No rows match your search.")
            else:
                st.dataframe(filtered_df, use_container_width=True)

# ===========================
# CRUD Operations Page (MySQL)
# ===========================
elif page == "CRUD Operations":
    st.title("📝 CRUD Operations for Food Data")
    st.markdown("Managing data in MySQL database for Providers, Receivers, Food Listings, and Claims.")

    if not st.session_state.db_initialized:
        st.error("Database not initialized. Please check your MySQL connection.")
        st.stop()

    # --------- CRUD Functions for MySQL -------------

    # Providers CRUD
    def add_provider(provider_id, name, p_type, address, city, contact):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO providers_data (Provider_ID, Name, Type, Address, City, Contact) VALUES (%s, %s, %s, %s, %s, %s)",
                (provider_id, name, p_type, address, city, contact)
            )
            conn.commit()
            st.success(f"Provider '{name}' (ID: {provider_id}) added successfully!")
            clear_cache()
        except mysql.connector.IntegrityError:
            st.error(f"Error: Provider ID '{provider_id}' already exists. Please use a unique ID.")
        except Exception as e:
            st.error(f"Error adding provider: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_provider(provider_id, name, p_type, address, city, contact):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE providers_data SET Name = %s, Type = %s, Address = %s, City = %s, Contact = %s WHERE Provider_ID = %s",
                (name, p_type, address, city, contact, provider_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Provider ID {provider_id} updated successfully!")
                clear_cache()
            else:
                st.warning(f"No provider found with ID {provider_id} to update.")
        except Exception as e:
            st.error(f"Error updating provider: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_provider(provider_id):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM providers_data WHERE Provider_ID = %s", (provider_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Provider ID {provider_id} deleted successfully!")
                clear_cache()
            else:
                st.warning(f"No provider found with ID {provider_id} to delete.")
        except Exception as e:
            st.error(f"Error deleting provider: {e}")
        finally:
            cursor.close()
            conn.close()

    # Similar functions for receivers, food_listings, and claims
    def add_receiver(receiver_id, name, r_type, city, contact):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO receivers_data (Receiver_ID, Name, Type, City, Contact) VALUES (%s, %s, %s, %s, %s)",
                (receiver_id, name, r_type, city, contact)
            )
            conn.commit()
            st.success(f"Receiver '{name}' (ID: {receiver_id}) added successfully!")
            clear_cache()
        except mysql.connector.IntegrityError:
            st.error(f"Error: Receiver ID '{receiver_id}' already exists. Please use a unique ID.")
        except Exception as e:
            st.error(f"Error adding receiver: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_receiver(receiver_id, name, r_type, city, contact):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE receivers_data SET Name = %s, Type = %s, City = %s, Contact = %s WHERE Receiver_ID = %s",
                (name, r_type, city, contact, receiver_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Receiver ID {receiver_id} updated successfully!")
                clear_cache()
            else:
                st.warning(f"No receiver found with ID {receiver_id} to update.")
        except Exception as e:
            st.error(f"Error updating receiver: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_receiver(receiver_id):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM receivers_data WHERE Receiver_ID = %s", (receiver_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Receiver ID {receiver_id} deleted successfully!")
                clear_cache()
            else:
                st.warning(f"No receiver found with ID {receiver_id} to delete.")
        except Exception as e:
            st.error(f"Error deleting receiver: {e}")
        finally:
            cursor.close()
            conn.close()

    def add_food_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO food_listings_data (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            )
            conn.commit()
            st.success(f"Food Listing '{food_name}' (ID: {food_id}) added successfully!")
            clear_cache()
        except mysql.connector.IntegrityError:
            st.error(f"Error: Food ID '{food_id}' already exists. Please use a unique ID.")
        except Exception as e:
            st.error(f"Error adding food listing: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_food_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE food_listings_data SET Food_Name = %s, Quantity = %s, Expiry_Date = %s, Provider_ID = %s, Provider_Type = %s, Location = %s, Food_Type = %s, Meal_Type = %s WHERE Food_ID = %s",
                (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type, food_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Food Listing ID {food_id} updated successfully!")
                clear_cache()
            else:
                st.warning(f"No food listing found with ID {food_id} to update.")
        except Exception as e:
            st.error(f"Error updating food listing: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_food_listing(food_id):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM food_listings_data WHERE Food_ID = %s", (food_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Food Listing ID {food_id} deleted successfully!")
                clear_cache()
            else:
                st.warning(f"No food listing found with ID {food_id} to delete.")
        except Exception as e:
            st.error(f"Error deleting food listing: {e}")
        finally:
            cursor.close()
            conn.close()

    def add_claim(claim_id, food_id, receiver_id, status, timestamp):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO claims_data (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp) VALUES (%s, %s, %s, %s, %s)",
                (claim_id, food_id, receiver_id, status, timestamp)
            )
            conn.commit()
            st.success(f"Claim '{claim_id}' added successfully!")
            clear_cache()
        except mysql.connector.IntegrityError:
            st.error(f"Error: Claim ID '{claim_id}' already exists. Please use a unique ID.")
        except Exception as e:
            st.error(f"Error adding claim: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_claim(claim_id, food_id, receiver_id, status, timestamp):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE claims_data SET Food_ID = %s, Receiver_ID = %s, Status = %s, Timestamp = %s WHERE Claim_ID = %s",
                (food_id, receiver_id, status, timestamp, claim_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Claim ID {claim_id} updated successfully!")
                clear_cache()
            else:
                st.warning(f"No claim found with ID {claim_id} to update.")
        except Exception as e:
            st.error(f"Error updating claim: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_claim(claim_id):
        conn = get_mysql_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM claims_data WHERE Claim_ID = %s", (claim_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Claim ID {claim_id} deleted successfully!")
                clear_cache()
            else:
                st.warning(f"No claim found with ID {claim_id} to delete.")
        except Exception as e:
            st.error(f"Error deleting claim: {e}")
        finally:
            cursor.close()
            conn.close()

    # Load current data for CRUD operations
    df_providers = load_table_data("providers_data")
    df_receivers = load_table_data("receivers_data")
    df_food_listings = load_table_data("food_listings_data")
    df_claims = load_table_data("claims_data")

    # -------- Providers CRUD Interface ---
    st.header("👤 Providers Data")
    with st.expander("Manage Providers"):

        # Add New Provider
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
                if all([new_Provider_ID, new_Name, new_Type, new_Address, new_City, new_Contact]):
                    add_provider(int(new_Provider_ID), new_Name, new_Type, new_Address, new_City, new_Contact)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields to add a provider.")

        st.markdown("---")

        # Provider Selection for Update/Delete
        if not df_providers.empty:
            provider_options = [''] + [f"{row['Provider_ID']} - {row['Name']}" for _, row in df_providers.iterrows()]
            selected_option_provider = st.selectbox("Select a Provider for Update/Delete:", provider_options, key="select_provider")

            if selected_option_provider and selected_option_provider != '':
                selected_provider_id = int(selected_option_provider.split(' - ')[0])
                st.session_state.selected_provider_data = df_providers[
                    df_providers['Provider_ID']==selected_provider_id
                ].iloc[0].to_dict()
            else:
                st.session_state.selected_provider_data = {}
        else:
            st.info("No providers found to select for update/delete.")

        # Update Provider
        st.subheader("✏️ Update Existing Provider")
        if st.session_state.selected_provider_data and st.session_state.selected_provider_data.get('Provider_ID'):
            sel = st.session_state.selected_provider_data
            st.write(f"**Updating Provider ID:** `{sel['Provider_ID']}`")

            with st.form("update_provider_form"):
                st.text_input("Provider ID (Cannot be changed)", value=str(sel['Provider_ID']), disabled=True)
                update_Name = st.text_input("Provider Name", value=sel.get('Name',''), key="update_provider_name")
                update_Type = st.text_input("Provider Type", value=sel.get('Type',''), key="update_provider_type_update")
                update_Address = st.text_input("Address", value=sel.get('Address',''), key="update_provider_address")
                update_City = st.text_input("City", value=sel.get('City',''), key="update_provider_city")
                update_Contact = st.text_input("Contact Info", value=sel.get('Contact',''), key="update_provider_contact")

                col1, col2 = st.columns(2)
                with col1:
                    submit_update = st.form_submit_button("Update Provider")
                with col2:
                    cancel_update = st.form_submit_button("Cancel Update")

                if submit_update:
                    if all([update_Name, update_Type, update_Address, update_City, update_Contact]):
                        update_provider(sel['Provider_ID'], update_Name, update_Type, update_Address, update_City, update_Contact)
                        st.session_state.selected_provider_data = {}
                        st.rerun()
                    else:
                        st.warning("Please fill in all fields to update the provider.")

                if cancel_update:
                    st.session_state.selected_provider_data = {}
                    st.info("Update cancelled.")
                    st.rerun()
        else:
            st.info("Select a provider above to update.")

        # Delete Provider
        st.subheader("🗑️ Delete Provider")
        if st.session_state.selected_provider_data and st.session_state.selected_provider_data.get('Provider_ID'):
            sel = st.session_state.selected_provider_data
            st.write(f"**Selected Provider for Deletion:** `{sel.get('Name')}` (ID: `{sel.get('Provider_ID')}`)")
            if st.button(f"Confirm Delete Provider '{sel.get('Name')}'"):
                delete_provider(sel.get('Provider_ID'))
                st.session_state.selected_provider_data = {}
                st.rerun()
        else:
            st.info("Select a provider above to delete.")

    # ------- RECEIVERS CRUD SECTION --------
    st.markdown("---")
    st.header("👥 Receivers Data")
    with st.expander("Manage Receivers"):

        # Add New Receiver
        st.subheader("➕ Add New Receiver")
        with st.form("add_receiver_form", clear_on_submit=True):
            new_Receiver_ID = st.number_input("Receiver ID", min_value=1, step=1, format="%d", key="add_receiver_id")
            new_Name_receiver = st.text_input("Receiver Name", max_chars=255, key="add_receiver_name")
            new_Type_receiver = st.text_input("Type", max_chars=100, key="add_receiver_type")
            new_City_receiver = st.text_input("City", max_chars=100, key="add_receiver_city")
            new_Contact_receiver = st.text_input("Contact Info", max_chars=50, key="add_receiver_contact")

            submit_add_receiver = st.form_submit_button("Add Receiver")
            if submit_add_receiver:
                if all([new_Receiver_ID, new_Name_receiver, new_Type_receiver, new_City_receiver, new_Contact_receiver]):
                    add_receiver(int(new_Receiver_ID), new_Name_receiver, new_Type_receiver, new_City_receiver, new_Contact_receiver)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields to add a receiver.")

        st.markdown("---")

        # Update Receiver
        st.subheader("✏️ Update Existing Receiver")
        if not df_receivers.empty:
            receiver_options = [''] + [f"{row['Receiver_ID']} - {row['Name']}" for _, row in df_receivers.iterrows()]
            selected_option_receiver = st.selectbox("Select a Receiver for Update/Delete:", receiver_options, key="select_receiver")

            if selected_option_receiver and selected_option_receiver != '':
                selected_receiver_id = int(selected_option_receiver.split(' - ')[0])
                st.session_state.selected_receiver_data = df_receivers[
                    df_receivers['Receiver_ID'] == selected_receiver_id
                ].iloc[0].to_dict()
            else:
                st.session_state.selected_receiver_data = {}

            if st.session_state.selected_receiver_data and st.session_state.selected_receiver_data.get('Receiver_ID'):
                sel = st.session_state.selected_receiver_data
                st.write(f"**Updating Receiver ID:** `{sel['Receiver_ID']}`")

                with st.form("update_receiver_form"):
                    st.text_input("Receiver ID (Cannot be changed)", value=str(sel['Receiver_ID']), disabled=True)
                    update_Name_receiver = st.text_input("Receiver Name", value=sel.get('Name',''), key="update_receiver_name")
                    update_Type_receiver = st.text_input("Type", value=sel.get('Type',''), key="update_receiver_type")
                    update_City_receiver = st.text_input("City", value=sel.get('City',''), key="update_receiver_city")
                    update_Contact_receiver = st.text_input("Contact Info", value=sel.get('Contact',''), key="update_receiver_contact")

                    col1, col2 = st.columns(2)
                    with col1:
                        submit_update_receiver = st.form_submit_button("Update Receiver")
                    with col2:
                        cancel_update_receiver = st.form_submit_button("Cancel Update")

                    if submit_update_receiver:
                        if all([update_Name_receiver, update_Type_receiver, update_City_receiver, update_Contact_receiver]):
                            update_receiver(sel['Receiver_ID'], update_Name_receiver, update_Type_receiver, update_City_receiver, update_Contact_receiver)
                            st.session_state.selected_receiver_data = {}
                            st.rerun()
                        else:
                            st.warning("Please fill in all fields to update the receiver.")

                    if cancel_update_receiver:
                        st.session_state.selected_receiver_data = {}
                        st.info("Update cancelled.")
                        st.rerun()
            else:
                st.info("Select a receiver above to update.")
        else:
            st.info("No receivers found. Add some above to update.")

        st.markdown("---")

        # Delete Receiver
        st.subheader("🗑️ Delete Receiver")
        if st.session_state.selected_receiver_data and st.session_state.selected_receiver_data.get('Receiver_ID'):
            sel = st.session_state.selected_receiver_data
            st.write(f"**Selected Receiver for Deletion:** `{sel.get('Name')}` (ID: `{sel.get('Receiver_ID')}`)")
            if st.button(f"Confirm Delete Receiver '{sel.get('Name')}'"):
                delete_receiver(sel.get('Receiver_ID'))
                st.session_state.selected_receiver_data = {}
                st.rerun()
        else:
            st.info("Select a receiver above to delete.")

        st.markdown("---")

        # Current Receivers List (at the end)
        st.subheader("📋 Current Receivers List")
        if not df_receivers.empty:
            st.dataframe(df_receivers, use_container_width=True, hide_index=True)
        else:
            st.info("No receivers found in database.")

    # ------- FOOD LISTINGS CRUD SECTION --------
    st.markdown("---")
    st.header("🍔 Food Listings Data")
    with st.expander("Manage Food Listings"):

        # Add New Food Listing
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
                if all([new_Food_ID, new_Food_Name, new_Quantity is not None, new_Expiry_Date, new_Provider_ID_food, new_Provider_Type_food,
                        new_Location_food, new_Food_Type, new_Meal_Type]):
                    add_food_listing(int(new_Food_ID), new_Food_Name, int(new_Quantity), new_Expiry_Date.strftime('%Y-%m-%d'),
                                     int(new_Provider_ID_food), new_Provider_Type_food, new_Location_food, new_Food_Type, new_Meal_Type)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields to add a food listing.")

        st.markdown("---")

        # Update Food Listing
        st.subheader("✏️ Update Existing Food Listing")
        if not df_food_listings.empty:
            food_options = [''] + [f"{row['Food_ID']} - {row['Food_Name']}" for _, row in df_food_listings.iterrows()]
            selected_option_food = st.selectbox("Select a Food Listing for Update/Delete:", food_options, key="select_food_listing")

            if selected_option_food and selected_option_food != '':
                selected_food_id = int(selected_option_food.split(' - ')[0])
                st.session_state.selected_food_listing_data = df_food_listings[
                    df_food_listings['Food_ID'] == selected_food_id
                ].iloc[0].to_dict()
            else:
                st.session_state.selected_food_listing_data = {}

            if st.session_state.selected_food_listing_data and st.session_state.selected_food_listing_data.get('Food_ID'):
                sel = st.session_state.selected_food_listing_data
                st.write(f"**Updating Food Listing ID:** `{sel['Food_ID']}`")

                with st.form("update_food_listing_form"):
                    st.text_input("Food ID (Cannot be changed)", value=str(sel['Food_ID']), disabled=True)
                    update_Food_Name = st.text_input("Food Name", value=sel.get('Food_Name',''), key="update_food_name")
                    update_Quantity = st.number_input("Quantity", value=int(sel.get('Quantity', 0)), min_value=0, step=1, format="%d", key="update_quantity")

                    # Convert stored date string to datetime.date object for date_input
                    parsed_date = None
                    try:
                        parsed_date = datetime.strptime(str(sel.get('Expiry_Date','')), '%Y-%m-%d').date()
                    except Exception:
                        parsed_date = datetime.today().date()
                    update_Expiry_Date = st.date_input("Expiry Date", value=parsed_date, key="update_expiry_date")

                    update_Provider_ID_food = st.number_input("Provider ID (FK)", value=int(sel.get('Provider_ID', 1)), min_value=1, step=1, format="%d", key="update_provider_id_food")
                    update_Provider_Type_food = st.text_input("Provider Type", value=sel.get('Provider_Type',''), key="update_provider_type_food")
                    update_Location_food = st.text_input("Location", value=sel.get('Location',''), key="update_location_food")
                    update_Food_Type = st.text_input("Food Type", value=sel.get('Food_Type',''), key="update_food_type")
                    update_Meal_Type = st.text_input("Meal Type", value=sel.get('Meal_Type',''), key="update_meal_type")

                    col1, col2 = st.columns(2)
                    with col1:
                        submit_update_food = st.form_submit_button("Update Food Listing")
                    with col2:
                        cancel_update_food = st.form_submit_button("Cancel Update")

                    if submit_update_food:
                        if all([update_Food_Name, update_Quantity is not None, update_Expiry_Date, update_Provider_ID_food,
                                update_Provider_Type_food, update_Location_food, update_Food_Type, update_Meal_Type]):
                            update_food_listing(sel['Food_ID'], update_Food_Name, int(update_Quantity), update_Expiry_Date.strftime('%Y-%m-%d'),
                                                int(update_Provider_ID_food), update_Provider_Type_food, update_Location_food, update_Food_Type, update_Meal_Type)
                            st.session_state.selected_food_listing_data = {}
                            st.rerun()
                        else:
                            st.warning("Please fill in all fields to update the food listing.")

                    if cancel_update_food:
                        st.session_state.selected_food_listing_data = {}
                        st.info("Update cancelled.")
                        st.rerun()
            else:
                st.info("Select a food listing above to update.")
        else:
            st.info("No food listings found. Add some above to update.")

        st.markdown("---")

        # Delete Food Listing
        st.subheader("🗑️ Delete Food Listing")
        if st.session_state.selected_food_listing_data and st.session_state.selected_food_listing_data.get('Food_ID'):
            sel = st.session_state.selected_food_listing_data
            st.write(f"**Selected Food Listing for Deletion:** `{sel.get('Food_Name')}` (ID: `{sel.get('Food_ID')}`)")
            if st.button(f"Confirm Delete Food Listing '{sel.get('Food_Name')}'"):
                delete_food_listing(sel.get('Food_ID'))
                st.session_state.selected_food_listing_data = {}
                st.rerun()
        else:
            st.info("Select a food listing above to delete.")

        st.markdown("---")

        # Current Food Listings List (at the end)
        st.subheader("📋 Current Food Listings List")
        if not df_food_listings.empty:
            st.dataframe(df_food_listings, use_container_width=True, hide_index=True)
        else:
            st.info("No food listings found in database.")

    # ------- CLAIMS CRUD SECTION --------
    st.markdown("---")
    st.header("📝 Claims Data")
    with st.expander("Manage Claims"):

        # Add New Claim
        st.subheader("➕ Add New Claim")
        with st.form("add_claim_form", clear_on_submit=True):
            new_Claim_ID = st.number_input("Claim ID", min_value=1, step=1, format="%d", key="add_claim_id")
            new_Food_ID_claim = st.number_input("Food ID (FK)", min_value=1, step=1, format="%d", key="add_food_id_claim")
            new_Receiver_ID_claim = st.number_input("Receiver ID (FK)", min_value=1, step=1, format="%d", key="add_receiver_id_claim")
            new_Status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"], key="add_status")
            new_Timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), key="add_timestamp")

            submit_add_claim = st.form_submit_button("Add Claim")
            if submit_add_claim:
                if all([new_Claim_ID, new_Food_ID_claim, new_Receiver_ID_claim, new_Status, new_Timestamp]):
                    add_claim(int(new_Claim_ID), int(new_Food_ID_claim), int(new_Receiver_ID_claim), new_Status, new_Timestamp)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields to add a claim.")

        st.markdown("---")

        # Update Claim
        st.subheader("✏️ Update Existing Claim")
        if not df_claims.empty:
            claim_options = [''] + [f"{row['Claim_ID']} - Status: {row['Status']}" for _, row in df_claims.iterrows()]
            selected_option_claim = st.selectbox("Select a Claim for Update/Delete:", claim_options, key="select_claim")

            if selected_option_claim and selected_option_claim != '':
                selected_claim_id = int(selected_option_claim.split(' - ')[0])
                st.session_state.selected_claim_data = df_claims[
                    df_claims['Claim_ID'] == selected_claim_id
                ].iloc[0].to_dict()
            else:
                st.session_state.selected_claim_data = {}

            if st.session_state.selected_claim_data and st.session_state.selected_claim_data.get('Claim_ID'):
                sel = st.session_state.selected_claim_data
                st.write(f"**Updating Claim ID:** `{sel['Claim_ID']}`")

                with st.form("update_claim_form"):
                    st.text_input("Claim ID (Cannot be changed)", value=str(sel['Claim_ID']), disabled=True)
                    update_Food_ID_claim = st.number_input("Food ID (FK)", value=int(sel.get('Food_ID',1)), min_value=1, step=1, format="%d", key="update_food_id_claim")
                    update_Receiver_ID_claim = st.number_input("Receiver ID (FK)", value=int(sel.get('Receiver_ID',1)), min_value=1, step=1, format="%d", key="update_receiver_id_claim")
                    update_Status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"], 
                                                index=["Pending", "Completed", "Cancelled"].index(sel.get('Status', 'Pending')) if sel.get('Status') in ["Pending", "Completed", "Cancelled"] else 0, 
                                                key="update_status")
                    update_Timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value=str(sel.get('Timestamp','')), key="update_timestamp")

                    col1, col2 = st.columns(2)
                    with col1:
                        submit_update_claim = st.form_submit_button("Update Claim")
                    with col2:
                        cancel_update_claim = st.form_submit_button("Cancel Update")

                    if submit_update_claim:
                        if all([update_Food_ID_claim, update_Receiver_ID_claim, update_Status, update_Timestamp]):
                            update_claim(sel['Claim_ID'], int(update_Food_ID_claim), int(update_Receiver_ID_claim), update_Status, update_Timestamp)
                            st.session_state.selected_claim_data = {}
                            st.rerun()
                        else:
                            st.warning("Please fill in all fields to update the claim.")

                    if cancel_update_claim:
                        st.session_state.selected_claim_data = {}
                        st.info("Update cancelled.")
                        st.rerun()
            else:
                st.info("Select a claim above to update.")
        else:
            st.info("No claims found. Add some above to update.")

        st.markdown("---")

        # Delete Claim
        st.subheader("🗑️ Delete Claim")
        if st.session_state.selected_claim_data and st.session_state.selected_claim_data.get('Claim_ID'):
            sel = st.session_state.selected_claim_data
            st.write(f"**Selected Claim for Deletion:** `{sel.get('Claim_ID')}` (Status: `{sel.get('Status')}`)")
            if st.button(f"Confirm Delete Claim '{sel.get('Claim_ID')}'"):
                delete_claim(sel.get('Claim_ID'))
                st.session_state.selected_claim_data = {}
                st.rerun()
        else:
            st.info("Select a claim above to delete.")

        st.markdown("---")

        # Current Claims List (at the end)
        st.subheader("📋 Current Claims List")
        if not df_claims.empty:
            st.dataframe(df_claims, use_container_width=True, hide_index=True)
        else:
            st.info("No claims found in database.")

# ===========================
# SQL Queries Page (MySQL)
# ===========================
elif page == "SQL Queries":
    st.title("🔍 SQL Query Page")
    st.markdown("Execute and view results of specific SQL queries from your MySQL database.")

    if not st.session_state.db_initialized:
        st.error("Database not initialized. Please check your MySQL connection.")
        st.stop()

    # Query options
    options = st.selectbox("Select the Query", (
        "How many food providers and receivers are there in each city",
        "Which type of food provider (restaurant, grocery store, etc.) contributes the most food",
        "What is the contact information of food providers in a specific city",
        "Which receivers have claimed the most food",
        "What is the total quantity of food available from all providers",
        "Which city has the highest number of food listings",
        "What are the most commonly available food types",
        "How many food claims have been made for each food item",
        "Which provider has had the highest number of successful food claims",
        "What percentage of food claims are completed vs. pending vs. canceled",
        "What is the average quantity of food claimed per receiver",
        "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most",
        "What is the total quantity of food donated by each provider",
        "Which food name and food type are most provided",
        "Which status has the highest number of claims"
    ))

    conn = get_mysql_connection()
    if conn is None:
        st.error("Could not connect to MySQL database.")
        st.stop()

    try:
        cursor = conn.cursor()

        if options == "How many food providers and receivers are there in each city":
            query = """
            WITH base AS (
                SELECT
                    COALESCE(p.city, r.city) AS city,
                    IFNULL(p.Providers_count, 0) AS Providers_count,
                    IFNULL(r.receivers_count, 0) AS receivers_count
                FROM
                    (SELECT p.City AS city, COUNT(DISTINCT p.Provider_ID) AS Providers_count FROM providers_data p GROUP BY 1) AS p
                LEFT JOIN
                    (SELECT r.City AS city, COUNT(DISTINCT r.Receiver_ID) AS receivers_count FROM receivers_data r GROUP BY 1) AS r
                ON p.City = r.City

                UNION

                SELECT
                    COALESCE(p.city, r.city) AS city,
                    IFNULL(p.Providers_count, 0) AS Providers_count,
                    IFNULL(r.receivers_count, 0) AS receivers_count
                FROM
                    (SELECT p.City AS city, COUNT(DISTINCT p.Provider_ID) AS Providers_count FROM providers_data p GROUP BY 1) AS p
                RIGHT JOIN
                    (SELECT r.City AS city, COUNT(DISTINCT r.Receiver_ID) AS receivers_count FROM receivers_data r GROUP BY 1) AS r
                ON p.City = r.City
            )
            SELECT DISTINCT *
            FROM base
            ORDER BY Providers_Count DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            df1 = pd.DataFrame(result, columns=["city", "Providers_Count", "Receivers_count"])
            st.dataframe(df1)
        if options=="Which type of food provider (restaurant, grocery store, etc.) contributes the most food":
            query="""
                SELECT provider_Type,sum(Quantity) as provided_quantity from food_listings_data
                group by provider_Type
                order by provided_quantity desc
                limit 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df2 = pd.DataFrame(result, columns=["provider_Type","provided_quantity"])
            st.dataframe(df2)
        if options=="What is the contact information of food providers in a specific city":
            query="""
                SELECT * from providers_data
                where City="Lake Jesusview";
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df3 = pd.DataFrame(result, columns=["provider_id","Name","Type","Address","City","Contact"])
            st.dataframe(df3)
        if options=="Which receivers have claimed the most food":
            query="""
            select r.Name as receiver_name,sum(Quantity)as Food_quantity_claimed,count(c.Claim_ID)as Claim_count
                from claims_data c
                left join receivers_data r on c.receiver_ID=r.receiver_ID
                left join food_listings_data f on c.food_ID=f.food_ID
                where c.Status="Completed"
                group by r.Name
                order by Food_quantity_claimed desc
                limit 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df4 = pd.DataFrame(result, columns=["receiver_name", "Food_quantity", "claim_count"])
            st.dataframe(df4)
        if options=="What is the total quantity of food available from all providers":
            query="""
                with base as (select distinct * from food_listings_data)
                select sum(Quantity) as Total_Quantity from base
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df5 = pd.DataFrame(result, columns=["Total_Quantity"])
            st.dataframe(df5)
        if options=="Which city has the highest number of food listings":
            query="""
                SELECT Location, COUNT(distinct food_ID) as count_listing
            FROM food_listings_data
            GROUP BY Location
            ORDER BY count_listing DESC
            LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df6 = pd.DataFrame(result, columns=["city","count_listing"])
            st.dataframe(df6)
        if options=="What are the most commonly available food types":
            query="""
                SELECT Food_Type,count(distinct Food_ID)as count_food from food_listings_data
                group by Food_Type
                order by count_food desc
                limit 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df7 = pd.DataFrame(result, columns=["city","count"])
            st.dataframe(df7)
        if options=="How many food claims have been made for each food item":
            query="""
                SELECT Food_Name,count(distinct food_id) as Food_count from food_listings_data
                group by Food_Name
                order by Food_count;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df8 = pd.DataFrame(result, columns=["Food_Name","Food_claim_count"])
            st.dataframe(df8)
        if options=="Which provider has had the highest number of successful food claims":
                    query="""
                SELECT Provider_Type,count(distinct claim_id) as successful_claims
                from food_listings_data f join claims_data c on f.food_ID=c.food_ID
                where c.Status="Completed"
                group by Provider_Type
                order by successful_claims desc
                limit 1 ;
            """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    # Convert result into a DataFrame for better readability
                    df9 = pd.DataFrame(result, columns=["Provider_Type","successful_claims"])
                    st.dataframe(df9)
        if options=="What percentage of food claims are completed vs. pending vs. canceled":
            query="""
                SELECT Status,
                (COUNT(distinct claim_id) * 100.0 / (SELECT COUNT(distinct claim_id) FROM claims_data)) AS percentage
            FROM claims_data
            GROUP BY Status;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df10 = pd.DataFrame(result, columns=["Status","percentage"])
            st.dataframe(df10)
        if options=="What is the average quantity of food claimed per receiver":
            query="""
            select sum(Quantity) / count(distinct receiver_id) as average_quantity_per_receiver
            from food_listings_data f join claims_data c on f.food_id = c.food_id  ;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df11 = pd.DataFrame(result, columns=["average_quantity_per_receiver"])
            st.dataframe(df11)
        if options=="Which meal type (breakfast, lunch, dinner, snacks) is claimed the most":
            query="""
                    select Meal_Type, count(distinct claim_id) as count_claims
                    from food_listings_data f
                    join claims_data c on f.food_id = c.food_id
                    where c.Status = 'Completed'
                    group by Meal_Type
                    order by count_claims desc
                    limit 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df12 = pd.DataFrame(result, columns=["Meal_Type","count_meal_type"])
            st.dataframe(df12)
        if options=="What is the total quantity of food donated by each provider":
            query="""
                    select  p.Provider_ID, p.name as provider_name, sum(Quantity) as total_quantity
            from food_listings_data f join providers_data p on f.Provider_ID = p.Provider_ID
            group by p.Provider_ID, p.name;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df13 = pd.DataFrame(result, columns=["provider_id","provider_name","total_quantity"])
            st.dataframe(df13)
        if options=="Which food name and food type are most provided":
            query="""
                    select Food_Name,sum(Quantity) as total_quantity,Food_Type from food_listings_data
                    group by Food_Name,Food_Type
                    order by total_quantity desc
                    limit 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df14 = pd.DataFrame(result, columns=["Food_Name","total_quantity","Food_Type"])
            st.dataframe(df14)
        if options=="Which status has the highest number of claims":
            query=""" 
                    select Status,count(distinct claim_id)as count from claims_data
                    group by Status
                    order by count desc
                    limit 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Convert result into a DataFrame for better readability
            df15 = pd.DataFrame(result, columns=["Status","count"])
            st.dataframe(df15)   

            cursor.close()
            conn.close()
    except Exception as e:
            st.error(f"An error occurred: {e}")
            if conn:
                conn.close()
