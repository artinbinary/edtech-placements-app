# Import streamlit library as st for creating the web application
import streamlit as st
# Import pandas library for data manipulation and analysis
import pandas as pd
# Import random module for generating random numbers and selections
import random
# Import numpy library as np for numerical operations
import numpy as np
# Import plotly.express as px for creating interactive visualizations
import plotly.express as px


# Attempt to import mysql.connector and Error for database operations
try:
    import mysql.connector
    from mysql.connector import Error
    # Set HAS_MYSQL to True if import succeeds
    HAS_MYSQL = True
# Handle ModuleNotFoundError if mysql-connector-python is not installed
except ModuleNotFoundError:
    # Display a warning if mysql-connector-python is not installed
    st.warning("The 'mysql-connector-python' package is not installed. Live DB features disabled.")
    # Set HAS_MYSQL to False
    HAS_MYSQL = False


# Define function to connect to MySQL database
def connect_to_mysql(password):  # Define helper to open a MySQL connection and set session flags on success
    if 'HAS_MYSQL' in globals() and not HAS_MYSQL:  # Skip DB actions when connector isn't installed
        st.warning("MySQL connector not available; skipping DB connection.")
        return None
    db_config = {  # Build connection parameters for MySQL
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': password,
        'database': 'student_db'
    }

    try:
        conn = mysql.connector.connect(**db_config)  # Create a new MySQL connection with provided settings
        if conn.is_connected():  # Verify the connection is active
            st.session_state.db_connected = True  # Mark DB connection as established in session state
            st.session_state.db_config = db_config  # Cache DB config for reuse across queries
            st.success("Login successful!")  # Notify user of successful login
            st.markdown('<hr style="border: .8px solid black; margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)  # Insert a thin horizontal rule for visual separation
            return conn
    except Error as e:  # Gracefully handle database connector errors
        st.error(f"Connection failed: {e}")  # Show DB failure message to the user
        st.session_state.db_connected = False  # Initialize db_connected as False
        return None

    # Try to connect
    try:
        # Establish connection with db_config
        conn = mysql.connector.connect(**db_config)  # Create a new MySQL connection with provided settings
        # Check if connected
        if conn.is_connected():  # Verify the connection is active
            # Set session state db_connected to True
            st.session_state.db_connected = True  # Mark DB connection as established in session state
            # Store db_config in session state
            st.session_state.db_config = db_config  # Cache DB config for reuse across queries
            # Display success message
            st.success("Login successful!")  # Notify user of successful login
            st.markdown('<hr style="border: .8px solid black; margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)  # Insert a thin horizontal rule for visual separation
            # Return the connection
            return conn
    # Handle Error exception
    except Error as e:  # Gracefully handle database connector errors
        # Display error message
        st.error(f"Connection failed: {e}")  # Show DB failure message to the user
        # Set db_connected to False
        st.session_state.db_connected = False  # Initialize db_connected as False
        # Return None
        return None

# ___________________________________________ #

# Set Streamlit page configuration for title, icon, and layout
st.set_page_config(  # Configure Streamlit page (title, icon, layout)
    page_title="Guvi Placements Portal",
    page_icon="🎓",
    layout="wide"
)
# Display a markdown header for the portal welcome message
st.markdown("<h1 class='main-header-small'>Welcome to Guvi Placements Portal</h1>", unsafe_allow_html=True)  # Render main header using HTML for precise styling

# Inject custom CSS styling for the application
st.markdown(""" 
<style>

    .stApp, .main .block-container {
        background-color: white !important;
        color: black !important;
        text-align: left !important;
    }

    .main-header {
        color: black !important;
        font-size: 2rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: left !important;
    }

    .section-header {
        color: black !important;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    label,
    div[data-testid="stPassword"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] {
        color: black !important;
    }

    .stTextInput > div > div > input {
        background-color: #bcd5b0 !important;
        color: black !important;
        border: .1px solid #808000 !important;
    }

    .stButton > button {
        background-color: #bcd5b0 !important;
        color: black !important;
        border: 1px solid #808000 !important;
    }

    .stButton > button:hover {
        background-color: #a8c89a !important;
        color: black !important;
    }

    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        color: white !important;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown strong {
        color: black !important;
        text-align: left !important;
    }

    .section-separator {
        border-bottom: 1px solid black;
        margin: 20px 0;
    }

    div[data-testid="stAlert"] {
        background-color: #c6d9ed !important;  /* pastel blue background */
        color: black !important;
        border: 1px solid #6c89a0 !important;
        border-radius: 3px !important;
        padding: 0.4rem !important;
        font-size: 0.8rem !important;
    }        

    /* Target only the success alert for 'login successful' */
    div[data-testid="stAlert"]:has(+ div:contains("login successful")) {
        background-color: #c6d9ed !important; /* Pastel blue */
        color: black !important;
        border: 1px solid #6c89a0 !important;
        border-radius: 3px !important;
        padding: 0.4rem !important;
        font-size: 0.8rem !important;
        margin-top: 1.5rem !important; /* Add spacing above */
        position: relative;
        z-index: 10; /* Ensure it stays above */
    }

    /* Fallback for older browsers or Streamlit versions */
    div[data-testid="stAlert"] {
        background-color: #c6d9ed !important; /* Default for all alerts */
        color: black !important;
        border: 1px solid #6c89a0 !important;
        border-radius: 3px !important;
        padding: 0.4rem !important;
        font-size: 0.8rem !important;
    }

    .mysql-table {
        background-color: #2e2e2e !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 12px !important;
        border-radius: 5px;
        padding: 8px;
        margin: 15px 0;
        overflow-x: auto;
    }

    .mysql-table table {
        width: 100%;
        border-collapse: collapse;
    }

    .mysql-table th {
        background-color: #404040 !important;
        color: #ffffff !important;
        font-weight: bold;
        border: 1px solid #666666 !important;
        padding: 8px !important;
        text-align: left;
    }

    .mysql-table td {
        background-color: #2e2e2e !important;
        color: #ffffff !important;
        border: 1px solid #666666 !important;
        padding: 8px !important;
    }

    .mysql-table tr:nth-child(even) td {
        background-color: #333333 !important;
    }

    .mysql-table-container {
        max-height: 480px;
        overflow-y: auto;
        background-color: #1b1b1b !important; 
        border: 1px solid #444444 !important;
        border-radius: 8px;
        padding: 6px;
    }

    .mysql-table thead th {
        position: sticky;
        top: 0;
        z-index: 2;
    }

    div[data-testid="stDownloadButton"] button {
        background-color: #D9DDDC !important; 
        color: black !important;
    }

</style>
""", unsafe_allow_html=True)

# ___________________________________________ #

# Initialize session state for db_connected if not present
if 'db_connected' not in st.session_state:  # Ensure db_connected key exists in session state
    st.session_state.db_connected = False  # Initialize db_connected as False
# Initialize session state for db_config if not present
if 'db_config' not in st.session_state:  # Ensure db_config key exists
    st.session_state.db_config = None  # Initialize DB config placeholder
# Initialize session state for custom_visible_rows if not present
if 'custom_visible_rows' not in st.session_state:  # Ensure pagination size key for custom view exists
    st.session_state.custom_visible_rows = 10  # Reset pagination for custom view
# Initialize session state for insights_visible_rows if not present
if 'insights_visible_rows' not in st.session_state:  # Ensure pagination size key for insights exists
    st.session_state.insights_visible_rows = 10
# Initialize session state for search_visible_rows if not present
if 'search_visible_rows' not in st.session_state:  # Ensure pagination size key for search exists
    st.session_state.search_visible_rows = 10  # Reset pagination for the search results
# Initialize session state for selected_query if not present
if 'selected_query' not in st.session_state:  # Ensure selected_query key exists
    st.session_state.selected_query = None
# Initialize session state for current_result if not present
if 'current_result' not in st.session_state:  # Ensure current_result DataFrame exists
    st.session_state.current_result = pd.DataFrame()
# Initialize session state for current_insight if not present
if 'current_insight' not in st.session_state:  # Ensure current_insight DataFrame exists
    st.session_state.current_insight = pd.DataFrame()
# Initialize session state for search_result if not present
if 'search_result' not in st.session_state:  # Ensure search_result DataFrame exists
    st.session_state.search_result = pd.DataFrame()
# Initialize session state for custom_columns if not present
if 'custom_columns' not in st.session_state:  # Ensure per-section selected columns cache exists
    st.session_state.custom_columns = {'students': [], 'placements': [], 'programming': [], 'soft_skills': []}

# ___________________________________________ #
# Define function to execute SQL query
def execute_sql_query(query, params=None):  # Execute a SQL query and return results as a DataFrame
    # Check if connected and config exists
    if not st.session_state.db_connected or not st.session_state.db_config:  # Guard: return empty results if not authenticated to DB
        # Return empty DataFrame if not
        return pd.DataFrame()
    # Try to execute
    try:
        # Connect using config
        conn = mysql.connector.connect(**st.session_state.db_config)  # Create a new MySQL connection with provided settings
        # Read query into DataFrame with parameters
        df = pd.read_sql(query, conn, params=params)  # Run the SQL against MySQL and load the result into a DataFrame
        # Close connection
        conn.close()  # Close the temporary connection handle
        # Replace None with empty string
        return df.replace({None: ''})  # Normalize None values to empty strings for cleaner display
    # Handle Error
    except Error as e:  # Gracefully handle database connector errors
        # Display error
        st.error(f"Query failed: {e}")
        # Return empty DataFrame
        return pd.DataFrame()
# ___________________________________________ #

# Define function to get columns from table
def get_table_columns(table_name):  # Return the list of columns for a given table
    # If connected, query columns
    if st.session_state.db_connected:  # Use live MySQL search when connected
        query = f"SHOW COLUMNS FROM {table_name}"  # Use MySQL metadata query to fetch column names
        columns_df = execute_sql_query(query)
        # Return list of Field names
        return [row['Field'] for _, row in columns_df.iterrows()]
    # Return empty list if not connected
    return []
# ___________________________________________ #

# Define utility function to get DataFrame from session state
def _get_state_df(key: str) -> pd.DataFrame:  # Utility: fetch a DataFrame from session safely
    # Get value from session state or empty DataFrame
    val = st.session_state.get(key, pd.DataFrame())
    # Return if DataFrame, else empty
    return val if isinstance(val, pd.DataFrame) else pd.DataFrame()  # If stored value isn't a DataFrame, fall back to an empty one

# ___________________________________________ #

# Define function to display DataFrame in MySQL style
def display_mysql_table(df, visible_rows_key, section_title):  # Render a DataFrame styled like a MySQL Workbench table
    # Check if DataFrame is empty
    if df.empty:  # Early exit when there's nothing to show
        # Display warning
        st.warning(f"No results found for {section_title}.")
        # Return
        return

    # Display sort header
    st.markdown(f"**Sort {section_title}**")  # Add a small sort header above the table

    # Create columns for sort controls (equal widths for balance)
    sort_col, sort_dir = st.columns([3, 1])  # Layout: place sort column and direction controls side by side

    with sort_col:
        sort_column = st.selectbox(
            "Sort By", 
            [""] + list(df.columns), 
            key=f"{visible_rows_key}_sort_col"
        )

    with sort_dir:
        sort_direction = st.radio(
            "Direction",  # 👈 Native label (this keeps it directly above the options)
            ["Ascending", "Descending"],
            index=0 if st.session_state.get(f"{visible_rows_key}_sort_dir", "Ascending") == "Ascending" else 1,
            key=f"{visible_rows_key}_sort_dir"
        )

    # Apply sort if column selected
    if sort_column and sort_column != "":
        df = df.sort_values(by=sort_column, ascending=(sort_direction == "Ascending"))  # Apply sorting to the DataFrame

    # Get visible portion of DataFrame
    visible_df = df.head(st.session_state[visible_rows_key])  # Paginate by showing only the first N rows

    # Convert to HTML with class
    html_table = visible_df.to_html(index=False, classes="mysql-table", escape=False)  # Convert visible rows to HTML table with MySQL-like CSS classes
    # Display in container
    st.markdown(f'<div class="mysql-table-container">{html_table}</div>', unsafe_allow_html=True)

    # If more rows, show button
    if len(df) > st.session_state[visible_rows_key]:
        if st.button("Show More", key=f"{visible_rows_key}_show_more"):  # Button to increase page size
            # Increment visible rows
            st.session_state[visible_rows_key] += 10  # Increment the visible row count by 10
            # Rerun app
            st.rerun()  # Trigger a rerun so the UI reflects the new page size

    # Generate CSV
    csv = df.to_csv(index=False)  # Create a CSV download of the (sorted) result
    # Display download button
    st.download_button(  # Provide a button to download the CSV
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"guvi_placements_{section_title.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

# ___________________________________________ #

# Define main function
def main():  # Entry point for assembling the app UI and behavior

    # Handle MySQL connection if not connected
    if not st.session_state.db_connected:  # If not logged in to DB, prompt for credentials
        # Input for password
        password = st.text_input("Enter your password", type="password", key="mysql_password")  # Password input field for MySQL
        if password:
            # Spinner for connecting
            with st.spinner("Connecting to MySQL..."):  # Show a spinner while attempting DB connection
                # Attempt connection
                conn = connect_to_mysql(password)  # Try to connect using the provided password
                if conn:
                    # Close connection
                    conn.close()  # Close the temporary connection handle
                    # Load DataFrames from tables
                    st.session_state.df_students = execute_sql_query("SELECT * FROM Students")  # Load Students table into session after login
                    st.session_state.df_programming = execute_sql_query("SELECT * FROM Programming")  # Load Programming table into session
                    st.session_state.df_soft_skills = execute_sql_query("SELECT * FROM Soft_Skills")  # Load Soft_Skills table into session
                    st.session_state.df_placements = execute_sql_query("SELECT * FROM Placements")  # Load Placements table into session
                else:
                    # Warning for fallback
                    st.warning("Using sample data due to connection failure.")  # Inform the user that fallback sample data will be used
                    # Generate sample data
                    st.session_state.df_students, st.session_state.df_programming, \
                    st.session_state.df_soft_skills, st.session_state.df_placements = generate_sample_data()  # Populate sample DataFrames to keep the app usable offline

    # ___________________________________________ #
    # Get DataFrames from session state
    df_students = st.session_state.get('df_students', pd.DataFrame())  # Fetch Students data (session or default empty)
    df_programming = st.session_state.get('df_programming', pd.DataFrame())  # Fetch Programming data (session or default empty)
    df_soft_skills = st.session_state.get('df_soft_skills', pd.DataFrame())  # Fetch Soft_Skills data (session or default empty)
    df_placements = st.session_state.get('df_placements', pd.DataFrame())  # Fetch Placements data (session or default empty)
   # ___________________________________________ #

    # Keyword Search Section
    st.markdown('<div class="section-header">Search</div>', unsafe_allow_html=True)  # Section: keyword search across joined tables
    search_criteria = st.text_input(  # Textbox to enter comma-separated keywords; Enter key triggers search
        "", 
        placeholder="Enter keywords (e.g., Chennai, placed, python)", 
        key="search_input", 
        label_visibility="collapsed",
        on_change=lambda: st.session_state.update({"search_trigger": True})  # 👈 enables Enter key
    )
    # Ensure dataframes are available
    if 'df_students' not in st.session_state or st.session_state.df_students.empty:  # If not logged in yet, show a friendly callout instead of search UI
        st.markdown(
            """
            <div style='background-color: #c6d9ed; padding: .4rem; border-radius: 8px; border: 1px solid #6c89a0;'>
                <span style='font-size: 1rem; color: black;'>Login to access details.</span>
            </div>
            """, 
            unsafe_allow_html=True
        )      
    else:
        if st.button("Search", key="search_button") or st.session_state.get('search_trigger', False):  # Create a Search button or trigger search if 'search_trigger' is True  # Click to run search (or auto-run on Enter)
            st.session_state["search_trigger"] = False   # Reset the Enter-key trigger flag
            if not search_criteria:  # Validate that the user typed something
                st.warning("Please enter a search keyword.")  # Display a warning if no keyword is entered
            else:
                with st.spinner("Searching..."):  # Show a spinning loader during the search process  # Show a spinner while building and running the search
                    if st.session_state.db_connected:  # Check if the database is connected  # Use live MySQL search when connected
                        keywords = [k.strip().lower() for k in search_criteria.split(',') if k.strip()]  # Split search criteria by comma, strip whitespace, convert to lowercase  # Normalize keywords: split by comma, trim, lowercase
                        if not keywords:
                            st.warning("Please enter valid search keywords.")  # Display a warning if no valid keywords
                        else:
                            # Define all columns from all tables with correct aliases
                            all_columns = {  # Lookup all column names for each table alias
                                's': get_table_columns('Students'),
                                'pr': get_table_columns('Programming'),
                                'ss': get_table_columns('Soft_Skills'),
                                'p': get_table_columns('Placements')
                            }
                            flat_columns = [col for sublist in all_columns.values() for col in sublist]  # Flatten the list of all columns across tables  # Flatten list of all column names for iteration

                            # Default columns to always include in specified order
                            default_cols = ['s.Name', 's.Student_ID', 's.Course_Batch', 'p.Placement_Status']  # Columns that always appear first in search results
                            # Select all columns initially for full search, prioritizing s.Student_ID
                            all_select_cols = ['s.Student_ID'] + [f'{table}.{col}' for table, cols in all_columns.items() for col in cols if col != 'Student_ID']  # Build the full SELECT column list (Student_ID first)

                            # Base query with all columns and named placeholders
                            base_query = """
                            SELECT {select_cols}
                            FROM Students s
                            LEFT JOIN Programming pr ON s.Student_ID = pr.Student_ID
                            LEFT JOIN Soft_Skills ss ON s.Student_ID = ss.Student_ID
                            LEFT JOIN Placements p ON s.Student_ID = p.Student_ID
                            WHERE {where_clause}
                            """

                            conditions = []  # Accumulate WHERE clause parts here
                            params = []
                            # Separate column name keywords from value-based keywords
                            col_name_keywords = [k for k in keywords if k in flat_columns or any(k in col.lower() for col in flat_columns)]  # Separate keywords that look like column names
                            value_keywords = [k for k in keywords if k not in col_name_keywords]  # Remaining keywords treated as search terms for values

                            if value_keywords:  # When value terms are present, search across all columns
                                # Build AND condition for value-based keywords
                                for keyword in value_keywords:
                                    keyword_condition = " OR ".join(  # Build OR across all columns for one keyword
                                        f"LOWER({table}.{col}) LIKE %s"
                                        for table, cols in all_columns.items()
                                        for col in cols
                                    )
                                    conditions.append(f"({keyword_condition})")  # Add per-keyword OR group to WHERE
                                    params.extend([f"%{keyword}%"] * len(flat_columns))  # Supply parameterized LIKE patterns for safety
                                where_clause = " AND ".join(conditions) if conditions else "1=1"  # Combine per-keyword groups with AND
                            else:  # If no value keywords, match all rows
                                where_clause = "1=1"  # No value-based conditions, match all rows

                            final_query = base_query.format(select_cols=', '.join(all_select_cols), where_clause=where_clause)  # Render the final SQL with columns and WHERE

                            # Debug: Print the final query to verify
                            # st.write("Debug Query:", final_query, params)

                            try:
                                result = execute_sql_query(final_query, params) if params else execute_sql_query(final_query)  # Execute parameterized search query
                                if not result.empty:  # Handle non-empty results
                                    # Identify columns containing each keyword in the full result set with partial matching
                                    matching_cols = set(col_name_keywords)  # Start with column name keywords  # Start with any columns named directly by the user
                                    for keyword in value_keywords:
                                        for col in result.columns:
                                            # Robust check for partial keyword presence in column values
                                            if any(keyword in str(value).lower() for value in result[col].dropna()):
                                                matching_cols.add(col.split('.')[-1])  # Add column name without alias
                                    # Special handling for common partial matches
                                    if any(k in ('internship', 'internships') for k in keywords):
                                        matching_cols.add('Internships_Completed')  # Special-case common synonyms to expected columns
                                    if 'certification' in ' '.join(keywords):
                                        matching_cols.add('Certifications_Earned')  # Include certification-related columns when asked
                                    if 'mock' in ' '.join(keywords):
                                        matching_cols.add('Mock_Interview_Score')  # Ensure interview-related columns are present
                                    if 'interview' in ' '.join(keywords):
                                        matching_cols.add('Mock_Interview_Score')  # Ensure interview-related columns are present
                                    # Combine default and matching columns, enforcing specified order and validating against result columns
                                    final_cols = ['Name', 'Student_ID', 'Course_Batch', 'Placement_Status']  # Compose final visible columns (defaults first)
                                    matching_cols = matching_cols.intersection(set(result.columns))  # Only keep columns that exist  # Keep only columns that truly exist in result
                                    final_cols.extend(list(matching_cols - {'Name', 'Student_ID', 'Course_Batch', 'Placement_Status'}))
                                    st.session_state.search_result = result[final_cols]  # Store slimmed result in session for display
                                    if st.session_state.search_result.empty:
                                        st.write("No results for your search criteria. Try a different search?")
                                    else:
                                        st.session_state.search_visible_rows = 10  # Reset pagination for the search results
                                else:
                                    st.write("No results for your search criteria. Try a different search?")
                            except Exception as e:
                                st.error(f"Search failed: {str(e)}")  # Display error for debugging  # Show any search error and clear results
                                st.session_state.search_result = pd.DataFrame()
                    else:  # If offline, run the same search logic on sample DataFrames
                        # Fallback to sample data
                        df_students = st.session_state.df_students
                        df_programming = st.session_state.df_programming
                        df_soft_skills = st.session_state.df_soft_skills
                        df_placements = st.session_state.df_placements
                        result = search_sample_data(search_criteria, df_students, df_programming, df_soft_skills, df_placements)  # Use a helper to search across sample data tables
                        if not result.empty:  # Handle non-empty results
                            default_cols = ['Name', 'Student_ID', 'Course_Batch', 'Placement_Status']
                            # Include columns where any keyword is found in the full sample data
                            matching_cols = set()
                            for keyword in keywords:
                                for col in result.columns:
                                    if col not in default_cols and any(keyword in str(value).lower() for value in result[col].dropna()):
                                        matching_cols.add(col)
                            # Special handling for common partial matches
                            if any(k in ('internship', 'internships') for k in keywords):
                                matching_cols.add('Internships_Completed')  # Special-case common synonyms to expected columns
                            if 'certification' in ' '.join(keywords):
                                matching_cols.add('Certifications_Earned')  # Include certification-related columns when asked
                            if 'mock' in ' '.join(keywords):
                                matching_cols.add('Mock_Interview_Score')  # Ensure interview-related columns are present
                            if 'interview' in ' '.join(keywords):
                                matching_cols.add('Mock_Interview_Score')  # Ensure interview-related columns are present
                            result = result[default_cols + list(matching_cols - set(default_cols))]
                            st.session_state.search_result = result
                            if st.session_state.search_result.empty:
                                st.write("No results for your search criteria. Try a different search?")
                            else:
                                st.session_state.search_visible_rows = 10  # Reset pagination for the search results
                        else:
                            st.write("No results for your search criteria. Try a different search?")

            st.session_state.search_trigger = False

    if 'search_result' in st.session_state and not st.session_state.search_result.empty:
        display_mysql_table(st.session_state.search_result, 'search_visible_rows', 'Search Results')  # Render the search results with MySQL-themed table

    # Separator to ensure other sections appear
    st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)  # Horizontal separator to visually split sections

    # _____________________________________________ #

    # Display custom view header
    st.markdown('<div class="section-header">Custom View</div>', unsafe_allow_html=True)  # Section: choose arbitrary columns to view

    # Get columns for students
    students_cols = get_table_columns('Students') if st.session_state.db_connected else [  # Fallback column list for Students when not connected
        "Student_ID", "Name", "Age", "Gender", "Email", "Phone", "Enrollment_Year", 
        "Course_Batch", "City", "Graduation_Year"
    ]
    # Get columns for placements
    placements_cols = get_table_columns('Placements') if st.session_state.db_connected else [  # Fallback column list for Placements when not connected
        "Student_ID", "Mock_Interview_Score", "Internships_Completed", "Company_Name", 
        "Placement_Package", "Interview_Rounds_Cleared", "Placement_Date", "Placement_Status"
    ]
    # Get columns for programming
    programming_cols = get_table_columns('Programming') if st.session_state.db_connected else [  # Fallback column list for Programming when not connected
        "Programming_ID", "Student_ID", "Language", "Problems_Solved", "Assessments_Completed", 
        "Mini_Projects", "Certifications_Earned", "Latest_Project_Score"
    ]
    # Get columns for soft_skills
    soft_skills_cols = get_table_columns('Soft_Skills') if st.session_state.db_connected else [  # Fallback column list for Soft_Skills when not connected
        "Soft_Skills_ID", "Student_ID", "Communication_Score", "Teamwork_Score", 
        "Presentation_Score", "Leadership_Score", "Critical_Thinking", "Interpersonal_Skills"
    ]

    # Create four columns for filters
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)  # Layout: 4 equal-width columns for filter pickers

    # In first column, student details
    with filter_col1:  # Left column: student attribute picker
        st.markdown("**Student Details**")
        # Multiselect for students columns
        student_filter = st.multiselect("", students_cols, key="student_filter", default=st.session_state.custom_columns['students'])  # Multi-select list of student columns
        # Update session state
        st.session_state.custom_columns['students'] = student_filter  # Persist student column selection in session

    # In second column, placement status
    with filter_col2:  # Second column: placement fields picker
        st.markdown("**Placement Status**")
        # Multiselect for placements columns
        placement_filter = st.multiselect("", placements_cols, key="placement_filter", default=st.session_state.custom_columns['placements'])  # Multi-select placement columns
        # Update session state
        st.session_state.custom_columns['placements'] = placement_filter  # Persist placement column selection in session

    # In third column, programming
    with filter_col3:  # Third column: programming fields picker
        st.markdown("**Programming**")
        # Multiselect for programming columns
        programming_filter = st.multiselect("", programming_cols, key="programming_filter", default=st.session_state.custom_columns['programming'])  # Multi-select programming columns
        # Update session state
        st.session_state.custom_columns['programming'] = programming_filter  # Persist programming column selection in session

    # In fourth column, soft skills
    with filter_col4:  # Fourth column: soft-skill fields picker
        st.markdown("**Soft Skills**")
        # Multiselect for soft skills columns
        soft_skills_filter = st.multiselect("", soft_skills_cols, key="soft_skills_filter", default=st.session_state.custom_columns['soft_skills'])  # Multi-select soft-skill columns
        # Update session state
        st.session_state.custom_columns['soft_skills'] = soft_skills_filter  # Persist soft-skill column selection in session

    # Button to apply filters
    if st.button("Apply Filters", key="apply_filters"):  # Generate a joined query based on chosen columns
        # Check if any columns selected
        if not (student_filter or placement_filter or programming_filter or soft_skills_filter):  # Block empty runs—require at least one column
            # Warning if none
            st.warning("Please select at least one column.")
        else:
            # Initialize selected columns list
            selected_columns = []  # Collect fully qualified column names here
            # Initialize tables list
            tables = []  # Track which tables must be joined
            # If student filter, add columns and table
            if student_filter:
                selected_columns.extend([f"s.{col}" for col in student_filter])  # Add chosen Student columns (aliased as s)
                tables.append("Students s")  # Include Students as the base table
            # If placement filter, add columns and table
            if placement_filter:
                selected_columns.extend([f"p.{col}" for col in placement_filter if col != "Student_ID"])  # Add chosen Placement columns (aliased as p)
                tables.append("Placements p")  # Include Placements join target
            # If programming filter, add columns and table
            if programming_filter:
                selected_columns.extend([f"pr.{col}" for col in programming_filter if col != "Student_ID"])  # Add chosen Programming columns (aliased as pr)
                tables.append("Programming pr")  # Include Programming join target
            # If soft skills filter, add columns and table
            if soft_skills_filter:
                selected_columns.extend([f"ss.{col}" for col in soft_skills_filter if col != "Student_ID"])  # Add chosen Soft_Skills columns (aliased as ss)
                tables.append("Soft_Skills ss")  # Include Soft_Skills join target

            # Ensure Student_ID included
            if "s.Student_ID" not in selected_columns:  # Ensure primary key is present for joining/results
                selected_columns.insert(0, "s.Student_ID")

            # Build base query
            query = f"SELECT {', '.join(selected_columns)} FROM {tables[0]}"  # Start SELECT with the base table
            # Add joins if multiple tables
            if len(tables) > 1:  # Append JOINs when more than one table is selected
                query += " " + " ".join([f"JOIN {t} ON s.Student_ID = {t.split()[1]}.Student_ID" for t in tables[1:]])  # Join each extra table on Student_ID

            # Execute query
            result = execute_sql_query(query)  # Run the dynamically constructed query
            # If not empty, store in session
            if not result.empty:  # Handle non-empty results
                st.session_state.custom_result = result  # Cache result for rendering and pagination
                st.session_state.custom_visible_rows = 10  # Reset pagination for custom view

    # If custom_result not empty, display
    if not _get_state_df('custom_result').empty:  # Render custom view if there is data
        # Separator
        st.markdown("---")
        # Subheader
        st.subheader("📈 Custom View Results")  # Label the results section with an icon
        # Display table
        display_mysql_table(st.session_state.custom_result, 'custom_visible_rows', 'Custom View')  # Render custom result set with consistent styling

    # Display separator
    st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)  # Horizontal separator to visually split sections

    # ___________________________________________ #

    # Display insights header
    st.markdown('<div class="section-header">Actionable Insights</div>', unsafe_allow_html=True)  # Section: prebuilt SQL insights over the data

    # Define insight options list
    insight_options = [  # Menu choices for insights (display text)
        {"id": 1, "logic": "List 'Ready' students with mock interview scores and internships."},
        {"id": 2, "logic": "Show 'Ready' students with all skills, scores, and academic details."},
        {"id": 3, "logic": "Rank 'Ready' students by mock interview scores with full profiles."},
        {"id": 4, "logic": "Find 'Ready' students skilled in Python, PyTorch, Mistral, or Llama for AI roles."},
        {"id": 5, "logic": "List 'Ready' students with strong coding skills (mini projects > 5) for coding tests."},
        {"id": 6, "logic": "Identify 'Ready' students with high soft skills for techno-functional roles."},
        {"id": 7, "logic": "Find 'Ready' students with low soft skills (40-70) but high technical scores."},
        {"id": 8, "logic": "Count 'Ready' students by city to target local companies."},
        {"id": 9, "logic": "List 2024-2025 graduates who are 'Ready,' ranked by mock interview scores."},
        {"id": 10, "logic": "Analyze success factors (scores, certifications, internships) for placed students."}
    ]

    # If connected
    if st.session_state.get('db_connected', False):  # Show insights only after successful login
        # Create opts list (not used)
        opts = [f"{o['id']}. {o['logic']}" for o in insight_options]
        # Selectbox for insight
        choice = st.selectbox("Select an insight", options=[o['id'] for o in insight_options],  # Dropdown to pick which insight to run
                            format_func=lambda i: f"{i}. {insight_options[i-1]['logic']}",
                            key="insight_select")
        # Button to run insight
        if st.button("Run Insight", key="run_insight_button"):
            # Get SQL from dict
            sql = sql_queries.get(choice, "")  # Map choice to its underlying SQL
            if sql:
                # Spinner
                with st.spinner("Running insight..."):
                    # Execute
                    res = execute_sql_query(sql)  # Execute the selected insight query
                    # If not empty, store
                    if not res.empty:
                        st.session_state.current_insight = res  # Persist insight results for rendering
                        st.session_state.insights_visible_rows = 10
                    else:
                        # Empty and warning
                        st.session_state.current_insight = pd.DataFrame()
                        st.warning("No rows returned for this insight.")  # Inform user when insight returns nothing
    else:  # When logged out, show an info card instead
        # Info if not connected
        st.markdown(
            """
            <div style='background-color: #c6d9ed; padding: 1rem; border-radius: 12px; border: 1px solid #6c89a0;'>
                <span style='font-size: 1.1rem; color: black;'>Login to access insights.</span>
            </div>
            """,
            unsafe_allow_html=True
        )


    # If current_insight not empty, display
    if not _get_state_df('current_insight').empty:  # Render insight results if available
        display_mysql_table(st.session_state.current_insight, 'insights_visible_rows', 'Insights')  # Render insights table with pagination and download

