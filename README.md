Know About Disaster

•	Objective:
The project aims to develop a web application that enhances disaster preparedness and response. The application will address challenges such as limited access to reliable information, insufficient education on disaster response, and fragmented communication channels by providing a platform where users can access disaster information, report local disasters, and receive notifications.

•	Technologies Used:
-	HTML
-	CSS
-	JavaScript
-	Flask (Python)
-	Gemini LLM API
-	Geolocation API
-	Excel Sheets (for data storage)

•	Features and Functionality

-	User Authentication

-	Registration:
-	Users can create a new account by providing necessary details such as username, email, and password.
-	Passwords are stored securely (note: hashing passwords is recommended for security).

-	Login:
-	Users can log in using their credentials.
-	After successful authentication, users are redirected to the main dashboard.

-	Main Dashboard Layout

•	The dashboard is divided into three main sections:

-	Left Section: Know More About Natural Disasters
-	Displays a list of natural disasters in containers (e.g., hurricanes, earthquakes, floods, wildfires).
-	Each disaster name is clickable and opens a popup box with detailed information and a chatbox for interaction.

-	Center Section: User Geolocation and Reporting
-	Displays a welcome message ("Hello, User") and prompts users to upload their geolocation if they are in an area affected by a disaster.
-	Users can click a button to automatically obtain their latitude and longitude using the Geolocation API.
-	Users are required to input the disaster type and submit it.

-	Right Section: Notifications
-	Displays a list of current disasters reported by users.
-	Each notification includes details such as disaster type, date, time, location, and the username of the uploader.

-	Disaster Information and Chatbox

-	Popup Box:
-	Opens when a user clicks on a disaster name in the left section.
-	Provides a title, brief description, and a chatbox for users to interact with the Gemini LLM API.

-	Chatbox:
-	Integrated with Gemini LLM API.
-	Allows users to ask questions and get information about the selected disaster.

-	Geolocation and Reporting

-	Get Location Button:
-	Fetches the user’s current latitude and longitude using the Geolocation API.
-	Displays the coordinates on the screen.

-	Disaster Reporting:
-	Users input the disaster name and submit their location.
-	The information is updated in the notifications section and made visible to all logged-in users.

•	User Interface Design

-	Layout:
-	The layout is designed to be clean, intuitive, and user-friendly.
-	The three sections are clearly defined and positioned horizontally.

-	Styling:
-	The application uses CSS for styling to ensure an attractive and responsive design.
-	JavaScript is used for dynamic interactions, such as displaying popups and updating notifications.

•	API Integration

-	Gemini LLM API:
-	Used for providing disaster-related information through a chatbox.
-	Integration involves sending user queries and receiving responses relevant to the selected disaster.

-	Geolocation API:
-	Retrieves the user’s geographical coordinates.
-	Used to report and display disaster locations in real-time.

•	Backend and Data Storage

-	Flask (Python):
-	Manages user authentication, handles API requests, and serves data to the frontend.
-	Routes are created for user registration, login, geolocation updates, and disaster reporting.

-	Data Storage:
-	Excel Sheets:
-	User data, disaster reports, and notifications are stored and managed using local Excel sheets.
-	This approach is used for simplicity and local data management.

•	Security Considerations

-	Authentication:
-	Secure handling of user passwords.

-	Data Protection:
-	Ensure sensitive information is transmitted securely (e.g., use HTTPS).

•	Deployment

-	Hosting:
-	The application is deployed on a web server (i.e., Render) for public access.
-	Its not working because its making use of Local Database..

•	Future Enhancements

-	Mobile App Version:
-	Consider developing a mobile app version for broader accessibility.

-	Advanced Features:
-	Implement additional features such as real-time alerts, detailed disaster maps, and community forums.
