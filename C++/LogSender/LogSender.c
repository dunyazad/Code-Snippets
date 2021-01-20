//
// Created by jongh on 2021-01-07.
//

#include <time.h>
#include "LogSender.h"

double GetTimeInSeconds();

LogSender* gLogSender = 0;
void* SendingThread(void* arg);

void InitializeLogSender(){
    gLogSender = malloc(sizeof(LogSender));
    memset(gLogSender, 0, sizeof(LogSender));

    gLogSender->sock_fd = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&gLogSender->addr, 0, sizeof(struct sockaddr_in));
    gLogSender->addr.sin_family = AF_INET;
    gLogSender->addr.sin_port = htons(12121);
    inet_aton("192.168.3.170", &gLogSender->addr.sin_addr);

    gLogSender->finished = false;
    pthread_create(&gLogSender->sendingThread, NULL, SendingThread, "LogSender Sending Thread");

    gLogSender->initialized = true;
}

void* SendingThread(void* arg)
{
    pthread_mutex_init(&gLogSender->bufferLock, NULL);

    while(gLogSender->finished == false)
    {
        pthread_mutex_lock(&gLogSender->bufferLock);

        if(gLogSender->dataSize > 0)
        {
            sendto(gLogSender->sock_fd, gLogSender->buffer, gLogSender->dataSize, 0, (struct sockaddr*)&gLogSender->addr, sizeof(struct sockaddr_in));
            memset(gLogSender->buffer, 0, 1024);
            gLogSender->dataSize = 0;
        }

        pthread_mutex_unlock(&gLogSender->bufferLock);
        usleep(1);
    }

    pthread_mutex_destroy(&gLogSender->bufferLock);
    return NULL;
}

void SendLog(char* message){
    if(gLogSender == 0)
        InitializeLogSender();

    char buffer[1024];
    memset(buffer, 0, 1024);
    int length = sprintf(buffer, "[%f] %s", GetTimeInSeconds(), message);

    pthread_mutex_lock(&gLogSender->bufferLock);

    memcpy(gLogSender->buffer, buffer, length);
    gLogSender->dataSize = length;

    pthread_mutex_unlock(&gLogSender->bufferLock);
}

double GetTimeInSeconds() {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return (now.tv_sec * 1e9 + now.tv_nsec) * 0.000000001;
}
