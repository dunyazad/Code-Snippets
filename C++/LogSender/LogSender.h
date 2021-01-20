//
// Created by jongh on 2021-01-07.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <unistd.h>

#ifndef IXRCLIENT_LOGSENDER_H
#define IXRCLIENT_LOGSENDER_H

typedef struct _LogSender {
    bool initialized;
    bool finished;
    int sock_fd;
    struct sockaddr_in addr;
    pthread_t sendingThread;
    char buffer[1024];
    int dataSize;
    pthread_mutex_t bufferLock;
} LogSender;

void InitializeLogSender();
void SendLog(char* message);

#endif //IXRCLIENT_LOGSENDER_H
