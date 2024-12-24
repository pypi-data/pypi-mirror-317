# **PingPong: A Dynamic and Scalable Notification Delivery System**

PingPong is a robust, scalable, and highly customizable **Dynamic Notification Delivery System** designed to efficiently manage and deliver notifications across various channels, including **Email**, **SMS**, and **Push Notifications**. Built with modern technologies and adhering to high-performance standards, PingPong serves as a comprehensive solution for handling diverse notification workflows, ensuring reliability, speed, and scalability.

---

## **Features**
### 🔔 **Multi-Channel Notification Delivery**
- **Email**: Seamlessly integrates with **Mailgun** and other email providers for reliable email delivery {Future Scope}.
- **SMS**: Supports integration with **Twilio** for fast and secure text message delivery.
- **Push Notifications**: Will be implementing for real-time, personalized push notifications to mobile and web devices. {Future Scope}

### 💾 **Data Management**
- Centralized storage in **Google Firestore**, optimized for managing user preferences and notification history.
- Flexible and scalable queues powered by **Redis** and **Kafka**, ensuring efficient message processing and delivery.

### ⚡ **User-Centric Design**
- Supports **user preferences** to respect channel priorities and avoid unnecessary notifications.
- Allocates **unique notification IDs** for precise tracking and audit trails.

### 🛡️ **Secure and Robust Architecture**
- **Authentication and Authorization**:
  - Implements a secure login and signup feature with **JWT-based authentication**.
  - Dynamically handles notification publishing based on logged-in user context.
- **Message Integrity**: Ensures notifications are correctly routed to their intended users, leveraging Redis and Kafka filtering logic.

### 🚀 **Scalability and Performance**
- Dockerized microservice architecture for seamless deployment and portability.
- Scalable infrastructure to handle millions of notifications, ensuring minimal latency and high throughput.
- Auto-scaling and cost-efficient hosting on **GCP Cloud Run** with pay-as-you-use billing.

### 🛠️ **Developer-Friendly**
- Designed for extensibility with clear and modular code.
- Supports new channel integrations with minimal effort.
- Just import the package for publishing, consuming, and managing notifications.


### 🛠️ **User-Friendly**
- Easy-to-use interface with a class-based design for sending notifications.
- You can opt for trail account for sending 3 emails and 1 sms/48 hours.
- Support for configurable parameters, including sender, receiver, notification channels & API/Auth Keys.
- Integration with popular services like Mailgun (for email) and Twilio (for SMS).
- Future-ready: Additional notification services will be supported in upcoming updates.
- Fully customizable by passing API Keys and Auth Tokens.
---

## **Tech Stack**
- **Backend**: Python, FastAPI
- **Messaging Queues**: Kafka, Redis
- **Database**: Google Firestore
- **Notifications**: Mailgun, Twilio, OneSignal
- **Deployment**: Docker, GCP Cloud Run
- **Authentication**: JWT-based authentication and role management

---

## **How It Works**
1. **Notification Publishing**:
   - Users or services send notification requests via a REST API endpoint for demo purpose or by importing python package with their personal API keys.
   - Notifications are queued in **Redis** and **Kafka** for asynchronous processing.

2. **User Preferences**:
   - Every user can configure their preferred notification channels (e.g., Email, SMS).
   - Notifications respect user preferences during both publishing and consumption.

3. **Message Consumption**:
   - Consumers retrieve notifications from queues and deliver them through the appropriate channels.
   - Redis ensures only recent and relevant messages are processed.

4. **Integration with External Services**:
   - Email and SMS are sent using external providers (Mailgun, Omnisend, Twilio, etc).

5. **Analytics and Tracking**:
   - All notifications are logged with unique IDs in **Firestore**, enabling detailed tracking and reporting.

---

## **GitHub Setup and Usage**
1. Clone the repository:
   ```bash
   git clone https://github.com/karan-kap00r/PingPong.git
   cd pingpongx
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the API on `http://localhost:8080` and explore the interactive Swagger documentation at `http://localhost:8000/docs`.

4. Configure your environment variables:
   - Redis and Kafka configurations.
   - API keys for Mailgun, Twilio, Omnisend, and OneSignal.

5. Enjoy the PingPong.

---

## **PyPI Setup and Usage**
- To import package:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/import.png)
- To send notifications by importing python package:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/code.png)
- To set and get user preferences:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/get_set_UP.png)

---
## **Usage Via APIs**
- To SignUp:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/signUp.png)
- To Login:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/login.png)
- To Send Notifications:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/send.png)
- To Get User Preferences:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/getUP.png)
- To Update User Preferences:
![Image description](https://raw.githubusercontent.com/karan-kap00r/PingPong/refs/heads/master/static/setUP.png)
---

## **Why PingPong?**
PingPong is the ultimate notification management solution for projects demanding:
- **High performance**: Deliver notifications at lightning speed to millions of users.
- **Scalability**: Handle growing notification workloads with ease.
- **Flexibility**: Support for multiple notification channels and user preferences.
- **Security**: Robust authentication and secure data management.

---

## **Contributions**
We welcome contributions to enhance PingPong! Feel free to submit pull requests, open issues, or share feature ideas.

---

## **License**
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  

---
