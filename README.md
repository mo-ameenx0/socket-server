# Socket Server Application

This project consists of a basic client-server application using socket programming. The application allows for user authentication (signup, login, logout), file operations (listing, downloading, uploading), action history viewing, and file searching.

## Getting Started

### Prerequisites

- Python 3.6+
- A virtual environment (recommended)

### Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory and set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Set up the necessary environment variables in `.env` files within both `client` and `server` directories. You need to specify the `HOST` and `PORT` values that the server will listen on and the client will connect to.

Example `.env` content:

```
HOST=localhost
PORT=12345
```

### Running the Server

Navigate to the `server` directory and start the server using:

```bash
python main.py
```

### Running the Client

Open a new terminal window, navigate to the `client` directory, and start the client using:

```bash
python client.py --action [arguments...]
```

Replace `--action` with specific operations like `--signup`, `--login`, etc., followed by the necessary arguments.

## Client Operations

- **Signup**: `python client.py --signup --name USERNAME --password PASSWORD`
- **Login**: `python client.py --login --name USERNAME --password PASSWORD`
- **Logout**: `python client.py --logout --session_id SESSION_ID`
- **List Files**: `python client.py --listing --session_id SESSION_ID`
- **Download File**: `python client.py --download --file_name FILENAME --session_id SESSION_ID`
- **Upload File**: `python client.py --upload --file_path FILEPATH --session_id SESSION_ID`
- **View History**: `python client.py --history --session_id SESSION_ID`
- **Search Files**: `python client.py --search QUERY_STRING --session_id SESSION_ID`

## Protocol Documentation

### Protocol Overview

The communication protocol between the client and server is designed around a simple, text-based format. Each request from the client to the server follows this format:

```
REQUEST = '{method}|{message}'
```

- `{method}`: This is a string that represents the action the client wants to perform. It's a predefined keyword understood by both the client and server, such as `login`, `signup`, `download`, etc.
- `{message}`: Accompanies the method and provides necessary data for the server to process the request. The content and structure of the message depend on the method being invoked.

The server parses each incoming request by splitting the string on the `|` delimiter. The first part is interpreted as the method, and the second part as the message. Based on the method, the server then knows how to further parse the message and what action to take.

### Client Request Invocation

Clients invoke methods by constructing a request string in the above format and sending it to the server. Here's how the client can format requests for different methods:

1. **Signup**: To create a new account.

   - **Request Format**: `signup|{'NAME':'name', 'PASSWORD':'password'}`
   - **Client Invocation**: The client would construct this request, replacing `{name}` and `{password}` with the desired username and password, and send it to the server.

2. **Login**: To authenticate an existing user.

   - **Request Format**: `login|{'NAME':'name', 'PASSWORD':'password'}`
   - **Client Invocation**: Similar to signup, with the client replacing `{name}` and `{password}` with their credentials.

3. **Logout**: To end a session for the logged-in user.

   - **Request Format**: `logout|{'SESSION_ID':'session_id'}`
   - **Client Invocation**: The client sends this request with the current session ID to log out.

4. **File Listing**: To list all available files.

   - **Request Format**: `listing|{'SESSION_ID':'session_id'}`
   - **Client Invocation**: The client sends this request with the current session ID to get a list of files.

5. **File Download**: To request a file download.

   - **Request Format**: `download|{'SESSION_ID':'session_id', 'FILE_NAME':'file_name'}`
   - **Client Invocation**: The client specifies the file name to download in the request.

6. **File Upload**: To upload a new file.

   - **Request Format**: `upload|{'SESSION_ID':'session_id', 'FILE_NAME':'file_name', 'FILE_CHUNK':'file_chunk'}`
   - **Client Invocation**: The client includes the file name and content in the message part of the request.

7. **View History**: To view the action history of the user.

   - **Request Format**: `history|{'SESSION_ID':'session_id'}`
   - **Client Invocation**: The client sends this request with the session ID to retrieve the user's history.

8. **Search**: To search for files using a query string.
   - **Request Format**: `search|{'SESSION_ID':'session_id', 'FILE_NAME':'file_name'}`
   - **Client Invocation**: The client includes a search query in the request message.

### Server Request Processing

Upon receiving a request, the server performs the following steps:

1. **Parse the Request**: The server splits the incoming request string on `|` to extract the method and message.
2. **Identify the Method**: The server checks the method against known methods. If the method is recognized, it proceeds to process the request; otherwise, it returns an error.
3. **Process the Message**: Depending on the method, the server may need to further parse the message part of the request to extract necessary data (like username, password, file name, etc.).
4. **Perform the Action**: The server executes the requested action, such as creating a user account, authenticating a user, listing files, etc.
5. **Send a Response**: The server constructs a response indicating the outcome of the request and sends it back to the client.
