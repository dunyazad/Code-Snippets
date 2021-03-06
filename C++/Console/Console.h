#pragma once

#include <string>
#define _CRT_SECURE_NO_WARNINGS
#pragma warning (disable : 4996)

class Console
{
	static Console* sConsole;

	//static std::string log;
	static bool sInitialized;

	Console() {}

public:
	static void initialize(int posX, int posY, int verticalSize)
	{
		if( sConsole == NULL )
		{
			AllocConsole();
			freopen( "CONOUT$", "wt", stdout );
			HWND ConsolehWnd = GetConsoleWindow();

			SetWindowPos( ConsolehWnd, HWND_TOPMOST,                          
				posX, posY, 800, verticalSize, SWP_SHOWWINDOW );

			sConsole = new Console();
			sInitialized = true;
		}
	}

	static void terminate()
	{
		if (sInitialized)
		{
			delete sConsole;
			sConsole = NULL;

			FreeConsole();
		}
	}

	static void OutLog(char *str, ...)
	{
		if (sInitialized == false) return;

		char msg[1024];

		va_list va;
		va_start(va, str);

		vsprintf(msg, str, va);

		va_end(va) ;
		printf("%s", msg);

		//log.append(msg);
	}

	static void OutLogString(char *str, ...)
	{
		if (sInitialized == false) return;

		char msg[1024];

		va_list va;
		va_start(va, str);

		vsprintf(msg, str, va);

		va_end(va) ;
		printf("%s\n", msg);

		//log.append(msg);
	}

	/*void flush()
	{
		FILE* fp = OpenFile(
	}*/
};

Console* Console::sConsole = 0;
bool Console::sInitialized = false;
