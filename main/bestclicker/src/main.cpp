#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <time.h>
#include <math.h>
#include <string>
#include <pthread.h>
using namespace std;

// DLL NAME (LINE 13)

char* dll_path = "SDLWAPI.dll";

// Vars

bool running = true;
bool toggle = false;
int CPS = 10;
int delay;

typedef void (__stdcall *StartPaint)();
typedef void (__stdcall *StopPaint)();
typedef void (__stdcall *AbortPaint)();
typedef void (__stdcall *SetDelay)(int);
typedef void* (__stdcall *StartDialog)(void*);

// DLL Vars

HINSTANCE hGetProcIDDLL;
StartPaint a1;
StopPaint a2;
AbortPaint a3;
SetDelay a4;
StartDialog a5;

int sock_com(SOCKET s) {

    int bytes;
    int buf_len = 1024;
    char buffer[buf_len];

    string response;
    string toggled = (toggle ? "on" : "off");

    memset(buffer, 0, buf_len);
    strcpy(buffer, toggled.c_str());
    send(s, buffer, buf_len, 0);

    while (running) {

        memset(buffer, 0, buf_len);
        bytes = recv(s, buffer, buf_len, 0);

        if (bytes < 0) {
            if (response != "exit") cout << "SOCKET | Server error" << endl;
            return -1;
        } else {
            if (response == "updt") {
                response = buffer;
                CPS = stoi(response);
                delay = (1000 / CPS) - (CPS/3);
                a4(delay);

                cout << "Updated to " << CPS << " CPS" << endl;
            }
            response = buffer;
            if (response == "togl") {
                toggle = !toggle;
                if (toggle) a1();
                else a2();

                toggled = (toggle ? "on" : "off");
                memset(buffer, 0, buf_len);
                strcpy(buffer, toggled.c_str());
                send(s, buffer, buf_len, 0);

                cout << "Autoclicker toggle " << (toggle ? "on" : "off") << endl;
            }
            if (response == "updt") {
                cout << "Autoclicker update cps" << endl;
            }
            if (response == "clse") {
                cout << "Closing" << endl;
                a3();
                running = false;
            }
            if (response == "exit") {
                break;
            }
        }
    }
    return 0;
}

int main() {

    FreeConsole();

    // Instance DLL
    hGetProcIDDLL = LoadLibrary(dll_path);
    while (!hGetProcIDDLL) {
        try {
            hGetProcIDDLL = LoadLibrary(dll_path);
        } catch(...){}
    }

    // Load Functions
    a1 = (StartPaint)GetProcAddress(hGetProcIDDLL, "StartPaint");
    if (!a1) return EXIT_FAILURE;
    a2 = (StopPaint)GetProcAddress(hGetProcIDDLL, "StopPaint");
    if (!a2) return EXIT_FAILURE;
    a3 = (AbortPaint)GetProcAddress(hGetProcIDDLL, "AbortPaint");
    if (!a3) return EXIT_FAILURE;
    a4 = (SetDelay)GetProcAddress(hGetProcIDDLL, "SetDelay");
    if (!a4) return EXIT_FAILURE;
    a5 = (StartDialog)GetProcAddress(hGetProcIDDLL, "StartDialog");
    if (!a5) return EXIT_FAILURE;

    SOCKET server, a_server;

    int port = 42069;
    WSADATA wsaData;
    WORD wsaVer = MAKEWORD(2, 2);
    WSAStartup(wsaVer, &wsaData);

    server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    sockaddr_in service;
    service.sin_family = AF_INET;
    service.sin_addr.s_addr = INADDR_ANY;
    service.sin_port = htons(port);

    bind(server, (SOCKADDR*)&service, sizeof(service));
    listen(server, 1);

    pthread_t clickth;
    pthread_create(&clickth, NULL, a5, NULL);

    while (running) {
        cout << "Waiting for a connection" << endl;
        a_server = accept(server, NULL, NULL);
        if (a_server == INVALID_SOCKET) {
            cout << "Failed to accept" << endl;
            WSACleanup();
            return -1;
        }
        cout << "Client connected" << endl;
        sock_com(a_server);
        closesocket(a_server);
        cout << "Client disconnected" << endl;
    }
    pthread_join(clickth, NULL);
    closesocket(server);
    WSACleanup();
    FreeLibrary(hGetProcIDDLL);
    return 0;
}