# ___________________________________________ #

# Define insight_options again (duplicate)
insight_options = [  # Re-declare insight options (duplicated)
    {"id": 1, "logic": "List 'Ready' students with mock interview scores and internships."},
    {"id": 2, "logic": "Show 'Ready' students with skills, scores, and academic details."},
    {"id": 3, "logic": "Rank 'Ready' students by mock interview scores with tech context."},
    {"id": 4, "logic": "Find 'Ready' students skilled in Python/PyTorch/Llama for AI roles."},
    {"id": 5, "logic": "List 'Ready' students with strong coding (mini projects > 5)."},
    {"id": 6, "logic": "Identify 'Ready' students with high soft skills."},
    {"id": 7, "logic": "Find 'Ready' students with soft skills in 40–70 and high technical scores."},
    {"id": 8, "logic": "Count 'Ready' students by city."},
    {"id": 9, "logic": "List 2024–2025 'Ready' graduates by mock interview scores."},
    {"id": 10, "logic": "Analyze success factors (scores, certs, internships) for placed/ready."}
]
# ___________________________________________ #

# Define dict of SQL queries for insights
sql_queries = {
    1: """
    SELECT s.Student_ID, s.Name, s.Email, p.Mock_Interview_Score, p.Internships_Completed, p.Placement_Status
    FROM Students s
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready';
    """,
    2: """
    SELECT s.Student_ID, s.Name, s.Graduation_Year, s.City, pr.Language, pr.Problems_Solved,
           pr.Assessments_Completed, pr.Mini_Projects, pr.Certifications_Earned, pr.Latest_Project_Score,
           ss.Communication_Score, ss.Teamwork_Score, ss.Presentation_Score, ss.Leadership_Score,
           ss.Critical_Thinking, ss.Interpersonal_Skills, p.Mock_Interview_Score
    FROM Students s
    JOIN Programming pr ON s.Student_ID = pr.Student_ID
    JOIN Soft_Skills ss ON s.Student_ID = ss.Student_ID
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready';
    """,
    3: """
    SELECT s.Student_ID, s.Name, p.Mock_Interview_Score, p.Placement_Status,
           COALESCE(pr.Problems_Solved,0) AS Problems_Solved, COALESCE(pr.Latest_Project_Score,0) AS Latest_Project_Score
    FROM Students s
    JOIN Placements p ON s.Student_ID = p.Student_ID
    LEFT JOIN Programming pr ON s.Student_ID = pr.Student_ID
    WHERE p.Placement_Status = 'Ready'
    ORDER BY p.Mock_Interview_Score DESC;
    """,
    4: """
    SELECT s.Student_ID, s.Name, s.City, s.Graduation_Year, pr.Language, p.Placement_Status
    FROM Students s
    JOIN Programming pr ON s.Student_ID = pr.Student_ID
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready' AND
          (pr.Language LIKE '%Python%' OR pr.Language LIKE '%PyTorch%' OR pr.Language LIKE '%Llama%');
    """,
    5: """
    SELECT s.Student_ID, s.Name, pr.Problems_Solved, pr.Mini_Projects, p.Placement_Status
    FROM Students s
    JOIN Programming pr ON s.Student_ID = pr.Student_ID
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready' AND pr.Mini_Projects > 5
    ORDER BY pr.Problems_Solved DESC;
    """,
    6: """
    SELECT s.Student_ID, s.Name,
           (ss.Communication_Score + ss.Teamwork_Score + ss.Presentation_Score +
            ss.Leadership_Score + ss.Critical_Thinking + ss.Interpersonal_Skills)/6.0 AS Avg_Soft_Skills,
           p.Placement_Status
    FROM Students s
    JOIN Soft_Skills ss ON s.Student_ID = ss.Student_ID
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready'
    ORDER BY Avg_Soft_Skills DESC;
    """,
    7: """
    SELECT s.Student_ID, s.Name,
           (ss.Communication_Score + ss.Teamwork_Score + ss.Presentation_Score +
            ss.Leadership_Score + ss.Critical_Thinking + ss.Interpersonal_Skills)/6.0 AS Avg_Soft_Skills,
           COALESCE(pr.Problems_Solved,0) AS Problems_Solved, COALESCE(pr.Assessments_Completed,0) AS Assessments_Completed,
           p.Placement_Status
    FROM Students s
    JOIN Soft_Skills ss ON s.Student_ID = ss.Student_ID
    LEFT JOIN Programming pr ON s.Student_ID = pr.Student_ID
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready' AND
          (ss.Communication_Score + ss.Teamwork_Score + ss.Presentation_Score +
           ss.Leadership_Score + ss.Critical_Thinking + ss.Interpersonal_Skills)/6.0 BETWEEN 40 AND 70
    ORDER BY Problems_Solved DESC, Assessments_Completed DESC;
    """,
    8: """
    SELECT s.City, COUNT(*) AS Ready_Students_Count
    FROM Students s
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status = 'Ready'
    GROUP BY s.City
    ORDER BY Ready_Students_Count DESC
    LIMIT 1;
    """,
    9: """
    SELECT s.Name, s.Student_ID, s.City AS Location, s.Graduation_Year, p.Placement_Status,
           p.Mock_Interview_Score
    FROM Students s
    JOIN Placements p ON s.Student_ID = p.Student_ID
    JOIN Programming pr ON s.Student_ID = pr.Student_ID
    WHERE s.Graduation_Year IN (2024, 2025) AND p.Placement_Status = 'Ready'
    ORDER BY p.Mock_Interview_Score DESC;
    """,
    10: """
    SELECT s.Student_ID, s.Name,
           (ss.Communication_Score + ss.Teamwork_Score + ss.Presentation_Score +
            ss.Leadership_Score + ss.Critical_Thinking + ss.Interpersonal_Skills)/6.0 AS Avg_Soft_Skills,
           pr.Certifications_Earned, COALESCE(p.Internships_Completed,0) AS Internships_Completed,
           COALESCE(p.Mock_Interview_Score,0) AS Mock_Interview_Score,
           COALESCE(pr.Latest_Project_Score,0) AS Latest_Project_Score, p.Placement_Status
    FROM Students s
    JOIN Soft_Skills ss ON s.Student_ID = ss.Student_ID
    LEFT JOIN Programming pr ON s.Student_ID = pr.Student_ID
    JOIN Placements p ON s.Student_ID = p.Student_ID
    WHERE p.Placement_Status IN ('Ready','Placed');
    """
}

# Call main function to run the app
main()  # Run the app

# ___________________________________________ #
