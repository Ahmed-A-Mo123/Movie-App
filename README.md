# MasterFlix 🎬

MasterFlix is a web application designed to be your ultimate movie companion. Whether you want to keep track of movies you want to watch, share your favorite films with others, or express your thoughts through reviews, MasterFlix has got you covered. 🍿

## Features

- **Movie Management**: Save movies you want to watch or love in your personalized profile.
- **Review System**: Share your thoughts by adding reviews to movies, be it your own or others'.
- **User Profiles**: Enjoy a personalized experience with user profiles to keep track of your movie journey.
- **User Authentication**: Secure your account with user login features.

## Technologies Used

MasterFlix is powered by cutting-edge technologies to enhance your movie experience.

- **Bootstrap**: Stylish and responsive front-end design for an engaging user interface.
- **Flask**: A lightweight and versatile web framework in Python for robust backend development.
- **SQLAlchemy**: A powerful SQL toolkit for database integration, ensuring seamless data management.

## Movie API Integration

MasterFlix leverages a movie API to fetch detailed information about movies, including ratings, posters, directors, and more. This integration allows users to add movies to their profiles effortlessly.

## Getting Started

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Ahmed-A-Mo123/Movie-App.git
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Database Setup**:

    Update the database URI in `config.py` to your desired database and run:

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

4. **Run the Application**:


5. **Access MasterFlix**:

    Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Contributing

We welcome contributions to make MasterFlix even better! If you have any ideas, bug reports, or feature requests, feel free to open an issue or submit a pull request.

🎉 Happy movie watching with MasterFlix! 🎉
```
