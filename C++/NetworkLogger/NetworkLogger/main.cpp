#include <iostream>
#include <string>
#include <memory>
#include <thread>
#include <mutex>
#include <queue>
#include <condition_variable>
#include <WinSock2.h>
#include <WS2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")

class Logger {
public:
    virtual void log(const char* format, ...) = 0;
    virtual ~Logger() {}
};

class NetworkLogger : public Logger {
public:
    NetworkLogger(const std::string& multicastGroup, int port)
        : multicastGroup(multicastGroup), port(port), stopFlag(false), socket_fd(0) {
        // Initialize Winsock
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            std::cerr << "WSAStartup failed" << std::endl;
            return;
        }

        // Create UDP socket
        if ((socket_fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == INVALID_SOCKET) {
            std::cerr << "Failed to create socket" << std::endl;
            return;
        }

        // Enable reuse of address and port
        int reuse = 1;
        if (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&reuse, sizeof(reuse)) == SOCKET_ERROR) {
            std::cerr << "setsockopt SO_REUSEADDR failed" << std::endl;
            closesocket(socket_fd);
            return;
        }

        // Setup server address
        memset(&serverAddr, 0, sizeof(serverAddr));
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(port);
        serverAddr.sin_addr.s_addr = htonl(INADDR_ANY); // Bind to any available interface

        // Bind to the port
        if (bind(socket_fd, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
            std::cerr << "bind failed with error" << WSAGetLastError() << std::endl;
            closesocket(socket_fd);
            return;
        }

        // Join multicast group
        ip_mreq mreq;
        InetPtonA(AF_INET, multicastGroup.c_str(), &mreq.imr_multiaddr);
        mreq.imr_interface.s_addr = htonl(INADDR_ANY);
        if (setsockopt(socket_fd, IPPROTO_IP, IP_ADD_MEMBERSHIP, (char*)&mreq, sizeof(mreq)) == SOCKET_ERROR) {
            std::cerr << "setsockopt IP_ADD_MEMBERSHIP failed" << std::endl;
            closesocket(socket_fd);
            return;
        }

        // Start the background logging thread
        loggingThread = std::thread(&NetworkLogger::loggingLoop, this);
    }

    void log(const char* format, ...) override {
        char buffer[1024];
        va_list args;
        va_start(args, format);
        vsnprintf(buffer, sizeof(buffer), format, args);
        va_end(args);
        send(buffer);
    }

    ~NetworkLogger() {
        {
            std::lock_guard<std::mutex> lock(mutex);
            stopFlag = true;
        }
        condition.notify_one(); // Notify the logging thread to stop

        // Join the logging thread
        if (loggingThread.joinable())
            loggingThread.join();

        // Cleanup Winsock
        WSACleanup();

        // Close socket
        if (socket_fd != INVALID_SOCKET)
            closesocket(socket_fd);
    }

private:
    std::string multicastGroup;
    int port;
    bool stopFlag;
    SOCKET socket_fd;
    struct sockaddr_in serverAddr;
    std::queue<std::string> logQueue;
    std::thread loggingThread;
    std::mutex mutex;
    std::condition_variable condition;

    void loggingLoop() {
        while (true) {
            std::unique_lock<std::mutex> lock(mutex);
            condition.wait(lock, [this] { return !logQueue.empty() || stopFlag; });

            // Check if it's time to stop
            if (stopFlag && logQueue.empty())
                break;

            // Process the log queue
            while (!logQueue.empty()) {
                std::string message = logQueue.front();
                logQueue.pop();
                send(message);
            }
        }
    }

    void send(const std::string& message) {
        // Send log message over UDP multicast
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        InetPtonA(AF_INET, multicastGroup.c_str(), &addr.sin_addr);
        addr.sin_port = htons(port);

        if (sendto(socket_fd, message.c_str(), message.length(), 0,
            (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
            std::cerr << "Failed to send message: " << WSAGetLastError() << std::endl;
        }
    }
};

// Example usage
int main() {
    // Create a network logger for multicast
    std::unique_ptr<Logger> logger = std::make_unique<NetworkLogger>("239.255.0.1", 1234);

    // Log some messages
    logger->log("This is a multicast log message with value: %d", 42);
    logger->log("Another multicast log message with value: %f", 3.14);

    // Wait for a while to allow background thread to process logs
    std::this_thread::sleep_for(std::chrono::seconds(1));

    return 0;
}
